import subprocess
from pathlib import Path

def get_recent_pacman_logs(lines: int = 50) -> str:
    """Read the last N lines from pacman.log."""
    log_path = Path("/var/log/pacman.log")
    if not log_path.exists():
        return "Error: /var/log/pacman.log not found."
    
    try:
        # Use tail to get recent lines efficiently
        output = subprocess.check_output(["tail", "-n", str(lines), str(log_path)]).decode()
        return output
    except Exception as e:
        return f"Error reading logs: {str(e)}"

def get_recent_journal_logs(lines: int = 50) -> str:
    """Read the last N lines from journalctl -xe."""
    try:
        output = subprocess.check_output(["journalctl", "-n", str(lines), "--no-pager"]).decode()
        return output
    except Exception as e:
        return f"Error reading journal: {str(e)}"
