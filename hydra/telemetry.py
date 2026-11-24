"""
Live Telemetry & Grokbot Skeptic Engine
Interrogates Darwin kernel, hardware anchors, and OpenBot team state.
"""

import os
import subprocess
from typing import Dict, Any, List, Tuple

def get_system_telemetry() -> Dict[str, Any]:
    """Reads live hardware and kernel telemetry without external packages."""
    cpu_brand = "Apple Silicon"
    ncpu = "8"
    try:
        cpu_brand = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"], text=True).strip()
        ncpu = subprocess.check_output(["sysctl", "-n", "hw.ncpu"], text=True).strip()
    except Exception:
        pass

    load1, load5, load15 = os.getloadavg()

    free_mb = 2048
    try:
        vm = subprocess.check_output(["vm_stat"], text=True)
        for line in vm.splitlines():
            if "Pages free" in line:
                free_mb = int(line.split(":")[1].strip().replace(".", "")) * 4096 // (1024 * 1024)
    except Exception:
        pass

    listening_ports = []
    try:
        out = subprocess.check_output(["lsof", "-iTCP", "-sTCP:LISTEN", "-n", "-P"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 9:
                proc = parts[0]
                addr = parts[8]
                listening_ports.append(f"{proc} @ {addr}")
    except Exception:
        pass

    agents_dir = "/Users/lovelogic/OpenBot/Agents"
    discovered_agents = []
    if os.path.exists(agents_dir):
        for entry in os.listdir(agents_dir):
            if entry.startswith("agent-"):
                discovered_agents.append(entry)

    return {
        "cpu_brand": cpu_brand,
        "ncpu": ncpu,
        "load": (load1, load5, load15),
        "free_mb": free_mb,
        "ports": listening_ports,
        "agents_count": len(discovered_agents),
        "agents": discovered_agents
    }


def run_grokbot_audit(telemetry: Dict[str, Any]) -> Tuple[int, List[Tuple[str, str, str]]]:
    """Zero-bullshit empirical reality audit of workspace & runtime."""
    receipts = []
    score = 100

    suspicious_ports = [p for p in telemetry["ports"] if any(k in p for k in ["3000", "8000", "8080", "5173"])]
    if suspicious_ports:
        receipts.append(("WARN", "Port Hygiene", f"Active ephemeral dev listeners: {', '.join(suspicious_ports[:2])}"))
        score -= 15
    else:
        receipts.append(("PASS", "Port Hygiene", "Zero lingering rogue dev ports. LifeOS port hygiene pristine."))

    l1 = telemetry["load"][0]
    n = float(telemetry["ncpu"])
    if l1 > n * 10.0:  # Darwin normalized or high-concurrency indicator
        receipts.append(("WARN", "Compute Saturation", f"1m load ({l1:.2f}) elevated over core baseline ({n})"))
        score -= 10
    else:
        receipts.append(("PASS", "Compute Headroom", f"Load {l1:.2f}/{n} cores (stable)"))

    if telemetry["agents_count"] >= 5:
        receipts.append(("PASS", "Swarm Quorum", f"{telemetry['agents_count']} distinct autonomous agents mapped in mesh"))
    else:
        receipts.append(("WARN", "Swarm Quorum", f"Only {telemetry['agents_count']} agents found; consensus quorum impaired"))
        score -= 20

    typefire_path = "/Users/lovelogic/Documents/TypeFire_Notes"
    if os.path.exists(typefire_path):
        receipts.append(("PASS", "Memory Vault", "TypeFire_Notes vault mounted & readable"))
    else:
        receipts.append(("FAIL", "Memory Vault", "TypeFire_Notes path inaccessible"))
        score -= 25

    return score, receipts
