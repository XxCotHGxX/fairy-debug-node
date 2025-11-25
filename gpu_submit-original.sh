#!/bin/bash

# Helper function to parse JSON (replaces jq for Windows compatibility)
json_get() {
    python3 -c "import sys, json; data=json.load(sys.stdin); val=data.get('$1', ''); print(val if val is not None else '')" 2>/dev/null || python -c "import sys, json; data=json.load(sys.stdin); val=data.get('$1', ''); print(val if val is not None else '')" 2>/dev/null
}

# Load configuration from .env file if available
if [[ -f .env ]]; then
    export $(grep -v '^#' .env | xargs)
fi

# GPU Cluster Batch Submission Script
# Submits up to 2 jobs in parallel to the GPU cluster API

# Configuration
CODE_DIR="./code"
LOG_BASE_DIR="./logs"
SERVER_URL="https://ceriferous-hoelike-jeffie.ngrok-free.dev"
USER_ID="${USER_ID:-user_name}" # Load from env or default
EXPECTED_TIME=600
MAX_PARALLEL=1
TEMP_DIR=$(mktemp -d)

# Parse command line arguments
FORCE_REGRADE=false
if [[ "$1" == "--force" ]]; then
    FORCE_REGRADE=true
    echo "Force mode: Will re-submit all files, even if logs exist"
fi

# Check for GPU_TOKEN environment variable (from env or .env)
# Support both TOKEN and GPU_TOKEN
if [[ -n "$TOKEN" ]] && [[ -z "$GPU_TOKEN" ]]; then
    GPU_TOKEN="$TOKEN"
fi

if [[ -z "$GPU_TOKEN" ]]; then
    echo "Error: GPU_TOKEN environment variable not set (and not found in .env)"
    echo "Usage: GPU_TOKEN=\"your_token_here\" $0 [--force]"
    exit 1
