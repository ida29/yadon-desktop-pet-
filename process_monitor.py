"""Process monitoring functionality for Yadon Desktop Pet"""

import subprocess
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from config import YADON_POSITIONS, VARIANT_ORDER, MAX_YADON_COUNT


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
        
        if current_count != self.last_count:
            # Process count changed, update Yadon instances
            if current_count > self.last_count:
                # Add more Yadons
                screen = QApplication.primaryScreen().geometry()
                positions = [
                    (int(YADON_POSITIONS[i][0] * screen.width()),
                     int(YADON_POSITIONS[i][1] * screen.height()))
                    for i in range(len(YADON_POSITIONS))
                ]
                
                # Get current Claude PIDs (actual claude processes only)
                claude_pids = get_claude_pids()
                
                for i in range(self.last_count, current_count):
                    # Import here to avoid circular import
                    from yadon_pet import YadonPet
                    
                    claude_pid = claude_pids[i] if i < len(claude_pids) else None
                    variant = VARIANT_ORDER[i % len(VARIANT_ORDER)]  # Cycle through variants
                    pet = YadonPet(claude_pid=claude_pid, variant=variant)
                    if i < len(positions):
                        pet.move(positions[i][0] - pet.width() // 2,
                                positions[i][1] - pet.height() // 2)
                    self.pets.append(pet)
                    pet.show()
            elif current_count < self.last_count:
                # Remove excess Yadons
                while len(self.pets) > max(current_count, 0):
                    pet = self.pets.pop()
                    pet.close()
            
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
                if len(parts) > 10 and parts[10] == 'claude':
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
                if len(parts) > 10 and parts[10] == 'claude':
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