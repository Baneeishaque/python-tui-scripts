#!/bin/bash
# Description: Finalizes the workflow status and reports failures.

set -e

HAS_FAILURE=false
FAILURE_MSG=""

# 1. Check for downloader status (passed as env var) - Priority Check
if [ "$DOWNLOADER_OUTCOME" == "failure" ]; then
    HAS_FAILURE=true
    FAILURE_MSG="The downloader script failed."

# 2. Check for errors from artifacts script (only if downloader passed)
elif [ -f "artifacts/failure_message.txt" ]; then
    HAS_FAILURE=true
    FAILURE_MSG=$(cat artifacts/failure_message.txt)
fi

# 3. Handle failure reporting
if [ "$HAS_FAILURE" == "true" ]; then
    echo "::error::$FAILURE_MSG"
    
    echo "Creating GitHub Issue..."
    gh issue create --title "Workflow Failure: TLDV Downloader ($RUN_ID)" \
        --body "### Workflow failed
        
        $FAILURE_MSG
        
        [View logs]($SERVER_URL/$REPOSITORY/actions/runs/$RUN_ID)" \
        --assignee "$ACTOR"
    
    if [ "$EVENT_NAME" == "pull_request" ] && [ -n "$PR_NUMBER" ]; then
        echo "Posting PR comment..."
        gh pr comment "$PR_NUMBER" --body "❌ Workflow failed: $FAILURE_MSG. [View logs]($SERVER_URL/$REPOSITORY/actions/runs/$RUN_ID)"
    fi
    
    exit 1
fi

echo "Workflow finalized successfully."
