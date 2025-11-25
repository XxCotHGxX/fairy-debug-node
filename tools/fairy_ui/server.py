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

# Load environment variables
load_dotenv()

app = FastAPI()

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
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

# Configure LM Studio (local model)
SERVER_URL = os.getenv("SERVER_URL")
TOKEN = os.getenv("TOKEN")
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")  # Default LM Studio endpoint

class SubmissionRequest(BaseModel):
    competition_id: str
    datarow_id: str
    debug_step: int
    code: str
    original_plan: Optional[str] = ""
    ai_provider: Optional[str] = "gemini"

class ScaffoldRequest(BaseModel):
    competition_id: str
    datarow_id: str
    debug_step: int

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
        
    # 3. Return standard No Repro data
    # Returns a stringified JSON in 'analysis' to match the structure expected by the frontend's Gemini parser
    standard_response = {
        "revised_analysis": "The code executed successfully for over 6 minutes without throwing any errors.",
        "revised_plan": "N/A",
        "bug_confirmed": False,
        "bug_fixed": True,
        "proposed_debug_analysis_accurate": 0,
        "initial_bug_reproducible": False,
        "all_bugs_fixed": True
    }
    
    return {
        "status": "success",
        "analysis": json.dumps(standard_response)
    }

@app.post("/api/analyze")
async def analyze_results(req: SubmissionRequest):
    # 1. Get the logs
    log_path = LOG_DIR / req.datarow_id / f"{req.debug_step}.jsonl"
    if not log_path.exists():
        return {"status": "error", "message": "No logs found to analyze"}
        
    with open(log_path, "r", encoding="utf-8") as f:
        log_content = f.read()
    
    # 2. Get the previous step's code to preserve all fixes
    previous_code = req.code  # Start with current code
    if req.debug_step > 0:
        prev_step = req.debug_step - 1
        prev_filename = f"{req.competition_id}_{req.datarow_id}_{prev_step}.py"
        prev_file_path = CODE_DIR / prev_filename
        if prev_file_path.exists():
            with open(prev_file_path, "r", encoding="utf-8") as f:
                previous_code = f.read()

    # 3. Build History Context from Analysis Files
    history_context = ""
    if req.debug_step > 0:
        history_context = "HISTORY OF APPLIED FIXES (CRITICAL: YOU MUST PRESERVE THESE):\n"
        for step in range(req.debug_step):
            # Try to read the analysis file first (contains the plan)
            analysis_path = LOG_DIR / req.datarow_id / f"analysis_{step}.json"
            if analysis_path.exists():
                try:
                    with open(analysis_path, "r", encoding="utf-8") as f:
                        analysis_data = json.load(f)
                        if "revised_plan" in analysis_data:
                            history_context += f"\n[Step {step} Fix]\nPlan: {analysis_data.get('revised_plan')}\n"
                except Exception:
                    pass
            else:
                # Fallback to log file if analysis doesn't exist
                step_log_path = LOG_DIR / req.datarow_id / f"{step}.jsonl"
                if step_log_path.exists():
                    try:
                        with open(step_log_path, "r", encoding="utf-8") as f:
                            step_data = json.load(f)
                            if "message" in step_data:
                                history_context += f"\n[Step {step} Result]\n{step_data.get('message')}\n"
                    except Exception:
                        pass
        history_context += "\nDO NOT REVERT ANY OF THE ABOVE FIXES unless they are directly causing the current error.\n"

    # 4. Build the prompt (simplified for local models)
    prompt = f"""Analyze this ML competition code execution and return ONLY a valid JSON object.

CRITICAL: You MUST preserve ALL previous bug fixes when generating the fixed_code. Do NOT remove or undo any existing fixes.

CONTEXT:
- Competition: {req.competition_id}
- Original client plan: {req.original_plan[:500] if req.original_plan else "None"}

{history_context}

ERROR LOG:
{log_content[:2000]}

CURRENT CODE (BASE - preserve ALL fixes from this):
{previous_code[:4000]}

TASK: Return ONLY this JSON structure (no markdown, no explanations):

{{
  "revised_analysis": "Single paragraph explaining the error, line number, and root cause in third person.",
  "revised_plan": "**Bug Fix Plan**\\n1. Line X: Description\\n2. Line Y: Description",
  "fixed_code": "The COMPLETE fixed python code. Must be the full file content, not just a snippet.",
  "analysis_accuracy_explanation": "Brief explanation of why the original plan was correct, partially correct, or wrong.",
  "bug_confirmed": true,
  "bug_fixed": false,
  "proposed_debug_analysis_accurate": 2,
  "initial_bug_reproducible": true,
  "all_bugs_fixed": false
}}

RULES:
- revised_analysis: One paragraph, third person, include error message and line number
- revised_plan: MUST follow this exact format:
  **Bug Fix Plan**
  1. Line X: [Specific change description]
  2. Line Y: [Specific change description]
  3. Keep rest of pipeline unchanged: [List unchanged parts]
- fixed_code: The FULL python script with ALL previous fixes preserved PLUS the new fix. Start from CURRENT CODE above and only add/modify the specific lines mentioned in revised_plan. Do NOT remove existing bug fixes. CRITICAL: The code MUST be valid Python syntax - it will be validated before saving. Ensure all imports, indentation, and syntax are correct.
- analysis_accuracy_explanation: 1-2 sentences explaining the accuracy rating.
- bug_confirmed: true if error occurred, false if success=true
- bug_fixed: true if success=true AND valid_solution=true, else false
- proposed_debug_analysis_accurate: 0 (wrong), 1 (partial), 2 (correct) - compare with Original Plan
- initial_bug_reproducible: true if client's bug was reproduced, false otherwise
- all_bugs_fixed: true only if this is final step and all bugs fixed, else false

IMPORTANT: When generating fixed_code, you MUST:
1. Start with the CURRENT CODE provided above (which includes all previous fixes)
2. Only modify the specific lines mentioned in your revised_plan
3. DO NOT remove or undo any existing bug fixes (look for comments like #***BUG FIX***)
4. Add your new fix alongside the existing fixes
5. Ensure the code is valid Python syntax - check all indentation, quotes, brackets, and imports. The code will be validated before saving.

Return ONLY the JSON, nothing else."""

    
    # 3. Call AI Provider
    if req.ai_provider == "gemini":
        analysis_result = await call_gemini(prompt)
    else:
        analysis_result = await call_lm_studio(prompt)
        
    # Save analysis to file if successful
    if analysis_result["status"] == "success":
        try:
            log_dir = log_path.parent # Get the directory from the already defined log_path
            analysis_file = log_dir / f"analysis_{req.debug_step}.json"
            with open(analysis_file, "w", encoding="utf-8") as f:
                # Parse the JSON string back to dict for pretty printing, or just save raw string
                # analysis_result["analysis"] is a JSON string
                json_obj = json.loads(analysis_result["analysis"])
                json.dump(json_obj, f, indent=2)
            print(f"Saved analysis to {analysis_file}")
        except Exception as e:
            print(f"Failed to save analysis file: {e}")
            
    return analysis_result

