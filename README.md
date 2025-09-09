# MS Teams Keep Active

A Python utility that prevents Microsoft Teams from going inactive by simulating various types of user activity throughout the workday.

## Features

- **Multiple Activity Methods**: Rotates between mouse movements, keyboard inputs, scroll actions, and Teams-specific activities
- **Smart Window Focus**: Automatically detects and focuses Microsoft Teams windows for targeted activity simulation
- **Randomized Intervals**: Varies activity timing between 1-3 minutes to appear more natural
- **Automatic Exit**: Stops running after 5:30 PM by default
- **Graceful Shutdown**: Handle Ctrl+C interruption cleanly
- **Visual Feedback**: Provides clear console output showing activity status and timing

## Requirements

### System Dependencies
- **Linux**: This script is designed for Linux systems using X11 or XWayland
- **xdotool**: Required for simulating mouse and keyboard input

### Python Dependencies
- Python 3.x (no additional packages required - uses only standard library)

## Installation

1. **Install xdotool**
    ## Fedora/RHEL
   ```bash
   sudo dnf install xdotool
   ```
   ## Ubuntu/Debian
   ```bash
   sudo apt install xdotool
   ```
   ## Arch Linux
   ```bash
   sudo pacman -S xdotool
   ```

2. **Clone or download the script**:
   ```bash
   git clone https://github.com/friedcherries/ms-teams-keep-active.git
   cd ms-teams-keep-active
   ```

3. **Make executable** (optional):
   ```bash
   chmod +x keep_active.py
   ```

## Usage

### Basic Usage
```bash
python3 keep_active.py
```

### Background Execution
```bash
# Run in background
python3 keep_active.py &

# Or use nohup to persist after terminal closes
nohup python3 keep_active.py &
```

## How It Works

The script employs four different activity simulation methods:

1. **Mouse Jiggle**: Creates a small square movement pattern with the mouse cursor
2. **Key Combination**: Sends subtle key presses (Shift, F15, Ctrl)
3. **Scroll Activity**: Simulates mouse wheel scrolling up and down
4. **Teams-Specific Activity**: Focuses the Teams window and sends application-specific inputs

### Activity Rotation
- Methods rotate automatically to avoid predictable patterns
- Random intervals between 60-180 seconds (1-3 minutes)
- Always attempts to focus Teams window before simulating activity

### Automatic Shutdown
- Default exit time: 5:30 PM
- Modify the `exit_after()` function call in `main()` to change timing
- Example: `exit_after(18, 0)` for 6:00 PM shutdown

## Configuration

### Changing Exit Time
Edit the `exit_after()` call in the `main()` function:
```python
# Exit at 6:00 PM instead of 5:30 PM
exit_after(18, 0)
```

### Adjusting Activity Intervals
Modify the interval range in the main loop:
```python
# Change from 60-180 seconds to 30-120 seconds
interval_seconds = random.randint(30, 120)
```

## Output Example

```
🚀 MS Teams Keep Active
🎯 Multiple activity methods, every 2 minutes
🔄 Rotates between mouse, keyboard, and scroll methods
⌨️  Press Ctrl+C to stop

--- Activity cycle at 14:32:15 ---
🎯 Focused Teams window: Microsoft Teams - Chrome
📱 Teams-specific activity at 14:32:16
✅ Teams window was focused for activity
⏳ Waiting 2 minutes...

--- Activity cycle at 14:34:28 ---
🖱️  Mouse pattern completed at 14:34:29
⚠️  Could not focus Teams window
⏳ Waiting 1 minutes...
```

## Safety Features

- **Non-intrusive**: Activities are designed to be minimal and not interfere with actual work
- **Safe key combinations**: Uses modifier keys and function keys that typically don't trigger unwanted actions
- **Window detection**: Attempts to target Teams specifically rather than affecting other applications
- **Graceful exit**: Responds properly to interruption signals

## Troubleshooting

### "xdotool not found" Error
Install xdotool using your distribution's package manager (see Installation section).

### Teams Window Not Detected
- Ensure Microsoft Teams is running in a browser (Edge/Chrome)
- The script searches for windows containing "Teams" or "Microsoft Teams" in the title
- Check that Teams is visible (not minimized)

### Activity Not Preventing Idle Status
- Verify Teams is actually receiving focus when the script runs
- Try running Teams in a dedicated browser window rather than a tab
- Some corporate Teams configurations may have different idle detection methods

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the utility.

## Disclaimer

This tool is intended for legitimate use cases where preventing idle status is necessary (e.g., during long meetings, presentations, or monitoring tasks). Users are responsible for ensuring compliance with their organization's IT policies and employment guidelines.

## License

This project is provided as-is for educational and practical purposes. Use responsibly and in accordance with your workplace policies.