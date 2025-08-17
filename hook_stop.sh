#!/bin/bash
# Get the Claude Code PID - look for process exactly named 'claude'
CLAUDE_PID=$(ps aux | grep -E '^[^ ]+[ ]+[0-9]+.*claude[ ]*$' | grep -v grep | awk '{print $2}' | head -1)

if [ -z "$CLAUDE_PID" ]; then
    # Fallback: try to find any claude process in terminal
    CLAUDE_PID=$(ps aux | grep 'claude' | grep -v grep | grep -v 'Claude.app' | awk '{print $2}' | head -1)
fi

if [ -z "$CLAUDE_PID" ]; then
    # Last fallback to parent PID method
    CLAUDE_PID=$(ps -o ppid= -p $$ | xargs ps -o ppid= -p | tr -d ' ')
fi

echo "stop:" > /tmp/claude_hook_${CLAUDE_PID}.txt
echo "[$(date)] Stop hook called, Claude PID: $CLAUDE_PID" >> /tmp/hook_debug.log