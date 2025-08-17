#!/usr/bin/env python3
"""
Quick test script to send a single notification to Yadon pet.
Usage: python3 quick_hook_test.py [message]
"""

import sys
import subprocess

def get_claude_pid():
    """Get the first running Claude process PID"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if 'claude' in line and 'yadon' not in line and 'node' not in line and 'grep' not in line:
                parts = line.split()
                # Check if the command is just "claude" (actual claude process)
                if len(parts) > 10 and parts[10] == 'claude':
                    return parts[1]  # PID is second column
        return None
    except Exception:
        return None

def send_notification(message="Test notification from Claude Code"):
    """Send a notification to Yadon pet"""
    claude_pid = get_claude_pid()
    
    # Create generic hook file
    hook_message = f"notification:{message}"
    
    try:
        with open('/tmp/yadon_hook.txt', 'w') as f:
            f.write(hook_message)
        print(f"✓ Sent notification: {message}")
        
        # Also create PID-specific hook if we found a Claude process
        if claude_pid:
            with open(f'/tmp/yadon_hook_{claude_pid}.txt', 'w') as f:
                f.write(hook_message)
            print(f"✓ Sent PID-specific notification for Claude {claude_pid}")
        
        print("Check your screen for Yadon's response!")
        
    except Exception as e:
        print(f"Error sending notification: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = "Test notification from Claude Code"
    
    send_notification(message)