import subprocess
from typing import Dict, Any

def get_system_vitals() -> Dict[str, Any]:
    """Gather basic system metrics using standard Linux commands."""
    vitals = {}
    
    # 1. CPU Load (1, 5, 15 min averages)
    try:
        with open("/proc/loadavg", "r") as f:
            load = f.read().split()
            vitals["cpu_load"] = f"{load[0]}, {load[1]}, {load[2]}"
    except Exception:
        vitals["cpu_load"] = "Unknown"

    # 2. Memory Usage (Free command)
    try:
        mem_output = subprocess.check_output(["free", "-h"]).decode()
        lines = mem_output.splitlines()
        # "Mem: 15Gi 2.4Gi 8.2Gi ..."
        vitals["memory"] = lines[1].split()[2] + " / " + lines[1].split()[1]
    except Exception:
        vitals["memory"] = "Unknown"

    # 3. Disk Space (Root partition)
    try:
        df_output = subprocess.check_output(["df", "-h", "/"]).decode()
        lines = df_output.splitlines()
        vitals["disk"] = lines[1].split()[2] + " / " + lines[1].split()[1]
    except Exception:
        vitals["disk"] = "Unknown"

    return vitals
