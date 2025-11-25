#!/bin/bash

# GPU Cluster Submission Script
# Submits Python files to the GPU cluster API and saves results locally

# Helper function to parse JSON (replaces jq for Windows compatibility)
json_get() {
    python3 -c "import sys, json; data=json.load(sys.stdin); val=data.get('$1', ''); print(val if val is not None else '')" 2>/dev/null || python -c "import sys, json; data=json.load(sys.stdin); val=data.get('$1', ''); print(val if val is not None else '')" 2>/dev/null
}

# Helper function to process log: extract stdout from API response, parse as JSON, and truncate inner stdout
process_log() {
    script="
import sys, json

try:
    # Read API response (Wrapper)
    input_str = sys.stdin.read()
    if not input_str.strip():
        sys.exit(0) # Empty input
        
    wrapper = json.loads(input_str)
    wrapper_stdout = wrapper.get('stdout', [])
    
    # wrapper_stdout is likely a list of strings (lines) or a single string
    if isinstance(wrapper_stdout, list):
        log_text = ''.join(wrapper_stdout)
    else:
        log_text = str(wrapper_stdout)
        
    # Try to parse the log text as JSON (Format A)
    try:
        data = json.loads(log_text)
        
        # It is JSON. Now truncate/normalize its 'stdout' field
        stdout = data.get('stdout', [])
        
        # Normalize stdout: split by newline to create separate lines
        normalized_stdout = []
        for item in stdout:
            if isinstance(item, str):
                # Split lines so they appear as separate array elements (readable)
                # This removes \n characters and starts new lines in the array
                normalized_stdout.extend(item.splitlines())
            else:
                normalized_stdout.append(str(item))
        
        # Calculate base size (without stdout) to know how much space we have
        base_data = {k: v for k, v in data.items() if k != 'stdout'}
        base_str = json.dumps(base_data, ensure_ascii=False, indent=2)
        base_size = len(base_str)
        
        # Max file size 50000
        # Reserve space for overhead and base JSON
        limit = 50000
        available_for_stdout = limit - base_size - 500 # 500 buffer
        
        if available_for_stdout < 1000:
            available_for_stdout = 1000 # Minimum
            
        # Truncate from END (keep start)
        final_stdout = []
        current_size = 0
        
        for line in normalized_stdout:
            # Estimate size contribution: line + quotes + comma + indent (approx len + 10)
            line_size = len(line) + 10 
            
            if current_size + line_size > available_for_stdout:
                final_stdout.append(f'...[TRUNCATED to fit {limit} char limit]...')
                break
            
            final_stdout.append(line)
            current_size += line_size
            
        data['stdout'] = final_stdout
        
        # Output readable JSON
        print(json.dumps(data, ensure_ascii=False, indent=2))
        
    except json.JSONDecodeError:
        # Not JSON. Just truncate the text.
        if len(log_text) > 50000:
            # Cut at nearest newline before 50000
            truncated = log_text[:50000]
            last_newline = truncated.rfind('\n')
            if last_newline != -1:
                print(truncated[:last_newline])
            else:
                print(truncated)
            print('\n...[LOG TRUNCATED]...')
        else:
            print(log_text)
            
except Exception as e:
    sys.stderr.write(f'Error processing log: {e}\n')
    # Fallback: try to print something
    if 'input_str' in locals():
        print(input_str[:50000])
"
    python3 -c "$script" 2>/dev/null || python -c "$script" 2>/dev/null
}

# Configuration
CODE_DIR="./code"
LOG_BASE_DIR="./logs"
SERVER_URL="https://ceriferous-hoelike-jeffie.ngrok-free.dev"
USER_ID="your_user"
EXPECTED_TIME=300
TEMP_DIR=$(mktemp -d)

# Load USER_ID and TOKEN from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -E '^(USER_ID|TOKEN)=' | grep -v '^#' | xargs)
fi

# Set defaults if not loaded from .env
USER_ID="${USER_ID:-your_user}"

# Parse command line arguments
FORCE_REGRADE=false
if [[ "$1" == "--force" ]]; then
    FORCE_REGRADE=true
    echo "Force mode: Will re-submit all files, even if logs exist"
fi

# Check for TOKEN (from .env or environment variable)
if [[ -z "$TOKEN" ]]; then
    echo "Error: TOKEN not set (check .env file or set TOKEN environment variable)"
    echo "Usage: TOKEN=\"your_token_here\" $0 [--force]"
    exit 1
fi

