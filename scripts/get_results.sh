#!/bin/bash
# grab results for a job, saves em to results folder

SERVER_URL="https://ceriferous-hoelike-jeffie.ngrok-free.dev"
RESULTS_DIR="../results"

if [ -z "$1" ]; then
    echo "usage: ./get_results.sh <JOB_ID> [TOKEN]"
    echo "or set TOKEN env var"
    exit 1
fi

JOB_ID=$1
TOKEN=${2:-$TOKEN}

if [ -z "$TOKEN" ]; then
    echo "error: need token. set TOKEN env var or pass as second arg"
    exit 1
fi

echo "fetching results for job $JOB_ID..."
curl -s -H "Authorization: Bearer $TOKEN" \
  "$SERVER_URL/api/results/$JOB_ID" | \
  jq -r '.stdout' > "$RESULTS_DIR/results_${JOB_ID}.jsonl"

echo "saved to $RESULTS_DIR/results_${JOB_ID}.jsonl"
head -5 "$RESULTS_DIR/results_${JOB_ID}.jsonl"
