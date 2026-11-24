"""
Interactive Disimage Terminal User Interface (TUI)
Provides a live, refreshable terminal cockpit with telemetry and Disimage radar.
"""

import os
import sys
import time
from hydra.disimage import generate_swarm_radar_image, DisimageRenderer
from hydra.telemetry import get_system_telemetry, run_grokbot_audit

def run_tui(iterations: int = 1, delay: float = 0.5):
    """Executes live TUI refresh loop."""
    width, height = 72, 36
    tick = 0
    try:
        while True:
            rgb_buffer = generate_swarm_radar_image(width, height, pulse_tick=tick)
            telem = get_system_telemetry()
            score, receipts = run_grokbot_audit(telem)

            print("\033[2J\033[H", end="")
            print("\033[1;36m╔══════════════════════════════════════════════════════════════════════════════════════════╗\033[0m")
            print(f"\033[1;36m║\033[0m  \033[1;37mHYDRA COCKPIT TUI\033[0m │ \033[1;32mPULSE: {tick:04d}\033[0m │ \033[1;33mOPERATOR: REMY\033[0m │ \033[1;35mSWARM: 6 AGENTS\033[0m                  \033[1;36m║\033[0m")
            print("\033[1;36m╚══════════════════════════════════════════════════════════════════════════════════════════╝\033[0m")

            half_blocks = DisimageRenderer.render_half_block(rgb_buffer, width, height)
            for line in half_blocks.splitlines():
                print("  " + line)

            print(f"\033[1;34m── TELEMETRY ──\033[0m Load: {telem['load'][0]:.2f} │ Mem Free: {telem['free_mb']}MB │ Skeptic: \033[1;32m{score}/100\033[0m")
            print("\033[38;5;244mPress Ctrl+C to exit TUI.\033[0m")
            sys.stdout.flush()

            tick += 1
            if iterations > 0 and tick >= iterations:
                break
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n\033[0mExited HYDRA TUI.")
