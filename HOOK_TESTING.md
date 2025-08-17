# Yadon Pet Hook Testing Guide

This document describes how to test the Claude Code notification hook system with the Yadon desktop pet.

## Overview

The Yadon pet monitors several hook file locations for messages from Claude Code and responds with appropriate speech bubbles. The hook system supports:

- **Generic notifications**: `notification:message`
- **Stop notifications**: `stop:message`
- **Custom Japanese messages**: `notification:日本語メッセージ`

## Hook File Locations

The Yadon pet monitors these files in order of priority:

### PID-Specific Hook Files (Highest Priority)
- `/tmp/yadon_hook_{claude_pid}.txt`
- `/tmp/claude_hook_{claude_pid}.txt`

### Generic Hook Files (Fallback)
- `/tmp/yadon_hook.txt`
- `/tmp/claude_hook.txt`
- `/var/tmp/claude_hook.txt`
- `~/.claude/hook.txt`

## Test Scripts

### 1. Full Test Suite: `test_hook.py`

Comprehensive testing script that:
- Detects running Claude processes
- Tests multiple hook message types
- Creates both generic and PID-specific hook files
- Verifies hook processing by checking if files are cleared
- Shows debug log information

```bash
python3 test_hook.py
```

### 2. Quick Test: `quick_hook_test.py`

Simple script for sending a single notification:

```bash
# Send default test message
python3 quick_hook_test.py

# Send custom message
python3 quick_hook_test.py "Your custom message here"

# Send Japanese message (will be formatted with やぁん)
python3 quick_hook_test.py "テスト"
```

## How the Hook System Works

1. **Monitoring**: Yadon checks hook files every 1 second
2. **Processing**: When a file contains a message:
   - Yadon reads and processes the message
   - Displays appropriate response in a speech bubble
   - Clears the hook file content
3. **Responses**: Different hook types trigger different responses:
   - `notification:` → "おしらせやぁん！なんだろうやぁん"
   - `stop:` → "ひとやすみするやぁん"
   - Japanese text → Adds "やぁん" suffix

## Troubleshooting

### Check if Yadon is Running
```bash
ps aux | grep yadon_pet
```

### Check Debug Log
```bash
tail -f /tmp/yadon_debug.log
```

### Manual Hook Test
```bash
# Create a hook file manually
echo "notification:Manual test" > /tmp/yadon_hook.txt

# Check if it gets processed (file should be emptied)
cat /tmp/yadon_hook.txt
```

### Check Claude Process PIDs
```bash
ps aux | grep claude | grep -v grep | grep -v yadon
```

## Expected Behavior

When a hook is triggered:
1. Yadon should display a speech bubble with the response message
2. The speech bubble appears above Yadon for 5 seconds
3. The hook file content is cleared after processing
4. Debug information is logged to `/tmp/yadon_debug.log`

## Hook Message Format

Messages should follow this format:
```
type:details
```

Examples:
- `notification:Task completed`
- `stop:Taking a break`
- `notification:ファイルを保存しました` (Japanese message)

## Integration with Claude Code

To integrate with Claude Code, create hook files when certain events occur:

```python
# Example: Send notification when code is executed
def notify_yadon(message):
    import subprocess
    # Get Claude PID
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    # ... find Claude PID ...
    
    # Write hook file
    with open(f'/tmp/yadon_hook_{claude_pid}.txt', 'w') as f:
        f.write(f'notification:{message}')
```

This creates a notification system where Yadon can provide visual feedback for Claude Code operations.