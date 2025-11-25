#!/usr/bin/env python3
import argparse
import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
SERVER_URL = os.getenv("SERVER_URL", "https://ceriferous-hoelike-jeffie.ngrok-free.dev")
USER_ID = os.getenv("USER_ID", "your_username")
TOKEN = os.getenv("TOKEN", "your_secret_token_xyz")
PROJECT_ID = os.getenv("PROJECT_ID", "my-project")

TOOLS_DIR = Path(__file__).parent
TEMPLATE_PATH = TOOLS_DIR / "templates" / "debug_template.py"

def run_curl_command(args):
    """Runs a curl command and returns the output."""
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running curl: {e}")
        print(f"Stderr: {e.stderr}")
        return None

def scaffold(args):
    """Creates a new debug file from template."""
    filename = f"{args.datarow_id}_{args.competition_id}_{args.debug_step}.py"
    target_path = Path(filename)
    
    if target_path.exists():
        print(f"Error: File {filename} already exists.")
        return

    if not TEMPLATE_PATH.exists():
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        return

    shutil.copy(TEMPLATE_PATH, target_path)
    print(f"Created {filename} from template.")
    print(f"Don't forget to edit it to match the competition data!")

def submit(args):
    """Submits a job to the server."""
    code_file = Path(args.filename)
    if not code_file.exists():
        print(f"Error: File {code_file} not found.")
        return

    # Extract info from filename if possible
    # Expected format: <datarow_id>_<competition_id>_<debugstep>.py
    parts = code_file.stem.split('_')
    competition_id = parts[1] if len(parts) >= 2 else "unknown-competition"
    
    # Create temp config
    config_data = {
        "competition_id": competition_id,
        "project_id": PROJECT_ID,
        "user_id": USER_ID,
        "expected_time": args.expected_time,
        "token": TOKEN
    }
    
    config_file = Path("temp_config.yaml")
    with open(config_file, "w") as f:
        for k, v in config_data.items():
            f.write(f"{k}: \"{v}\"\n")

    print(f"Submitting {code_file} to {SERVER_URL}...")
    print(f"Competition: {competition_id}")
    
    wait_param = "true" if args.wait else "false"
    curl_args = [
        "curl", "-s", "-X", "POST",
        f"{SERVER_URL}/api/submit?wait={wait_param}",
        "-F", f"code=@{code_file}",
        "-F", f"config_file=@{config_file}"
    ]
    
    response_json = run_curl_command(curl_args)
    
    # Cleanup config
    if config_file.exists():
        config_file.unlink()
        
    if response_json:
        try:
            response = json.loads(response_json)
            print("Submission response:")
            print(json.dumps(response, indent=2))
            
            job_id = response.get("job_id")
            if job_id:
                print(f"\nJob ID: {job_id}")
                # Save to log
                log_dir = Path("logs")
                log_dir.mkdir(exist_ok=True)
                log_file = log_dir / f"{code_file.stem}_response.json"
                with open(log_file, "w") as f:
                    json.dump(response, f, indent=2)
                print(f"Response saved to {log_file}")
        except json.JSONDecodeError:
            print("Error decoding response JSON:")
            print(response_json)

def check(args):
    """Checks job status."""
    job_id = args.job_id
    print(f"Checking status for Job ID: {job_id}...")
    
    curl_args = [
        "curl", "-s",
        "-H", f"Authorization: Bearer {TOKEN}",
        f"{SERVER_URL}/api/status/{job_id}"
    ]
    
    response_json = run_curl_command(curl_args)
    if response_json:
        try:
            response = json.loads(response_json)
            print(json.dumps(response, indent=2))
        except json.JSONDecodeError:
            print(response_json)

def main():
    parser = argparse.ArgumentParser(description="Fairy Debugger CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Scaffold command
    scaffold_parser = subparsers.add_parser("scaffold", help="Create a new debug file")
    scaffold_parser.add_argument("competition_id", help="Competition ID")
    scaffold_parser.add_argument("datarow_id", help="Data Row ID")
    scaffold_parser.add_argument("debug_step", help="Debug Step (e.g. 0)")
    
    # Submit command
    submit_parser = subparsers.add_parser("submit", help="Submit a debug file")
    submit_parser.add_argument("filename", help="Path to the python file")
    submit_parser.add_argument("--expected-time", type=int, default=600, help="Expected runtime in seconds")
    submit_parser.add_argument("--wait", action="store_true", help="Wait for completion")
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check job status")
    check_parser.add_argument("job_id", help="Job ID")
    
    args = parser.parse_args()
    
    if args.command == "scaffold":
        scaffold(args)
    elif args.command == "submit":
        submit(args)
    elif args.command == "check":
        check(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
