"""
HYDRA CLI: Unified Command Line Interface
Subcommands:
- status   : Display Disimage graphics and full telemetry snapshot
- tui      : Run live interactive terminal cockpit
- audit    : Execute Grokbot reality audit
- bridge   : Inspect multi-channel status (iMessage, Telegram, Slack)
- mcp      : Run stdio JSON-RPC MCP server
- serve    : Run local WebUI dashboard
"""

import sys
import argparse
import json
from hydra.disimage import generate_swarm_radar_image, DisimageRenderer, create_png
from hydra.telemetry import get_system_telemetry, run_grokbot_audit
from hydra.bridge import HydraBridge
from hydra.tui import run_tui
from hydra.webui import serve_webui
from hydra.mcp_server import run_mcp_server

def cmd_status(args):
    width, height = 72, 36
    telem = get_system_telemetry()
    score, receipts = run_grokbot_audit(telem)
    rgb_buffer = generate_swarm_radar_image(width, height, pulse_tick=9)

    print("\033[1;36m╔══════════════════════════════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[1;36m║\033[0m  \033[1;37mHYDRA-MESH COCKPIT\033[0m │ \033[1;32mSTATUS: ACTIVE\033[0m │ \033[1;33mOPERATOR: REMY\033[0m │ \033[1;35mARM64 M4\033[0m                          \033[1;36m║\033[0m")
    print("\033[1;36m╚══════════════════════════════════════════════════════════════════════════════════════════╝\033[0m")

    print("\033[1;35m[DISIMAGE TOPOLOGY RADAR]\033[0m")
    half_blocks = DisimageRenderer.render_half_block(rgb_buffer, width, height)
    for line in half_blocks.splitlines():
        print("  " + line)

    print(f"\033[1;34m── TELEMETRY ──\033[0m {telem['cpu_brand']} • Load: {telem['load'][0]:.2f} • Agents: {telem['agents_count']}")
    print(f"\033[1;33m── GROKBOT AUDIT ──\033[0m Score: {score}/100")
    for st, cat, msg in receipts:
        badge = "PASS" if st == "PASS" else ("WARN" if st == "WARN" else "FAIL")
        print(f"  [{badge}] {cat:<18}: {msg}")

def cmd_audit(args):
    telem = get_system_telemetry()
    score, receipts = run_grokbot_audit(telem)
    out = {"score": score, "receipts": receipts, "telemetry": telem}
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"GROKBOT SKEPTIC SCORE: {score}/100")
        for st, cat, msg in receipts:
            print(f"[{st}] {cat}: {msg}")

def cmd_bridge(args):
    bridge = HydraBridge()
    matrix = bridge.get_channel_matrix()
    print(json.dumps(matrix, indent=2))

def cmd_tui(args):
    run_tui(iterations=args.iterations, delay=args.delay)

def cmd_serve(args):
    serve_webui(port=args.port)

def cmd_mcp(args):
    run_mcp_server()

def main():
    parser = argparse.ArgumentParser(prog="hydra", description="HYDRA-MESH CLI & Disimage Terminal Cockpit")
    sub = parser.add_subparsers(dest="command", help="Subcommand to execute")

    p_status = sub.add_parser("status", help="Show full Disimage graphics & status snapshot")
    p_status.set_defaults(func=cmd_status)

    p_audit = sub.add_parser("audit", help="Run Grokbot reality check & port audit")
    p_audit.add_argument("--json", action="store_true", help="Output as JSON")
    p_audit.set_defaults(func=cmd_audit)

    p_bridge = sub.add_parser("bridge", help="Inspect multi-channel connection matrix")
    p_bridge.set_defaults(func=cmd_bridge)

    p_tui = sub.add_parser("tui", help="Launch interactive live TUI cockpit")
    p_tui.add_argument("--iterations", type=int, default=1, help="Max refresh iterations (0 for infinite)")
    p_tui.add_argument("--delay", type=float, default=0.5, help="Frame delay in seconds")
    p_tui.set_defaults(func=cmd_tui)

    p_serve = sub.add_parser("serve", help="Launch local WebUI server")
    p_serve.add_argument("--port", type=int, default=49200, help="HTTP port")
    p_serve.set_defaults(func=cmd_serve)

    p_mcp = sub.add_parser("mcp", help="Run stdio JSON-RPC MCP server")
    p_mcp.set_defaults(func=cmd_mcp)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        cmd_status(args)
    else:
        args.func(args)

if __name__ == "__main__":
    main()
