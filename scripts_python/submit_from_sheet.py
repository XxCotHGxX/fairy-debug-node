#!/usr/bin/env python3
# helper to submit jobs from google sheet rows
# usage: python submit_from_sheet.py <competition_id> <code_file> [--project-id PROJECT_ID]

import argparse
import os
import sys
from pathlib import Path

# import the main submit function
sys.path.insert(0, str(Path(__file__).parent))
from api_run import submit_job

def main():
    parser = argparse.ArgumentParser(
        description="submit job from sheet row data",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('competition_id', help='competition id from sheet')
    parser.add_argument('code_file', help='path to code file')
    parser.add_argument('--project-id', help='project id (if different from default)')
    parser.add_argument('--expected-time', type=int, default=600,
                       help='runtime in seconds (default: 600)')
    parser.add_argument('--wait', action='store_true',
                       help='wait for completion')
    
    args = parser.parse_args()
    
    # use project_id from arg, or try to get from env, or use competition_id as fallback
    project_id = args.project_id or os.getenv("PROJECT_ID") or args.competition_id
    
    print(f"submitting job:")
    print(f"  competition: {args.competition_id}")
    print(f"  project: {project_id}")
    print(f"  code: {args.code_file}")
    print()
    
    submit_job(
        competition_id=args.competition_id,
        code_file=args.code_file,
        expected_time=args.expected_time,
        wait=args.wait,
        project_id=project_id
    )

if __name__ == "__main__":
    main()


