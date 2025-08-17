# Yadon Desktop Pet 🦦

A desktop pet application featuring Yadon (Slowpoke) that monitors Claude Code processes and responds to hooks with speech bubbles.

## Features

- **Pixel Art Yadon**: 16x16 pixel art sprite with animated face
- **Claude Code Integration**: Monitors Claude Code processes and displays PID
- **Hook Support**: Responds to Claude Code hooks with speech bubbles
- **Auto-start**: Can be configured to start automatically on system boot (macOS)
- **Multiple Yadon Support**: Spawns multiple Yadon instances for multiple Claude Code processes
- **Smart Speech Bubbles**: Pokemon-style text boxes that adjust position based on screen edges

## Installation

### Prerequisites

```bash
# Install Python 3 and PyQt6
pip install PyQt6
```

### Quick Install (macOS)

```bash
# Clone the repository
git clone https://github.com/ida29/yadon-desktop-pet-.git
cd yadon-desktop-pet-

# Run the installation script for auto-start
./install.sh
```

### Manual Run

```bash
python3 yadon_pet.py
```

## Claude Code Hook Integration

### Setting up hooks in Claude Code

Add the following to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/work/yadon-desktop-pet-/hook_notify.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/work/yadon-desktop-pet-/hook_stop.sh"
          }
        ]
      }
    ]
  },
  "model": "opus"
}
```

**Note**: Update the paths to match your installation directory.

### Available Hooks

- **Stop Hook** (`hook_stop.sh`): Displays "ひとやすみするやぁん" when Claude Code stops
- **Notification Hook** (`hook_notify.sh`): Displays "びびっときたやぁん" for notifications

### Custom Hook Messages

You can send custom messages to Yadon by writing to the hook file:

```bash
# Replace {PID} with your Claude Code process ID (shown under Yadon)
echo "your message" > /tmp/yadon_hook_{PID}.txt

# Or use a generic hook file (first Yadon will respond)
echo "your message" > /tmp/yadon_hook.txt
```

## Configuration

### Main Configuration (`config.py`)

- **Window Size**: 64x84 pixels (including PID display)
- **PID Display**: Shows Claude Code process ID (font size 12, bold)
- **Animation Interval**: Face animation every 500ms
- **Random Actions**: Every 45-90 seconds
- **Movement**: Slow, minimal movement (15 seconds per move, Yadon-style)
- **Speech Bubble Duration**: 5 seconds

### Speech Bubble Features

- Pokemon-style text boxes with double borders
- Automatic word wrapping for long messages
- Smart positioning:
  - Default: Above Yadon
  - If no space above: Below Yadon
  - If no vertical space: Beside Yadon (left or right based on position)
- Different colors for hook messages (light cyan) vs normal messages (white)
- Follows Yadon smoothly during movement

## File Structure

```
yadon-desktop-pet-/
├── yadon_pet.py           # Main application
├── config.py               # Configuration constants
├── pixel_data.py           # Yadon sprite data
├── speech_bubble.py        # Speech bubble widget
├── process_monitor.py      # Claude Code process monitoring
├── hook_handler.py         # Hook message handling
├── hook_notify.sh          # Notification hook script
├── hook_stop.sh           # Stop hook script
├── com.yadon.pet.plist    # macOS LaunchAgent config
├── install.sh             # Installation script
└── requirements.txt       # Python dependencies
```

## Auto-start Management (macOS)

### Enable auto-start
```bash
./install.sh
```

### Disable auto-start
```bash
launchctl unload ~/Library/LaunchAgents/com.yadon.pet.plist
```

### Complete removal
```bash
launchctl unload ~/Library/LaunchAgents/com.yadon.pet.plist
rm ~/Library/LaunchAgents/com.yadon.pet.plist
```

## Troubleshooting

### Yadon not appearing
- Check if the process is running: `ps aux | grep yadon_pet`
- Check logs: `tail -f /tmp/yadon-pet.log`
- Check error logs: `tail -f /tmp/yadon-pet-error.log`

### Hooks not working
- Verify Claude Code PID: Check the number displayed under Yadon
- Check hook debug log: `tail -f /tmp/hook_debug.log`
- Ensure hook scripts are executable: `chmod +x hook_*.sh`
- Verify paths in `~/.claude/settings.json` match your installation

### Speech bubble positioning issues
- The bubble automatically adjusts position based on screen edges
- If Yadon is at the top, bubble appears below
- If at the bottom, bubble appears above
- If no vertical space, bubble appears to the side

### Multiple Claude Code instances
- Each Claude Code process gets its own Yadon
- Each Yadon displays its associated Claude Code PID
- Hook messages are routed to the correct Yadon based on PID

## Debug Logs

- **Main log**: `/tmp/yadon-pet.log`
- **Error log**: `/tmp/yadon-pet-error.log`
- **Debug log**: `/tmp/yadon_debug.log`
- **Hook debug**: `/tmp/hook_debug.log`

## License

MIT License

## Credits

Created with Claude Code - A pixel art Yadon companion for your Claude Code sessions!

やぁん 🦥