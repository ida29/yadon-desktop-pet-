#!/usr/bin/env python3
"""
Test script to trigger Yadon pet notification hooks.

This script creates hook files that the Yadon pet monitors to test
if the notification system is working correctly.
"""

import os
import time
import subprocess
import sys

def get_claude_pids():
    """Get running Claude process PIDs"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        claude_pids = []
        for line in lines:
            if 'claude' in line and 'yadon' not in line and 'node' not in line and 'grep' not in line:
                parts = line.split()
                # Check if the command is just "claude" (actual claude process)
                if len(parts) > 10 and parts[10] == 'claude':
                    claude_pids.append(parts[1])  # PID is second column
        return claude_pids
    except Exception as e:
        print(f"Error getting Claude PIDs: {e}")
        return []

def create_hook_file(filepath, message):
    """Create a hook file with the specified message"""
    try:
        with open(filepath, 'w') as f:
            f.write(message)
        print(f"Created hook file: {filepath}")
        print(f"Message: {message}")
        return True
    except Exception as e:
        print(f"Error creating hook file {filepath}: {e}")
        return False

def test_notification_hook():
    """Test the notification hook functionality"""
    print("Testing Yadon pet notification hooks...")
    print("=" * 50)
    
    # Get current Claude PIDs
    claude_pids = get_claude_pids()
    print(f"Found Claude PIDs: {claude_pids}")
    
    # Test messages to send
    test_messages = [
        "notification:Test message from Claude Code",
        "notification:テストメッセージ",  # Japanese test message
        "stop:Taking a break",
        "notification:Hook test successful"
    ]
    
    # Generic hook files (for Yadon without specific PID)
    generic_hook_files = [
        '/tmp/yadon_hook.txt',
        '/tmp/claude_hook.txt'
    ]
    
    # Test each message
    for i, message in enumerate(test_messages):
        print(f"\nTest {i+1}: Sending '{message}'")
        
        # Create generic hook files
        for hook_file in generic_hook_files:
            if create_hook_file(hook_file, message):
                print(f"✓ Created {hook_file}")
        
        # Create PID-specific hook files for each Claude process
        for pid in claude_pids:
            pid_specific_files = [
                f'/tmp/yadon_hook_{pid}.txt',
                f'/tmp/claude_hook_{pid}.txt'
            ]
            for hook_file in pid_specific_files:
                if create_hook_file(hook_file, message):
                    print(f"✓ Created {hook_file} for PID {pid}")
        
        print(f"Waiting 6 seconds for Yadon to process hook...")
        time.sleep(6)
        
        # Check if hook files were cleared (indicating they were processed)
        files_cleared = 0
        total_files = 0
        
        for hook_file in generic_hook_files:
            total_files += 1
            try:
                if os.path.exists(hook_file):
                    with open(hook_file, 'r') as f:
                        content = f.read().strip()
                    if not content:
                        files_cleared += 1
                        print(f"✓ {hook_file} was processed (cleared)")
                    else:
                        print(f"✗ {hook_file} still contains: {content}")
                else:
                    print(f"✗ {hook_file} doesn't exist")
            except Exception as e:
                print(f"✗ Error checking {hook_file}: {e}")
        
        for pid in claude_pids:
            pid_specific_files = [
                f'/tmp/yadon_hook_{pid}.txt',
                f'/tmp/claude_hook_{pid}.txt'
            ]
            for hook_file in pid_specific_files:
                total_files += 1
                try:
                    if os.path.exists(hook_file):
                        with open(hook_file, 'r') as f:
                            content = f.read().strip()
                        if not content:
                            files_cleared += 1
                            print(f"✓ {hook_file} was processed (cleared)")
                        else:
                            print(f"✗ {hook_file} still contains: {content}")
                    else:
                        print(f"✗ {hook_file} doesn't exist")
                except Exception as e:
                    print(f"✗ Error checking {hook_file}: {e}")
        
        print(f"Files processed: {files_cleared}/{total_files}")
        
        if i < len(test_messages) - 1:
            print("\nPress Enter to continue to next test, or Ctrl+C to stop...")
            try:
                input()
            except KeyboardInterrupt:
                print("\nTest interrupted by user")
                break

def check_yadon_status():
    """Check if Yadon pets are running"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        yadon_count = 0
        for line in lines:
            if 'yadon_pet.py' in line and 'grep' not in line:
                yadon_count += 1
                print(f"Found Yadon process: {line}")
        
        if yadon_count == 0:
            print("⚠️  No Yadon pets are currently running!")
            print("Please start Yadon first by running: python3 yadon_pet.py")
            return False
        else:
            print(f"✓ Found {yadon_count} Yadon pet(s) running")
            return True
    except Exception as e:
        print(f"Error checking Yadon status: {e}")
        return False

def check_debug_log():
    """Check the debug log for hook processing"""
    log_file = '/tmp/yadon_debug.log'
    if os.path.exists(log_file):
        print(f"\nDebug log entries (last 20 lines):")
        print("-" * 40)
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-20:]:
                    print(line.strip())
        except Exception as e:
            print(f"Error reading debug log: {e}")
    else:
        print(f"\nDebug log not found at {log_file}")

def main():
    print("Yadon Pet Hook Test Script")
    print("=" * 30)
    
    # Check if Yadon is running
    if not check_yadon_status():
        sys.exit(1)
    
    print("\nThis script will test the notification hook system.")
    print("You should see Yadon respond with speech bubbles.")
    print("\nPress Enter to start testing, or Ctrl+C to exit...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    
    # Run the hook tests
    test_notification_hook()
    
    # Show debug log
    check_debug_log()
    
    print("\n" + "=" * 50)
    print("Hook testing completed!")
    print("Check if Yadon displayed speech bubbles during the test.")
    print("If not, check the debug log above for troubleshooting.")

if __name__ == '__main__':
    main()