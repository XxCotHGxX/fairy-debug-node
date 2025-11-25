#!/usr/bin/env python3
"""
Script to cancel all running GPU jobs for the current user.
Lists all jobs and cancels those that are still running.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "https://ceriferous-hoelike-jeffie.ngrok-free.dev")
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("Error: TOKEN not set in .env file")
    exit(1)

headers = {"Authorization": f"Bearer {TOKEN}"}

# Get all jobs
print("Fetching all jobs...")
try:
    response = requests.get(f"{SERVER_URL}/api/jobs", headers=headers)
    response.raise_for_status()
    data = response.json()
    
    jobs = data.get("jobs", [])
    print(f"Found {len(jobs)} total jobs\n")
    
    # Filter running jobs
    running_jobs = [job for job in jobs if job.get("status") in ["pending", "running"]]
    
    if not running_jobs:
        print("No running jobs found!")
        exit(0)
    
    print(f"Found {len(running_jobs)} running/pending jobs:\n")
    for job in running_jobs:
        print(f"  Job ID: {job.get('job_id')}")
        print(f"  Status: {job.get('status')}")
        print(f"  Created: {job.get('created_at', 'N/A')}")
        print()
    
    # Cancel all running jobs automatically
    print(f"\nCancelling {len(running_jobs)} job(s)...")
    
    # Cancel all running jobs
    print("\nCancelling jobs...")
    cancelled_count = 0
    for job in running_jobs:
        job_id = job.get("job_id")
        print(f"Cancelling {job_id}...", end=" ")
        
        try:
            cancel_response = requests.post(
                f"{SERVER_URL}/api/cancel/{job_id}",
                headers=headers
            )
            cancel_response.raise_for_status()
            result = cancel_response.json()
            
            if result.get("status") == "cancelled":
                print("Success")
                cancelled_count += 1
            else:
                print(f"Failed: {result}")
        except Exception as e:
            print(f"Error: {e}")
    
    print(f"\nCancelled {cancelled_count}/{len(running_jobs)} jobs")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    exit(1)