fi

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

    if [[ ${#active_jobs[@]} -gt 0 ]]; then
        echo ""
        echo "Active jobs (${#active_jobs[@]}):"
        for job_id in "${!active_jobs[@]}"; do
            local idx="${active_jobs[$job_id]}"
            local file="${queue_files[$idx]}"
            echo "  - Job ID: $job_id (File: $(basename "$file"))"
        done

        echo ""
        echo "These jobs are still running on the GPU cluster."
        echo "What would you like to do?"
        echo ""
        read -p "Cancel all remote jobs? (y/n): " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Cancelling all remote jobs..."
            for job_id in "${!active_jobs[@]}"; do
                echo "  Cancelling job $job_id..."
                cancel_response=$(curl -s -X POST -H "Authorization: Bearer $GPU_TOKEN" \
                    "$SERVER_URL/api/cancel/$job_id")
                echo "    Response: $(echo "$cancel_response" | json_get 'message')"
            done
            echo "All jobs cancelled."
        else
            echo "Remote jobs will continue running."
            echo ""
            echo "To check status later, use:"
            for job_id in "${!active_jobs[@]}"; do
                echo "  curl -H \"Authorization: Bearer \$GPU_TOKEN\" \\"
                echo "    \"$SERVER_URL/api/status/$job_id\""
            done
            echo ""
            echo "Or list all your jobs:"
            echo "  curl -H \"Authorization: Bearer \$GPU_TOKEN\" \\"
            echo "    \"$SERVER_URL/api/jobs\""
        fi
    fi

    echo ""
    echo "Script terminated."
    cleanup
    exit 130
}
trap interrupt_handler SIGINT

echo "Starting GPU cluster batch submissions (max $MAX_PARALLEL parallel jobs)..."
echo "Server: $SERVER_URL"
echo "User: $USER_ID"
echo "Expected runtime per job: ${EXPECTED_TIME}s"
echo ""

# Build queue of files to process
declare -a queue_files
declare -a queue_competitions
declare -a queue_ids
declare -a queue_numbers
declare -a queue_logfiles

for file in "$CODE_DIR"/*_*_*.py; do
    # Skip if no files match the pattern
    [ -e "$file" ] || continue

    total_files=$((total_files + 1))

    # Extract filename without path
    basename=$(basename "$file" .py)

    # Parse the filename: competition-name_id_number
    if [[ $basename =~ ^(.+)_([^_]+)_([^_]+)$ ]]; then
        competition_name="${BASH_REMATCH[1]}"
        id="${BASH_REMATCH[2]}"
        number="${BASH_REMATCH[3]}"

        # Create log directory for this ID if it doesn't exist
        log_dir="$LOG_BASE_DIR/$id"
        mkdir -p "$log_dir"

        # Construct log file path
        log_file="$log_dir/${number}.jsonl"

        # Check if log file already exists and skip if not forcing
        if [[ -f "$log_file" ]] && [[ "$FORCE_REGRADE" == false ]]; then
            echo "Skipping: $file (already submitted - log exists at $log_file)"
            skipped_files=$((skipped_files + 1))
            continue
        fi

        # Add to queue
        queue_files+=("$file")
        queue_competitions+=("$competition_name")
        queue_ids+=("$id")
        queue_numbers+=("$number")
        queue_logfiles+=("$log_file")
    else
        echo "Warning: Skipping $file - doesn't match expected pattern"
    fi
done

queue_size=${#queue_files[@]}
echo "Queue size: $queue_size files to process"
echo ""

if [[ $queue_size -eq 0 ]]; then
    echo "No files to process!"
    echo ""
    echo "========================================="
    echo "===== Submission Summary ====="
    echo "Total files found: $total_files"
    echo "Files submitted successfully: $submitted_files"
    echo "Files failed: $failed_files"
    echo "Files skipped (already done): $skipped_files"
    echo "All submissions complete!"
    exit 0
fi

# Track active jobs (job_id -> queue_index)
declare -A active_jobs
queue_index=0

# Function to submit a job from the queue
submit_job() {
    local idx=$1
    local file="${queue_files[$idx]}"
    local competition_name="${queue_competitions[$idx]}"
    local id="${queue_ids[$idx]}"
    local number="${queue_numbers[$idx]}"
    local log_file="${queue_logfiles[$idx]}"

    echo "========================================="
    echo "Processing: $file"
    echo "  Competition: $competition_name"
    echo "  Project ID: $id"
    echo "  Number: $number"
    echo "  Log: $log_file"

    # Create temporary solution.py (use unique name for parallel jobs)
    local temp_solution="$TEMP_DIR/solution_${idx}.py"
    local temp_config="$TEMP_DIR/config_${idx}.yaml"

    cp "$file" "$temp_solution"

    # Create temporary config.yaml
    cat > "$temp_config" <<EOF
competition_id: "$competition_name"
project_id: "$id"
user_id: "$USER_ID"
expected_time: $EXPECTED_TIME
timeout: 0.17
token: "$GPU_TOKEN"
EOF

    # Submit the job (async mode)
    echo "Submitting job..."
    submit_response=$(curl -s -X POST "$SERVER_URL/api/submit?wait=false" \
        -F "code=@$temp_solution" \
        -F "config_file=@$temp_config")

    # Extract job_id from response
    job_id=$(echo "$submit_response" | json_get 'job_id')

    if [[ -z "$job_id" ]] || [[ "$job_id" == "null" ]]; then
        echo "ERROR: Failed to submit job"
        echo "Response: $submit_response"
        failed_files=$((failed_files + 1))
        return 1
    fi

    echo "Job submitted! Job ID: $job_id"
    active_jobs["$job_id"]=$idx

    # Clean up temp files for this submission
    rm -f "$temp_solution" "$temp_config"

    return 0
}

# Function to check and handle completed jobs
check_jobs() {
    local -a completed_jobs=()

    for job_id in "${!active_jobs[@]}"; do
        local idx="${active_jobs[$job_id]}"
        local log_file="${queue_logfiles[$idx]}"
        local file="${queue_files[$idx]}"

        # Check job status
        status_response=$(curl -s -H "Authorization: Bearer $GPU_TOKEN" \
            "$SERVER_URL/api/status/$job_id")

        status=$(echo "$status_response" | json_get 'status')

        if [[ "$status" == "completed" ]] || [[ "$status" == "failed" ]] || [[ "$status" == "cancelled" ]]; then
            echo ""
            echo "Job $job_id finished with status: $status"
            echo "File: $file"

            # Get results
            echo "Job finished - waiting 5s for server to finalize results..."
            sleep 5
            echo "Retrieving results..."
            results_response=$(curl -s -H "Authorization: Bearer $GPU_TOKEN" \
                "$SERVER_URL/api/results/$job_id")

            # Extract stdout and save to log file
            echo "$results_response" | json_get 'stdout' > "$log_file"

            # Check exit code
            exit_code=$(echo "$results_response" | json_get 'exit_code')

            if [[ "$exit_code" == "0" ]]; then
                echo "✓ Results saved to $log_file"
                submitted_files=$((submitted_files + 1))
            else
                echo "⚠ Job failed/timed out - results saved to $log_file"
                stderr=$(echo "$results_response" | json_get 'stderr')
                if [[ -n "$stderr" ]] && [[ "$stderr" != "null" ]] && [[ "$stderr" != "" ]]; then
                    echo "Error output: $stderr"
                fi
                failed_files=$((failed_files + 1))
            fi

            # Mark for removal from active jobs
            completed_jobs+=("$job_id")
        fi
    done

    # Remove completed jobs from active list
    for job_id in "${completed_jobs[@]}"; do
        unset active_jobs["$job_id"]
    done

    return ${#completed_jobs[@]}
}

# Submit initial batch of jobs
echo "Submitting initial batch of jobs..."
while [[ $queue_index -lt $queue_size ]] && [[ ${#active_jobs[@]} -lt $MAX_PARALLEL ]]; do
    echo "Submitting job $((queue_index + 1))/$queue_size..."
    submit_job $queue_index
    ((queue_index++))
    echo "Active jobs now: ${#active_jobs[@]}"
done

echo ""
echo "Initial batch submitted: ${#active_jobs[@]} active jobs"
echo "Monitoring jobs..."
echo ""

# Main loop: monitor jobs and submit new ones as slots open up
max_monitoring_attempts=2880  # 8 hour max per monitoring cycle
monitoring_attempt=0

while [[ ${#active_jobs[@]} -gt 0 ]] || [[ $queue_index -lt $queue_size ]]; do
    # Check if any jobs have completed
    check_jobs
    jobs_completed=$?

    # If jobs completed and queue has more, submit new jobs
    if [[ $jobs_completed -gt 0 ]] && [[ $queue_index -lt $queue_size ]]; then
        echo ""
        echo "Jobs completed, filling slots from queue..."
        while [[ $queue_index -lt $queue_size ]] && [[ ${#active_jobs[@]} -lt $MAX_PARALLEL ]]; do
            echo "Submitting job $((queue_index + 1))/$queue_size..."
            submit_job $queue_index
            ((queue_index++))
            echo "Active jobs now: ${#active_jobs[@]}"
        done
    fi

    # Show status
    if [[ ${#active_jobs[@]} -gt 0 ]]; then
        echo -ne "\r[$(date '+%H:%M:%S')] Active jobs: ${#active_jobs[@]} | Completed: $((submitted_files + failed_files))/$queue_size | Queue remaining: $((queue_size - queue_index))      "
    fi

    # Break if all done
    if [[ ${#active_jobs[@]} -eq 0 ]] && [[ $queue_index -ge $queue_size ]]; then
        break
    fi

    # Timeout check
    if [[ $monitoring_attempt -ge $max_monitoring_attempts ]]; then
        echo ""
        echo "WARNING: Monitoring timeout reached (8 hours)"
        echo "Remaining active jobs may still be running on the server"
        break
    fi

    sleep 10
    ((monitoring_attempt++))
done

echo ""
echo ""
echo "========================================="
echo "===== Submission Summary ====="
echo "Total files found: $total_files"
echo "Files submitted successfully: $submitted_files"
echo "Files failed: $failed_files"
echo "Files skipped (already done): $skipped_files"
echo "All submissions complete!"
