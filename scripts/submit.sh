#!/bin/bash
# helper to submit jobs, pretty straightforward

SERVER_URL="https://ceriferous-hoelike-jeffie.ngrok-free.dev"
SUBMISSIONS_DIR="../submissions"

# check config exists
if [ ! -f "$SUBMISSIONS_DIR/config.yaml" ]; then
    echo "error: config.yaml not found in $SUBMISSIONS_DIR"
    exit 1
fi

# check solution exists
if [ ! -f "$SUBMISSIONS_DIR/solution.py" ]; then
    echo "error: solution.py not found in $SUBMISSIONS_DIR"
    exit 1
fi

# submit it (async by default)
echo "submitting..."
cd "$SUBMISSIONS_DIR"
curl -X POST "$SERVER_URL/api/submit?wait=false" \
  -F "code=@solution.py" \
  -F "config_file=@config.yaml" | tee ../results/last_submission.json

echo ""
echo "done! check results/last_submission.json for job_id"