# Use TOKEN as GPU_TOKEN internally for compatibility
GPU_TOKEN="$TOKEN"

# Check if code directory exists
if [ ! -d "$CODE_DIR" ]; then
    echo "Error: Code directory $CODE_DIR does not exist"
    exit 1
fi

# Ensure log base directory exists
mkdir -p "$LOG_BASE_DIR"

# Counters for summary
total_files=0
skipped_files=0
submitted_files=0
failed_files=0

# Track current job for interrupt handling
current_job_id=""
current_log_file=""

# Cleanup function
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Interrupt handler for Ctrl+C
interrupt_handler() {
    echo ""
    echo "========================================="
    echo "Interrupt signal received (Ctrl+C)"

    if [[ -n "$current_job_id" ]]; then
        echo "Current job ID: $current_job_id"
        echo ""
        echo "The remote job is still running on the GPU cluster."
        echo "What would you like to do?"
        echo ""
        read -p "Cancel the remote job? (y/n): " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Cancelling remote job $current_job_id..."
            cancel_response=$(curl -s -X POST -H "Authorization: Bearer $GPU_TOKEN" \
                "$SERVER_URL/api/cancel/$current_job_id")
            echo "Response: $cancel_response"
        else
            echo "Remote job will continue running."
            echo ""
            echo "To check status later, run:"
            echo "  GPU_TOKEN=\"your_token\" ./check_job.sh $current_job_id"
            echo ""
            echo "To get results when complete, run:"
            echo "  GPU_TOKEN=\"your_token\" ./check_job.sh $current_job_id $current_log_file"
            echo ""
            echo "Or manually:"
            echo "  curl -H \"Authorization: Bearer \$GPU_TOKEN\" \\"
            echo "    \"$SERVER_URL/api/status/$current_job_id\""
        fi
    fi

    echo ""
    echo "Script terminated."
    cleanup
    exit 130
}
trap interrupt_handler SIGINT

echo "Starting GPU cluster submissions..."
echo "Server: $SERVER_URL"
echo "User: $USER_ID"
echo "Expected runtime per job: ${EXPECTED_TIME}s"
echo ""

