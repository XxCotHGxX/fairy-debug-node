import os
import sys
import subprocess
import shutil
import time
import json
import glob
import re
import requests
from pathlib import Path
from typing import Optional, Dict

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Import the row generation logic
# Add scripts_python to path to allow import
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / "scripts_python"))
from generate_sheet_row import generate_row_data

# Load environment variables
load_dotenv()

app = FastAPI()

# Directories
CODE_DIR = BASE_DIR / "code"
LOG_DIR = BASE_DIR / "logs"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"
CODE_TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "debug_template.py"

# Store active subprocesses: { "datarow_step": subprocess.Popen }
active_processes: Dict[str, subprocess.Popen] = {}

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Configure Server URL
SERVER_URL = os.getenv("SERVER_URL")
TOKEN = os.getenv("TOKEN")

class SubmissionRequest(BaseModel):
    competition_id: str
    datarow_id: str
    debug_step: int
    code: str
    original_plan: Optional[str] = ""
    proposed_analysis: Optional[str] = ""

class ScaffoldRequest(BaseModel):
    competition_id: str
    datarow_id: str
    debug_step: int

class GenerateRowRequest(BaseModel):
    competition_id: str
    datarow_id: str
    debug_step: int
    proposed_analysis: Optional[str] = ""

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/scaffold")
async def scaffold_file(req: ScaffoldRequest):
    filename = f"{req.datarow_id}_{req.competition_id}_{req.debug_step}.py"
    file_path = CODE_DIR / filename
    
    if file_path.exists():
        return {"status": "error", "message": f"File {filename} already exists"}
        
    if not CODE_TEMPLATE_PATH.exists():
        return {"status": "error", "message": "Debug template not found"}
        
    try:
        shutil.copy(CODE_TEMPLATE_PATH, file_path)
        return {"status": "success", "message": f"Created {filename}", "filename": filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/run")
async def run_submission(req: SubmissionRequest):
    # 1. Validate and construct filename
    filename = f"{req.competition_id}_{req.datarow_id}_{req.debug_step}.py"
    file_path = CODE_DIR / filename
    
    # 2. Write code to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(req.code)
    
    # 3. Clear existing logs for this run
    log_path = LOG_DIR / req.datarow_id / f"{req.debug_step}.jsonl"
    if log_path.exists():
        os.remove(log_path)
        
    # 4. Run gpu_submit.sh in background
    try:
        # Capture output to a log file for live streaming
        raw_log_path = LOG_DIR / req.datarow_id / f"{req.debug_step}.raw.log"
        raw_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        log_file = open(raw_log_path, "w", encoding="utf-8")
        
        # Use unbuffered output for python if we were running python, but this is bash
        # We removed --force to avoid re-submitting other files in code/ that already have logs.
        # Since we deleted the specific log for this run above, gpu_submit.sh will run this one naturally.
        cmd = ["bash", "gpu_submit.sh"]
        
        process = subprocess.Popen(
            cmd, 
            cwd=str(BASE_DIR), 
            stdout=log_file, 
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8'
        )
        
        # Store process to allow cancellation
        key = f"{req.datarow_id}_{req.debug_step}"
        active_processes[key] = process
        
        return {"status": "started", "message": f"Started submission for {filename}"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/logs/{datarow_id}/{debug_step}")
async def get_live_logs(datarow_id: str, debug_step: int):
    raw_log_path = LOG_DIR / datarow_id / f"{debug_step}.raw.log"
    if raw_log_path.exists():
        try:
            with open(raw_log_path, "r", encoding="utf-8") as f:
                return {"content": f.read()}
        except Exception:
            return {"content": "Error reading log file"}
    return {"content": "Waiting for logs..."}

@app.get("/api/code/{competition_id}/{datarow_id}/{debug_step}")
async def get_code_file(competition_id: str, datarow_id: str, debug_step: int):
    filename = f"{competition_id}_{datarow_id}_{debug_step}.py"
    file_path = CODE_DIR / filename
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return {"code": f.read()}
        except Exception as e:
            return {"code": f"Error reading code file: {e}"}
    return JSONResponse(status_code=404, content={"message": f"Code file not found: {filename}"})

@app.get("/api/status/{datarow_id}/{debug_step}")
async def get_status(datarow_id: str, debug_step: int):
    # Check if process is still running
    key = f"{datarow_id}_{debug_step}"
    is_local_running = False
    if key in active_processes:
        if active_processes[key].poll() is None:
            is_local_running = True
        else:
            del active_processes[key]

    log_path = LOG_DIR / datarow_id / f"{debug_step}.jsonl"
    
    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Only return completed if we have valid JSON
                data = json.loads(content)
                return {"status": "completed", "data": data}
        except json.JSONDecodeError:
            pass # Log exists but incomplete
            
    return {"status": "running" if is_local_running else "processing", "message": "Waiting for logs..."}

@app.post("/api/cancel/{datarow_id}/{debug_step}")
async def cancel_job(datarow_id: str, debug_step: int):
    key = f"{datarow_id}_{debug_step}"
    
    # 1. Kill local process
    if key in active_processes:
        proc = active_processes[key]
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
        del active_processes[key]
    
    # 2. Try to find Job ID in the raw log and kill remote
    remote_cancelled = False
    job_id = None
    raw_log_path = LOG_DIR / datarow_id / f"{debug_step}.raw.log"
    if raw_log_path.exists():
        try:
            with open(raw_log_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Regex to find Job ID: "Job ID: xxxxxxxx-..."
                match = re.search(r"Job ID: ([a-f0-9\-]+)", content)
                if match and SERVER_URL and TOKEN:
                    job_id = match.group(1)
                    # Call remote cancel
                    headers = {
                        "Authorization": f"Bearer {TOKEN}",
                        "ngrok-skip-browser-warning": "true"
                    }
                    try:
                        cancel_response = requests.post(
                            f"{SERVER_URL}/api/cancel/{job_id}", 
                            headers=headers, 
                            verify=False, 
                            timeout=10
                        )
                        cancel_response.raise_for_status()
                        cancel_data = cancel_response.json()
                        
                        # Verify cancellation by checking job status
                        import time
                        time.sleep(1)  # Brief wait for status to update
                        status_response = requests.get(
                            f"{SERVER_URL}/api/status/{job_id}",
                            headers=headers,
                            verify=False,
                            timeout=5
                        )
                        
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            remote_status = status_data.get("status", "")
                            
                            if remote_status in ["cancelled", "completed", "failed"]:
                                remote_cancelled = True
                                return {
                                    "status": "success", 
                                    "message": f"Job {job_id} cancelled and confirmed. Remote status: {remote_status}"
                                }
                            else:
                                return {
                                    "status": "warning", 
                                    "message": f"Cancellation sent, but job still shows status: {remote_status}. Job ID: {job_id}"
                                }
                        else:
                            return {
                                "status": "warning", 
                                "message": f"Cancellation sent to {job_id}, but could not verify status"
                            }
                            
                    except requests.exceptions.Timeout:
                        return {"status": "warning", "message": f"Timeout cancelling remote job {job_id}. Check manually."}
                    except requests.exceptions.RequestException as e:
                        return {"status": "warning", "message": f"Failed to cancel remote job {job_id}: {str(e)}"}
                    except Exception as e:
                        return {"status": "warning", "message": f"Error cancelling/verifying job {job_id}: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Error reading log file: {str(e)}"}
    
    if job_id:
        return {"status": "warning", "message": f"Local stopped, but remote job {job_id} cancellation could not be confirmed"}
    else:
        return {"status": "success", "message": "Local process stopped (no remote job ID found in logs)"}

@app.post("/api/mark_no_repro")
async def mark_no_repro(req: SubmissionRequest):
    # 1. Cancel job if running and confirm remote cancellation
    cancel_result = await cancel_job(req.datarow_id, req.debug_step)
    
    # Check if remote cancellation was successful
    if cancel_result.get("status") == "warning":
        # Return warning message so user knows cancellation might not have worked
        return {
            "status": "warning",
            "message": f"Cannot mark as No Repro: {cancel_result.get('message')}. Please ensure the remote job is cancelled first."
        }
    
    # 2. Create placeholder log
    log_path = LOG_DIR / req.datarow_id / f"{req.debug_step}.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({
            "status": "skipped", 
            "message": "Manually verified (Runtime > 600s). No error reproduced."
        }, f)
        
    return {
        "status": "success",
        "message": "Marked as No Repro"
    }

@app.post("/api/generate_row")
async def generate_row(req: GenerateRowRequest):
    try:
        # Force reload to pick up changes to the script without restarting server
        import sys
        import importlib
        if 'generate_sheet_row' in sys.modules:
            import generate_sheet_row
            importlib.reload(generate_sheet_row)
            generate_row_data_func = generate_sheet_row.generate_row_data
        else:
            # Fallback if not in sys.modules (should be there from top-level import)
            from generate_sheet_row import generate_row_data as generate_row_data_func

        row_dict, raw_string = generate_row_data_func(
            req.competition_id, 
            req.datarow_id, 
            req.debug_step, 
            root_path=BASE_DIR,
            proposed_analysis=req.proposed_analysis # Pass the analysis
        )
        return {
            "status": "success",
            "columns": row_dict,
            "raw_string": raw_string
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Failed to generate row: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
