"""Process monitoring functionality for Yadon Desktop Pet"""

import subprocess
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from config import VARIANT_ORDER, MAX_YADON_COUNT


class ProcessMonitor(QTimer):
    """Monitor Claude Code processes and manage Yadon instances"""
    def __init__(self, initial_pets):
        super().__init__()
        self.pets = initial_pets
        self.last_count = len(initial_pets)
        self.timeout.connect(self.check_processes)
        self.setInterval(5000)  # Check every 5 seconds
    
    def check_processes(self):
        current_count = count_claude_processes()
        current_count = min(current_count, MAX_YADON_COUNT) if current_count > 0 else 0
        
        # Always update PIDs for existing Yadons
        claude_pids = get_claude_pids()
        for i, pet in enumerate(self.pets):
            if i < len(claude_pids):
                new_pid = claude_pids[i]
                if pet.claude_pid != new_pid:
                    # Update PID if it changed
                    pet.claude_pid = new_pid
                    # Also update hook handler with new PID
                    if hasattr(pet, 'hook_handler'):
                        pet.hook_handler.claude_pid = new_pid
                    pet.update()  # Trigger redraw to show new PID
        
        if current_count != self.last_count:
            # Process count changed, update Yadon instances
            if current_count > self.last_count:
                # Add more Yadons
                screen = QApplication.primaryScreen().geometry()
                
                # Calculate positions for bottom-right alignment
                margin = 20  # Margin from screen edges
                spacing = 10  # Space between Yadons
                
                # Already got PIDs above, reuse them
                # claude_pids = get_claude_pids()
                
                for i in range(self.last_count, current_count):
                    # Import here to avoid circular import
                    from yadon_pet import YadonPet
                    import random
                    
                    claude_pid = claude_pids[i] if i < len(claude_pids) else None
                    # Randomly select variant with equal probability
                    variant = random.choice(VARIANT_ORDER)
                    pet = YadonPet(claude_pid=claude_pid, variant=variant)
                    
                    # Position in bottom-right, stacking from right to left
                    from config import WINDOW_WIDTH, WINDOW_HEIGHT
                    x_pos = screen.width() - margin - (WINDOW_WIDTH + spacing) * (len(self.pets) + 1)
                    y_pos = screen.height() - margin - WINDOW_HEIGHT
                    pet.move(x_pos, y_pos)
                    
                    self.pets.append(pet)
                    pet.show()
            elif current_count < self.last_count:
                # Remove excess Yadons - properly clean up
                while len(self.pets) > max(current_count, 0):
                    pet = self.pets.pop()
                    # Close any open speech bubbles first
                    if hasattr(pet, 'bubble') and pet.bubble:
                        pet.bubble.close()
                    # Stop all timers
                    if hasattr(pet, 'timer'):
                        pet.timer.stop()
                    if hasattr(pet, 'action_timer'):
                        pet.action_timer.stop()
                    if hasattr(pet, 'monitor_timer'):
                        pet.monitor_timer.stop()
                    if hasattr(pet, 'hook_timer'):
                        pet.hook_timer.stop()
                    # Close the widget
                    pet.close()
                    pet.deleteLater()  # Ensure proper cleanup
            
            self.last_count = current_count


def count_claude_processes():
    """Count the number of Claude Code processes running"""
    try:
        # Use ps to get more detailed info and filter properly
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        claude_count = 0
        for line in lines:
            # Count only actual claude processes (not node wrapper, not yadon)
            if 'claude' in line and 'yadon' not in line and 'grep' not in line and 'node' not in line:
                # Look for the actual claude binary process
                parts = line.split()
                # Check if the command is just "claude" (not a path or other command)
                # The command may be at different column positions depending on process state
                if len(parts) > 10:
                    command_start = 10
                    # Check if it's actually the claude binary
                    if parts[command_start] == 'claude' or (len(parts) > 11 and parts[11] == 'claude'):
                        claude_count += 1
        return claude_count
    except Exception:
        return 0


def get_claude_pids():
    """Get list of Claude process PIDs"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        claude_pids = []
        for line in lines:
            if 'claude' in line and 'yadon' not in line and 'node' not in line and 'grep' not in line:
                parts = line.split()
                # Check if the command is just "claude" (actual claude process)
                # The command may be at different column positions depending on process state
                if len(parts) > 10:
                    # Find where the command starts (after process state columns)
                    command_start = 10
                    # Check if it's actually the claude binary
                    if parts[command_start] == 'claude' or (len(parts) > 11 and parts[11] == 'claude'):
                        claude_pids.append(parts[1])  # PID is second column
        return claude_pids
    except Exception:
        return []


def find_claude_pid():
    """Find a Claude process PID"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if 'claude' in line and 'yadon' not in line and 'node' not in line and 'grep' not in line:
                parts = line.split()
                if len(parts) > 1:
                    return parts[1]  # Return PID (second column)
    except Exception:
        pass
    return None