# Find all Python files matching the pattern and process them
for file in "$CODE_DIR"/*_*_*.py; do
    # Skip if no files match the pattern
    [ -e "$file" ] || continue

    total_files=$((total_files + 1))

    # Extract filename without path
    basename=$(basename "$file" .py)

    # Parse the filename: competition-name_id_number
    # This regex handles competition names with hyphens
    if [[ $basename =~ ^(.+)_([^_]+)_([^_]+)$ ]]; then
        competition_name="${BASH_REMATCH[1]}"
        id="${BASH_REMATCH[2]}"
        number="${BASH_REMATCH[3]}"

        # Create log directory for this ID if it doesn't exist
        log_dir="$LOG_BASE_DIR/$id"
        mkdir -p "$log_dir"

        # Construct log file path
        log_file="$log_dir/${number}.jsonl"
        current_log_file="$log_file"  # Track for interrupt handler

        # Check if log file already exists and skip if not forcing
        # Check both .jsonl (completed) and .raw.log (in progress/completed) files
        raw_log_file="$log_dir/${number}.raw.log"
        if [[ "$FORCE_REGRADE" == false ]]; then
            # If .jsonl exists, definitely skip (job completed)
            if [[ -f "$log_file" ]]; then
                echo "Skipping: $file (already completed - log exists at $log_file)"
                skipped_files=$((skipped_files + 1))
                continue
            fi
            
            # If .raw.log exists, check if it indicates completion/cancellation
            if [[ -f "$raw_log_file" ]]; then
                # Check file size - if it's very small (<100 bytes), might be incomplete
                file_size=$(stat -f%z "$raw_log_file" 2>/dev/null || stat -c%s "$raw_log_file" 2>/dev/null || echo "0")
                
                # If raw log has meaningful content, check for completion indicators
                if [[ $file_size -gt 100 ]]; then
                    # Check for completion/cancellation indicators in raw log
                    if grep -qiE "Job (completed|cancelled|failed)|Job ID:|Monitoring job status|no_repro|ERROR:|Results saved" "$raw_log_file" 2>/dev/null; then
                        echo "Skipping: $file (already processed - raw log exists at $raw_log_file)"
                        skipped_files=$((skipped_files + 1))
                        continue
                    fi
                fi
                # If raw log exists but is incomplete/small, we might want to retry - don't skip
            fi
        fi

        echo "========================================="
        echo "Processing: $file"
        echo "  Competition: $competition_name"
        echo "  Project ID: $id"
        echo "  Number: $number"
        echo "  Log: $log_file"

        # Create temporary solution.py (copy of the original file)
        cp "$file" "$TEMP_DIR/solution.py"

        # Create temporary config.yaml
        cat > "$TEMP_DIR/config.yaml" <<EOF
competition_id: "$competition_name"
project_id: "$id"
user_id: "$USER_ID"
expected_time: $EXPECTED_TIME
timeout: 0.1
token: "$GPU_TOKEN"
EOF

        # Submit the job (async mode for long-running jobs)
        echo "Submitting job..."
        submit_response=$(curl -s -X POST "$SERVER_URL/api/submit?wait=false" \
            -F "code=@$TEMP_DIR/solution.py" \
            -F "config_file=@$TEMP_DIR/config.yaml")

        # Extract job_id from response
        job_id=$(echo "$submit_response" | json_get 'job_id')
        current_job_id="$job_id"  # Track for interrupt handler

        if [[ -z "$job_id" ]] || [[ "$job_id" == "null" ]]; then
            echo "ERROR: Failed to submit job"
            echo "Response: $submit_response"
            failed_files=$((failed_files + 1))
            current_job_id=""  # Clear since job failed
            echo "---"
            continue
        fi

        echo "Job submitted! Job ID: $job_id"
        echo "Monitoring job status (will auto-cancel after 6 minutes if still running)..."

        # Poll for job completion with 6-minute auto-cancel
        max_attempts=360  # 1 hour max (10s intervals)
        cancel_timeout=36  # 6 minutes = 36 * 10s intervals
        attempt=0
        running_start_time=""
        job_cancelled_by_script=false
        
        while [ $attempt -lt $max_attempts ]; do
            status_response=$(curl -s -H "Authorization: Bearer $GPU_TOKEN" \
                "$SERVER_URL/api/status/$job_id")

            status=$(echo "$status_response" | json_get 'status')

            # Track when job starts running
            if [[ "$status" == "running" ]] && [[ -z "$running_start_time" ]]; then
                running_start_time=$attempt
                echo "  Job started running at $(date)"
            fi

            if [[ "$status" == "completed" ]]; then
                echo "Job completed successfully!"
                break
            elif [[ "$status" == "failed" ]]; then
                echo "ERROR: Job failed"
                failed_files=$((failed_files + 1))
                break
            elif [[ "$status" == "cancelled" ]]; then
                if [[ "$job_cancelled_by_script" == "true" ]]; then
                    # This case shouldn't happen as we break before this, but handle it just in case
                    echo "Job cancelled by script after 6 minutes (No Repro)"
                    skipped_files=$((skipped_files + 1))
                else
                    echo "WARNING: Job was cancelled externally"
                    failed_files=$((failed_files + 1))
                fi
                break
            fi

            # Auto-cancel after 6 minutes if still running
            if [[ "$status" == "running" ]] && [[ -n "$running_start_time" ]]; then
                running_duration=$((attempt - running_start_time))
                if [[ $running_duration -ge $cancel_timeout ]]; then
                    echo ""
                    echo "⏱ Job has been running for 6+ minutes. Auto-cancelling..."
                    cancel_response=$(curl -s -X POST -H "Authorization: Bearer $GPU_TOKEN" \
                        "$SERVER_URL/api/cancel/$job_id")
                    
                    # Verify cancellation
                    sleep 2
                    verify_response=$(curl -s -H "Authorization: Bearer $GPU_TOKEN" \
                        "$SERVER_URL/api/status/$job_id")
                    verify_status=$(echo "$verify_response" | json_get 'status')
                    
                    if [[ "$verify_status" == "cancelled" ]]; then
                        echo "✓ Job cancelled successfully. Moving to next file..."
                        job_cancelled_by_script=true
                        status="cancelled"  # Update status for consistency
                        # Create a "No Repro" log entry
                        echo "{\"status\": \"no_repro\", \"message\": \"Job ran for 6+ minutes without error. Auto-cancelled by script.\", \"exec_time\": 360}" > "$log_file"
                        skipped_files=$((skipped_files + 1))
                        break
                    else
                        echo "⚠ Warning: Cancellation sent but status is: $verify_status"
                        failed_files=$((failed_files + 1))
                        break
                    fi
                else
                    elapsed_minutes=$((running_duration * 10 / 60))
                    echo "  Status: Running on GPU... (${elapsed_minutes}m elapsed, will cancel at 6m)"
                fi
            elif [[ "$status" == "pending" ]]; then
                queue_pos=$(echo "$status_response" | json_get 'queue_position')
                echo "  Status: Pending (Queue position: $queue_pos)"
            fi

            sleep 10
            attempt=$((attempt + 1))
        done

        if [ $attempt -ge $max_attempts ]; then
            echo "ERROR: Job monitoring timeout (1 hour)"
            failed_files=$((failed_files + 1))
            echo "---"
            continue
        fi

        # Skip results retrieval if job was auto-cancelled (already created log)
        if [[ "$job_cancelled_by_script" == "true" ]]; then
            echo "---"
            continue
        fi

        # Get results if job completed
        if [[ "$status" == "completed" ]]; then
            echo "Retrieving results..."
            results_response=$(curl -s -H "Authorization: Bearer $GPU_TOKEN" \
                "$SERVER_URL/api/results/$job_id")

            # Save extracted results with stdout truncation
            echo "Processing log..."
            processed_response=$(echo "$results_response" | process_log)
            
            # Fallback if processing failed/returned empty
            if [[ -z "$processed_response" ]]; then
                echo "Warning: Log processing returned empty. Saving raw results response."
                # Fallback: extract stdout using json_get (simple) to ensure we save something
                echo "$results_response" | json_get 'stdout' > "$log_file"
            else
                echo "$processed_response" > "$log_file"
            fi
            
            echo "✓ Results saved to $log_file"

            # Check exit code
            exit_code=$(echo "$results_response" | json_get 'exit_code')

            if [[ "$exit_code" == "0" ]]; then
                echo "✓ Results saved to $log_file"
                submitted_files=$((submitted_files + 1))
            else
                echo "WARNING: Job completed with non-zero exit code: $exit_code"
                stderr=$(echo "$results_response" | json_get 'stderr')
                echo "Error output: $stderr"
                
                # Ensure we save the error to the log file if it's empty
                if [ ! -s "$log_file" ] || [ "$(cat "$log_file")" == "null" ]; then
                    echo "{\"error\": \"failed\", \"exit_code\": $exit_code, \"stderr\": \"$stderr\"}" > "$log_file"
                fi
                
                failed_files=$((failed_files + 1))
            fi
        # NEW: Handle failed jobs (e.g., timeouts) by writing a summary log
        elif [[ "$status" == "failed" ]]; then
            echo "Retrieving failure information..."
            results_response=$(curl -s -H "Authorization: Bearer $GPU_TOKEN" \
                "$SERVER_URL/api/results/$job_id")

            exit_code=$(echo "$results_response" | json_get 'exit_code')
            stderr=$(echo "$results_response" | json_get 'stderr')
            timeout_duration=$((EXPECTED_TIME * 2 / 60))  # Convert to minutes

            # Check if it's a timeout (exit code 143 = SIGTERM, or 137 = SIGKILL)
            if [[ "$exit_code" == "143" ]] || [[ "$exit_code" == "137" ]] || [[ "$stderr" == *"timeout"* ]] || [[ "$stderr" == *"killed"* ]]; then
                echo "{\"error\": \"timeout\", \"message\": \"Code ran for approximately ${timeout_duration} minutes without completing (timeout at 2x expected_time)\", \"exit_code\": $exit_code}" > "$log_file"
                echo "⚠ Timeout detected - summary saved to $log_file"
            else
                # Other failure - save stderr
                echo "{\"error\": \"failed\", \"message\": \"Job failed with exit code $exit_code\", \"stderr\": \"$stderr\"}" > "$log_file"
                echo "⚠ Failure logged to $log_file"
            fi

            if [[ -n "$stderr" ]] && [[ "$stderr" != "null" ]]; then
                echo "Error output: $stderr"
            fi
        fi

        # Clean up temp files for this iteration
        rm -f "$TEMP_DIR/solution.py" "$TEMP_DIR/config.yaml"

        # Clear current job tracking
        current_job_id=""
        current_log_file=""

        echo "---"
    else
        echo "Warning: Skipping $file - doesn't match expected pattern"
    fi
done

echo ""
echo "========================================="
echo "===== Submission Summary ====="
echo "Total files found: $total_files"
echo "Files submitted successfully: $submitted_files"
echo "Files failed: $failed_files"
echo "Files skipped (already done): $skipped_files"
echo "All submissions complete!"
