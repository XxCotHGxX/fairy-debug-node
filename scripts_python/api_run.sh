#!/bin/bash
# wrapper script to submit jobs to gpu cluster
# usage: ./api_run.sh <competition_id> <code_file> [expected_time] [--wait]

set -e

# config - set these env vars or change defaults here
SERVER_URL="${SERVER_URL:-https://ceriferous-hoelike-jeffie.ngrok-free.dev}"
USER_ID="${USER_ID:-your_username}"
TOKEN="${TOKEN:-your_secret_token_xyz}"
PROJECT_ID="${PROJECT_ID:-my-project}"

# check args
if [ $# -lt 2 ]; then
    echo "usage: $0 <competition_id> <code_file> [expected_time] [--wait]"
    echo ""
    echo "examples:"
    echo "  $0 random-acts-of-pizza solution.py"
    echo "  $0 random-acts-of-pizza solution.py 600"
    echo "  $0 random-acts-of-pizza solution.py 600 --wait"
    echo ""
    echo "env vars:"
    echo "  USER_ID - username (default: your_username)"
    echo "  TOKEN - secret token (default: your_secret_token_xyz)"
    echo "  PROJECT_ID - project id (default: my-project)"
    exit 1
fi

COMPETITION_ID=$1
CODE_FILE=$2
EXPECTED_TIME=${3:-600}
WAIT_FLAG=${4:-false}

# validate creds
if [ "$USER_ID" = "your_username" ] || [ "$TOKEN" = "your_secret_token_xyz" ]; then
    echo "ERROR: need to set USER_ID and TOKEN env vars"
    echo "like:"
    echo "  export USER_ID='your_username'"
    echo "  export TOKEN='your_secret_token_xyz'"
    exit 1
fi

# check file exists
if [ ! -f "$CODE_FILE" ]; then
    echo "ERROR: file not found: $CODE_FILE"
    exit 1
fi

# make temp config file
CONFIG_FILE=$(mktemp)
cat > "$CONFIG_FILE" <<EOF
competition_id: "$COMPETITION_ID"
project_id: "$PROJECT_ID"
user_id: "$USER_ID"
expected_time: $EXPECTED_TIME
token: "$TOKEN"
EOF

# set wait param
WAIT_PARAM="wait=false"
if [ "$WAIT_FLAG" = "--wait" ]; then
    WAIT_PARAM="wait=true"
fi

# submit it
echo "submitting to $SERVER_URL..."
echo "  competition: $COMPETITION_ID"
echo "  code file: $CODE_FILE"
echo "  expected time: $EXPECTED_TIME seconds"
echo "  wait mode: $WAIT_PARAM"
echo ""

RESPONSE=$(curl -s -X POST "$SERVER_URL/api/submit?$WAIT_PARAM" \
  -F "code=@$CODE_FILE" \
  -F "config_file=@$CONFIG_FILE")

# save response to logs
LOGS_DIR="$(dirname "$0")/../logs"
mkdir -p "$LOGS_DIR"
LOG_FILE="$LOGS_DIR/${COMPETITION_ID}_$(basename "$CODE_FILE" .py)_response.json"
echo "$RESPONSE" | jq '.' > "$LOG_FILE"

# get job id
JOB_ID=$(echo "$RESPONSE" | jq -r '.job_id')

if [ "$JOB_ID" != "null" ] && [ -n "$JOB_ID" ]; then
    echo "✓ submitted!"
    echo "  job id: $JOB_ID"
    echo "$RESPONSE" | jq -r '.node_id, .status' | while read line; do
        echo "  $line"
    done
    echo "  saved to: $LOG_FILE"
else
    echo "ERROR: submission failed"
    echo "$RESPONSE" | jq '.'
    rm -f "$CONFIG_FILE"
    exit 1
fi

# cleanup
rm -f "$CONFIG_FILE"

# if waiting, show completion status
if [ "$WAIT_FLAG" = "--wait" ]; then
    STATUS=$(echo "$RESPONSE" | jq -r '.status')
    if [ "$STATUS" = "completed" ]; then
        echo ""
        echo "✓ done!"
        EXIT_CODE=$(echo "$RESPONSE" | jq -r '.exit_code')
        if [ "$EXIT_CODE" != "null" ]; then
            echo "  exit code: $EXIT_CODE"
        fi
    fi
fi
