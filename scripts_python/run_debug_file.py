#!/usr/bin/env python3
# run a debug file - extracts competition_id and datarow_id from filename
# filename format: <datarow_id>_<competition_id>_<debugstep>.py
# usage: python run_debug_file.py <filename> [--expected-time SECONDS]

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from api_run import submit_job

def extract_parts(filename):
    # filename format: <datarow_id>_<competition_id>_<debugstep>.py
    stem = Path(filename).stem  # removes .py
    parts = stem.split('_')
    
    datarow_id = parts[0] if len(parts) >= 1 else None
    competition_id = parts[1] if len(parts) >= 2 else None
    debug_step = parts[2] if len(parts) >= 3 else None
    
    return datarow_id, competition_id, debug_step

def main():
    parser = argparse.ArgumentParser(
        description="run a debug file, extracts competition_id and datarow_id from filename"
    )
    
    parser.add_argument('filename', help='path to python file (e.g. 5076549aae3a4_random-acts-of-pizza_0.py)')
    parser.add_argument('--project-id', help='project id (defaults to datarow_id from filename)')
    parser.add_argument('--expected-time', type=int, default=600,
                       help='runtime in seconds (default: 600)')
    parser.add_argument('--wait', action='store_true',
                       help='wait for completion')
    
    args = parser.parse_args()
    
    # extract parts from filename
    datarow_id, competition_id, debug_step = extract_parts(args.filename)
    
    if not competition_id:
        print("ERROR: cant extract competition_id from filename")
        print("filename should be: <datarow_id>_<competition_id>_<debugstep>.py")
        sys.exit(1)
    
    # use project_id from arg, or datarow_id from filename, or fallback
    project_id = args.project_id or datarow_id or Path(args.filename).stem
    
    print(f"running file: {args.filename}")
    print(f"  competition: {competition_id}")
    print(f"  project: {project_id}")
    if datarow_id:
        print(f"  datarow id: {datarow_id}")
    if debug_step:
        print(f"  debug step: {debug_step}")
    print()
    
    submit_job(
        competition_id=competition_id,
        code_file=args.filename,
        expected_time=args.expected_time,
        wait=args.wait,
        project_id=project_id
    )

if __name__ == "__main__":
    main()
