#!/bin/bash
# check job status, need job id

SERVER_URL="https://ceriferous-hoelike-jeffie.ngrok-free.dev"

if [ -z "$1" ]; then
    echo "usage: ./check_status.sh <JOB_ID> [TOKEN]"
    echo "or set TOKEN env var"
    exit 1
fi

JOB_ID=$1
TOKEN=${2:-$TOKEN}

if [ -z "$TOKEN" ]; then
    echo "error: need token. set TOKEN env var or pass as second arg"
    exit 1
fi

curl -H "Authorization: Bearer $TOKEN" \
  "$SERVER_URL/api/status/$JOB_ID" | jq '.'
