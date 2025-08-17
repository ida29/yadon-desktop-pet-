#!/usr/bin/env python3
"""
Automated test script for Yadon pet notification hooks.
Runs without user interaction.
"""

import os
import time
import subprocess

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

def test_hook_system():
    """Run automated hook tests"""
    print("Running automated Yadon hook tests...")
    print("=" * 40)
    
    # Get Claude PIDs
    claude_pids = get_claude_pids()
    print(f"Found Claude PIDs: {claude_pids}")
    
    if not claude_pids:
        print("No Claude processes found - testing with generic hooks only")
    
    # Test messages
    test_cases = [
        ("notification", "Automated test message"),
        ("notification", "日本語テスト"),  # Japanese test
        ("stop", "Break time"),
        ("notification", "Final test")
    ]
    
    results = []
    
    for i, (hook_type, message) in enumerate(test_cases):
        print(f"\nTest {i+1}: {hook_type}:{message}")
        
        hook_message = f"{hook_type}:{message}"
        files_created = 0
        files_processed = 0
        
        # Create generic hook file
        try:
            with open('/tmp/yadon_hook.txt', 'w') as f:
                f.write(hook_message)
            files_created += 1
            print(f"✓ Created /tmp/yadon_hook.txt")
        except Exception as e:
            print(f"✗ Error creating generic hook: {e}")
        
        # Create PID-specific hook files
        for pid in claude_pids:
            try:
                hook_file = f'/tmp/yadon_hook_{pid}.txt'
                with open(hook_file, 'w') as f:
                    f.write(hook_message)
                files_created += 1
                print(f"✓ Created {hook_file}")
            except Exception as e:
                print(f"✗ Error creating hook for PID {pid}: {e}")
        
        # Wait for processing
        print("Waiting 3 seconds for processing...")
        time.sleep(3)
        
        # Check if files were processed (cleared)
        try:
            with open('/tmp/yadon_hook.txt', 'r') as f:
                content = f.read().strip()
            if not content:
                files_processed += 1
                print("✓ Generic hook file processed")
            else:
                print(f"✗ Generic hook file not processed: {content}")
        except Exception as e:
            print(f"✗ Error checking generic hook: {e}")
        
        for pid in claude_pids:
            try:
                hook_file = f'/tmp/yadon_hook_{pid}.txt'
                with open(hook_file, 'r') as f:
                    content = f.read().strip()
                if not content:
                    files_processed += 1
                    print(f"✓ PID {pid} hook file processed")
                else:
                    print(f"✗ PID {pid} hook file not processed: {content}")
            except Exception as e:
                print(f"✗ Error checking PID {pid} hook: {e}")
        
        success_rate = files_processed / files_created if files_created > 0 else 0
        results.append((hook_type, message, success_rate))
        print(f"Processing rate: {files_processed}/{files_created} ({success_rate:.1%})")
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    total_success = 0
    for hook_type, message, success_rate in results:
        status = "PASS" if success_rate >= 0.5 else "FAIL"
        print(f"{status}: {hook_type}:{message} ({success_rate:.1%})")
        if success_rate >= 0.5:
            total_success += 1
    
    overall_success = total_success / len(results) if results else 0
    print(f"\nOverall success rate: {total_success}/{len(results)} ({overall_success:.1%})")
    
    if overall_success >= 0.75:
        print("✓ Hook system is working correctly!")
    elif overall_success >= 0.5:
        print("⚠ Hook system is partially working")
    else:
        print("✗ Hook system appears to have issues")
    
    return overall_success >= 0.5

def check_yadon_running():
    """Check if Yadon is running"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if 'yadon_pet.py' in line and 'grep' not in line:
                print(f"✓ Yadon is running: PID {line.split()[1]}")
                return True
        print("✗ Yadon is not running")
        return False
    except Exception as e:
        print(f"Error checking Yadon: {e}")
        return False

def main():
    print("Yadon Pet Hook System - Automated Test")
    print("=" * 40)
    
    # Check prerequisites
    if not check_yadon_running():
        print("\nPlease start Yadon first: python3 yadon_pet.py")
        return False
    
    # Run tests
    success = test_hook_system()
    
    # Show debug log sample
    print("\nRecent debug log entries:")
    print("-" * 30)
    try:
        with open('/tmp/yadon_debug.log', 'r') as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(line.strip())
    except Exception as e:
        print(f"Could not read debug log: {e}")
    
    return success

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)