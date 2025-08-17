#!/usr/bin/env python3
"""
Visual verification test for Yadon hook responses.
This script sends a series of different hook types with clear messages.
"""

import time
import subprocess

def get_first_claude_pid():
    """Get the first running Claude process PID"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if 'claude' in line and 'yadon' not in line and 'node' not in line and 'grep' not in line:
                parts = line.split()
                if len(parts) > 10 and parts[10] == 'claude':
                    return parts[1]
        return None
    except Exception:
        return None

def send_hook_with_delay(message, delay=4):
    """Send a hook message and wait"""
    claude_pid = get_first_claude_pid()
    if not claude_pid:
        print("No Claude process found!")
        return False
    
    hook_file = f'/tmp/yadon_hook_{claude_pid}.txt'
    try:
        with open(hook_file, 'w') as f:
            f.write(message)
        print(f"📤 Sent: {message}")
        print(f"   → Look for Yadon's speech bubble!")
        time.sleep(delay)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🎯 Yadon Hook Response Verification")
    print("=" * 40)
    print("Watch your screen for Yadon's speech bubbles!")
    print()
    
    claude_pid = get_first_claude_pid()
    if not claude_pid:
        print("❌ No Claude process found. Please start Claude Code first.")
        return
    
    print(f"🎮 Using Claude PID: {claude_pid}")
    print()
    
    # Test sequence with clear visual cues
    tests = [
        ("notification:Hook test #1 - Basic notification", "Basic notification test"),
        ("stop:Hook test #2 - Stop message", "Stop/break message test"),
        ("notification:こんにちはやぁん", "Japanese message test"),
        ("notification:Hook test #3 - Final check", "Final verification test")
    ]
    
    for i, (hook_message, description) in enumerate(tests, 1):
        print(f"🔔 Test {i}: {description}")
        if send_hook_with_delay(hook_message):
            print("✅ Message sent successfully")
        else:
            print("❌ Failed to send message")
        print()
    
    print("🎉 Verification complete!")
    print("If you saw speech bubbles appear above Yadon, the hook system is working!")
    
    # Show recent debug log
    print("\n📋 Recent debug activity:")
    print("-" * 30)
    try:
        with open('/tmp/yadon_debug.log', 'r') as f:
            lines = f.readlines()
            relevant_lines = [line for line in lines[-20:] if 'respond_to_hook' in line or 'Hook message' in line]
            for line in relevant_lines[-5:]:
                print(f"   {line.strip()}")
    except Exception:
        print("   (Debug log not available)")

if __name__ == '__main__':
    main()