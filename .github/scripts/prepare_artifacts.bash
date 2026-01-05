#!/bin/bash
# Description: Pairs .mp4 files with their corresponding .json metadata files.

set -e

ARTIFACTS_DIR="artifacts"
mkdir -p "$ARTIFACTS_DIR"

echo "Searching for .mp4 files in the current directory..."
COUNT=0
MISSING_JSON_COUNT=0
shopt -s nullglob
for mp4 in *.mp4; do
    base="${mp4%.mp4}"
    json="$base.json"
    
    echo "Processing: $mp4"
    cp -v "$mp4" "$ARTIFACTS_DIR/"
    
    if [ -f "$json" ]; then
        echo "Matching json found: $json"
        cp -v "$json" "$ARTIFACTS_DIR/"
        ((COUNT++))
    else
        echo "Warning: No matching .json found for $mp4"
        ((MISSING_JSON_COUNT++))
    fi
done

FAILURE_REASON=""

if [ "$COUNT" -eq 0 ] && [ "$MISSING_JSON_COUNT" -eq 0 ]; then
    FAILURE_REASON="Error: No .mp4 files found. At least one pair is required."
elif [ "$MISSING_JSON_COUNT" -gt 0 ]; then
    FAILURE_REASON="Error: $MISSING_JSON_COUNT .mp4 file(s) are missing their matching .json files."
fi

if [ -n "$FAILURE_REASON" ]; then
    echo "$FAILURE_REASON"
    echo "Stored all available files in $ARTIFACTS_DIR/ for debugging."
    echo "$FAILURE_REASON" > "$ARTIFACTS_DIR/failure_message.txt"
fi

echo "Successfully processed $COUNT complete artifact pair(s) in $ARTIFACTS_DIR/"
