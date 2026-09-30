import os
import subprocess
from typing import Any, Dict


def get_system_vitals() -> Dict[str, Any]:
    """Gather basic system metrics using standard Linux commands."""
    vitals = {"cpu_cores": os.cpu_count() or "Unknown"}

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
        fields = mem_output.splitlines()[1].split()
        # "Mem: 15Gi 2.4Gi 8.2Gi ... 12Gi"
        vitals["memory"] = f"{fields[2]} / {fields[1]}"
        vitals["memory_available"] = fields[6]
    except Exception:
        vitals["memory"] = "Unknown"
        vitals["memory_available"] = "Unknown"

    # 3. Disk Space (Root partition)
    try:
        df_output = subprocess.check_output(["df", "-h", "/"]).decode()
        fields = df_output.splitlines()[1].split()
        vitals["disk"] = f"{fields[2]} / {fields[1]}"
        vitals["disk_percent"] = fields[4]
    except Exception:
        vitals["disk"] = "Unknown"
        vitals["disk_percent"] = "Unknown"

    return vitals
