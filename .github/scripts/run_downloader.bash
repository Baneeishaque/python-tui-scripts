#!/bin/bash
# Description: Runs the TLDV Downloader script non-interactively.

set -e

if [ -z "$MEETING_URL" ] || [ -z "$AUTH_TOKEN" ]; then
    echo "Error: MEETING_URL and AUTH_TOKEN environment variables must be set."
    exit 1
fi

echo "Running Downloader..."
python tldv_downloader.py <<EOF
$MEETING_URL
$AUTH_TOKEN
EOF
