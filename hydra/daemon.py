"""
HYDRA Background Daemon (hydrad)
Continuous background observer monitoring Darwin kernel metrics, M4 core saturation,
ephemeral port hygiene, and active agent mesh quorum.
Emits atomic heartbeat state to /Users/lovelogic/OpenBot/Shared/hydra_daemon_state.json.
"""

import os
import sys
import time
import signal
import json
from typing import Dict, Any
from hydra.telemetry import get_system_telemetry, run_grokbot_audit
from hydra.bridge import HydraBridge

STATE_PATH = "/Users/lovelogic/OpenBot/Shared/hydra_daemon_state.json"

class HydraDaemon:
    def __init__(self, interval: float = 3.0):
        self.interval = interval
        self.running = True
        self.bridge = HydraBridge()

    def handle_signal(self, signum, frame):
        self.running = False

    def tick(self) -> Dict[str, Any]:
        """Executes a single monitoring heartbeat."""
        telemetry = get_system_telemetry()
        score, receipts = run_grokbot_audit(telemetry)
        channel_matrix = self.bridge.get_channel_matrix()

        state = {
            "timestamp": time.time(),
            "status": "HEALTHY" if score >= 80 else "DEGRADED",
            "skeptic_score": score,
            "receipts": receipts,
            "hardware": {
                "cpu": telemetry["cpu_brand"],
                "cores": telemetry["ncpu"],
                "load": telemetry["load"],
                "free_mb": telemetry["free_mb"]
            },
            "swarm": {
                "active_agents": telemetry["agents_count"],
                "channel_matrix": channel_matrix
            }
        }

        # Write atomic state (write to temp then rename)
        tmp_path = STATE_PATH + ".tmp"
        try:
            with open(tmp_path, "w") as f:
                json.dump(state, f, indent=2)
            os.replace(tmp_path, STATE_PATH)
        except Exception as e:
            pass

        return state

    def run(self, once: bool = False):
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        if once:
            return self.tick()

        print(f"\033[1;32m[HYDRAD]\033[0m Daemon started. Monitoring interval: {self.interval}s")
        print(f"\033[1;32m[HYDRAD]\033[0m State file: {STATE_PATH}")
        while self.running:
            self.tick()
            time.sleep(self.interval)
        print("\n\033[1;33m[HYDRAD]\033[0m Daemon cleanly terminated.")

def run_daemon(interval: float = 3.0, once: bool = False):
    daemon = HydraDaemon(interval=interval)
    return daemon.run(once=once)

if __name__ == "__main__":
    once = "--once" in sys.argv
    run_daemon(once=once)