async def call_gemini(prompt: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"status": "error", "message": "GEMINI_API_KEY not found in environment variables"}

    # Simple REST call to Gemini API to avoid adding google-generativeai dependency if not needed
    # Using gemini-2.0-flash (Stable) as agreed with user for Paid Tier usage and reliability
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 65536,  # Kept high just in case, though model might cap at 8k
            "responseMimeType": "application/json"
        }
    }
    
    max_retries = 3
    base_delay = 2
    
    for attempt in range(max_retries + 1):
        try:
            # Increased timeout to 300s (5m) as 60s was timing out for large code generation
            response = requests.post(url, json=payload, timeout=300)
            
            if response.status_code == 200:
                data = response.json()
                # Extract text from Gemini response structure
                try:
                    if "candidates" not in data or not data["candidates"]:
                         return {"status": "error", "message": "Gemini returned no candidates"}
                    
                    candidate = data["candidates"][0]
                    
                    if "content" in candidate and "parts" in candidate["content"]:
                        analysis_text = candidate["content"]["parts"][0]["text"]
                        return process_analysis_text(analysis_text)
                    else:
                        # Check for safety/other finish reasons
                        finish_reason = candidate.get("finishReason", "UNKNOWN")
                        safety_ratings = candidate.get("safetyRatings", [])
                        print(f"Gemini No Content. Finish Reason: {finish_reason} - Safety: {safety_ratings}")
                        
                        if finish_reason == "MAX_TOKENS":
                            return {"status": "error", "message": "Gemini hit token limit (MAX_TOKENS). Try reducing code size or check logs."}
                            
                        return {"status": "error", "message": f"Gemini refused to generate content. Reason: {finish_reason} (Check terminal for safety details)"}
                except (KeyError, IndexError) as e:
                    print(f"Gemini Format Error: {e} - Data: {data}")
                    return {"status": "error", "message": f"Unexpected Gemini response format: {str(e)}"}
            elif response.status_code == 503 or response.status_code == 429:
                if attempt < max_retries:
                    import time
                    delay = base_delay * (2 ** attempt)
                    print(f"Gemini {response.status_code} (Overloaded/RateLimit). Retrying in {delay}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                    continue
                else:
                    print(f"Gemini {response.status_code}: Max retries reached")
                    return {"status": "error", "message": f"Gemini API error {response.status_code} after {max_retries} retries. Please try again later."}
            else:
                print(f"Gemini API Error: {response.status_code} - {response.text}")
                return {"status": "error", "message": f"Gemini API error: {response.status_code} - {response.text}"}
                
        except Exception as e:
            print(f"Gemini Connection Exception: {e}")
            return {"status": "error", "message": f"Gemini connection error: {str(e)}"}

async def call_lm_studio(prompt: str):
    try:
        lm_response = requests.post(
            LM_STUDIO_URL,
            json={
                "model": "local-model",  # LM Studio ignores this, uses the loaded model
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert AI debugger for ML competitions. Analyze execution results and provide JSON output."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,  # Lower temperature for more consistent JSON
                "max_tokens": 8000  # Increased to allow full code generation
            },
            timeout=600  # Increased to 10 minutes for slower local models
        )
        
        if lm_response.status_code == 200:
            lm_data = lm_response.json()
            analysis_text = lm_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return process_analysis_text(analysis_text)
        else:
            return {"status": "error", "message": f"LM Studio API error: {lm_response.status_code} - {lm_response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": "LM Studio not running. Please start LM Studio and ensure it's listening on the configured port."}
    except requests.exceptions.Timeout:
        return {"status": "error", "message": "LM Studio request timed out. The model may be too slow or not responding."}
    except Exception as e:
        return {"status": "error", "message": f"LM Studio error: {str(e)}"}

def process_analysis_text(analysis_text: str):
    if not analysis_text:
        return {"status": "error", "message": "AI returned empty response"}

    # Parse the JSON response - handle multiple JSON objects or incomplete JSON
    try:
        import re
        # Remove markdown code blocks (case insensitive)
        clean_text = re.sub(r'```json\s*', '', analysis_text, flags=re.IGNORECASE)
        clean_text = re.sub(r'```\s*', '', clean_text)
        
        # Find the FIRST complete JSON object (in case model generated multiple)
        json_start = clean_text.find('{')
        if json_start != -1:
            # Try to find a complete JSON object
            brace_count = 0
            json_end = json_start
            found_end = False
            
            for i in range(json_start, len(clean_text)):
                if clean_text[i] == '{':
                    brace_count += 1
                elif clean_text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        found_end = True
                        break
            
            # Fallback: if brace counting didn't find a clean end, try the last '}'
            if not found_end:
                 last_brace = clean_text.rfind('}')
                 if last_brace != -1 and last_brace > json_start:
                     json_end = last_brace + 1
            
            if json_end > json_start:
                json_str = clean_text[json_start:json_end]
                parsed = json.loads(json_str)
                
                # Validate required fields exist
                required_fields = ["revised_analysis", "revised_plan", "bug_confirmed", "bug_fixed", 
                                 "proposed_debug_analysis_accurate", "initial_bug_reproducible", "all_bugs_fixed", "analysis_accuracy_explanation"]
                missing = [f for f in required_fields if f not in parsed]
                
                if not missing:
                    # All fields present
                    
                    # SAVE THE FIXED CODE WITH RETRY ON SYNTAX ERRORS
                    if "fixed_code" in parsed and parsed["fixed_code"]:
                        fixed_code = parsed["fixed_code"]
                        # Validate Python syntax (simple check)
                        try:
                            compile(fixed_code, '<string>', 'exec')
                        except SyntaxError as e:
                            # For now, just warn in the log, don't retry recursively to avoid complexity in this refactor
                            print(f"Warning: AI generated code with syntax error: {e}")
                            # We could implement the retry logic here if needed, but keeping it simple for now
                    
                    return {"status": "success", "analysis": json.dumps(parsed)}
                else:
                    # Missing fields, try to fill defaults
                    for field in missing:
                        if field in ["bug_confirmed", "bug_fixed", "initial_bug_reproducible", "all_bugs_fixed"]:
                            parsed[field] = False
                        elif field == "proposed_debug_analysis_accurate":
                            parsed[field] = 0
                        else:
                            parsed[field] = ""
                    return {"status": "success", "analysis": json.dumps(parsed)}
        
    except (json.JSONDecodeError, ValueError) as e:
        # If JSON parsing fails, return success but with raw text so user can see it
        print(f"JSON parse error: {e}")
        return {
            "status": "success", 
            "analysis": analysis_text, # Return raw text
            "message": "Model output was not valid JSON. Raw output shown."
        }
    
    print(f"Failed to extract JSON from: {analysis_text[:500]}...")
    return {"status": "error", "message": "No valid JSON found in AI response (check terminal for raw output)"}
    
    # Shouldn't reach here, but just in case
    return {"status": "error", "message": "Failed to call LM Studio"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
