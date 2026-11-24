"""
HYDRA CLI: Unified Command Line Interface (v2.0.0 Quantum)
Subcommands:
- status          : Display Disimage graphics and full telemetry snapshot
- tui             : Run live interactive terminal cockpit
- audit           : Execute Grokbot reality audit
- bridge          : Inspect multi-channel status & dispatch
- benchmark       : Run Disimage rasterizer performance benchmark
- export          : Export swarm topology as PNG or SVG vector file
- daemon          : Run persistent background observer daemon
- consensus       : Run triadic dialectic consensus deliberation on an RFC
- auction         : Run autonomous capability Dutch auction for a task
- flight-recorder : Verify Merkle tree integrity of swarm event logs
- dream           : Run nocturnal counterfactual hypothesis simulation
- mcp             : Run stdio JSON-RPC MCP server
- serve           : Run local WebUI dashboard
"""

import sys
import time
import argparse
import json
from hydra.disimage import generate_swarm_radar_image, DisimageRenderer, create_png, generate_swarm_svg
from hydra.telemetry import get_system_telemetry, run_grokbot_audit
from hydra.bridge import HydraBridge
from hydra.tui import run_tui
from hydra.webui import serve_webui
from hydra.mcp_server import run_mcp_server
from hydra.daemon import run_daemon
from hydra.consensus import DialecticalConsensusEngine
from hydra.auction import CapabilityAuctionEngine
from hydra.flight_recorder import SwarmFlightRecorder
from hydra.dreamer import NocturnalSynthesisEngine

def cmd_status(args):
    width, height = 72, 36
    telem = get_system_telemetry()
    score, receipts = run_grokbot_audit(telem)
    rgb_buffer = generate_swarm_radar_image(width, height, pulse_tick=9)

    print("\033[1;36m╔══════════════════════════════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[1;36m║\033[0m  \033[1;37mHYDRA-MESH v2.0-QUANTUM\033[0m │ \033[1;32mSTATUS: ACTIVE\033[0m │ \033[1;33mOPERATOR: REMY\033[0m │ \033[1;35mARM64 M4\033[0m                   \033[1;36m║\033[0m")
    print("\033[1;36m╚══════════════════════════════════════════════════════════════════════════════════════════╝\033[0m")

    print("\033[1;35m[DISIMAGE TOPOLOGY RADAR & QUANTUM ORBITALS]\033[0m")
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
    if args.dispatch:
        res = bridge.dispatch_to_agent(args.dispatch[0], args.dispatch[1])
        print(json.dumps(res, indent=2))
    else:
        matrix = bridge.get_channel_matrix()
        print(json.dumps(matrix, indent=2))

def cmd_auction(args):
    engine = CapabilityAuctionEngine()
    task = args.task or "Refactor Disimage IPC to POSIX Shared Memory"
    res = engine.run_auction(task)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"\033[1;36m[CAPABILITY AUCTION]\033[0m Task: {res['task']}")
        print(f"  \033[1mWinning Agent:\033[0m \033[1;32m{res['winning_agent']}\033[0m ({res['winning_agent_id']})")
        print(f"  \033[1mLease Hash:\033[0m \033[38;5;244m{res['lease_hash']}\033[0m")
        print(f"  \033[1mBid Score:\033[0m {res['winning_bid']['bid_score']} (Est Latency: {res['winning_bid']['est_latency_ms']}ms, Cost: {res['winning_bid']['est_tokens']}t)")
        print("\n\033[1;34m── Competing Bids ──\033[0m")
        for b in res["competing_bids"]:
            print(f"  • {b['agent']:<22} : Score {b['bid_score']:<6} | Affinity {b['affinity']} | Latency {b['est_latency_ms']}ms")

def cmd_flight_recorder(args):
    recorder = SwarmFlightRecorder()
    if args.record:
        entry = recorder.record_event("OPERATOR_INSTRUCTION", "Remy", {"instruction": args.record})
        print(f"\033[1;32m✓ Recorded Event:\033[0m {entry['leaf_hash']}")
    report = recorder.verify_event_integrity()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        badge = "\033[1;42;30m SECURE \033[0m" if report["status"] == "VERIFIED_SECURE" else "\033[1;41;37m TAMPERED \033[0m"
        print(f"{badge} Merkle Flight Log: {report['valid_events']}/{report['total_events']} events valid ({report['integrity_percent']}%)")
        print(f"  \033[1mMerkle Root:\033[0m \033[1;33m{report['merkle_root']}\033[0m")

def cmd_dream(args):
    dreamer = NocturnalSynthesisEngine()
    report = dreamer.run_dream_cycle()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(dreamer.format_digest(report))

def cmd_benchmark(args):
    frames = args.frames
    print(f"\033[1;36m[HYDRA BENCHMARK]\033[0m Running {frames} frames through Disimage Rasterizer...")
    t0 = time.perf_counter()
    for tick in range(frames):
        buf = generate_swarm_radar_image(72, 36, pulse_tick=tick)
        png = create_png(72, 36, buf)
        art = DisimageRenderer.render_half_block(buf, 72, 36)
    t1 = time.perf_counter()
    elapsed = t1 - t0
    fps = frames / elapsed
    ms_frame = (elapsed / frames) * 1000
    print(f"\033[1;32m✓ COMPLETED\033[0m in {elapsed:.4f}s ({fps:.1f} FPS, {ms_frame:.2f} ms/frame)")

def cmd_export(args):
    if args.format == "svg":
        svg_content = generate_swarm_svg()
        if args.output:
            with open(args.output, "w") as f:
                f.write(svg_content)
            print(f"\033[1;32m✓ Exported SVG to {args.output}\033[0m")
        else:
            print(svg_content)
    elif args.format == "png":
        buf = generate_swarm_radar_image(160, 80)
        png = create_png(160, 80, buf)
        out_path = args.output or "hydra_swarm.png"
        with open(out_path, "wb") as f:
            f.write(png)
        print(f"\033[1;32m✓ Exported PNG ({len(png)} bytes) to {out_path}\033[0m")

def cmd_daemon(args):
    run_daemon(interval=args.interval, once=args.once)

def cmd_consensus(args):
    topic = args.topic or "Decentralized Swarm Task Allocation & Event Ingress Protocol (2027)"
    engine = DialecticalConsensusEngine()
    receipt = engine.deliberate(topic)
    if args.json:
        print(json.dumps(receipt, indent=2))
    else:
        print(engine.format_markdown_ledger(receipt))

def cmd_tui(args):
    run_tui(iterations=args.iterations, delay=args.delay)

def cmd_serve(args):
    serve_webui(port=args.port)

def cmd_mcp(args):
    run_mcp_server()

def main():
    parser = argparse.ArgumentParser(prog="hydra", description="HYDRA-MESH CLI & Disimage Terminal Cockpit v2.0")
    sub = parser.add_subparsers(dest="command", help="Subcommand to execute")

    p_status = sub.add_parser("status", help="Show full Disimage graphics & status snapshot")
    p_status.set_defaults(func=cmd_status)

    p_audit = sub.add_parser("audit", help="Run Grokbot reality check & port audit")
    p_audit.add_argument("--json", action="store_true", help="Output as JSON")
    p_audit.set_defaults(func=cmd_audit)

    p_bridge = sub.add_parser("bridge", help="Inspect multi-channel connection matrix or dispatch message")
    p_bridge.add_argument("--dispatch", nargs=2, metavar=("AGENT", "MSG"), help="Dispatch message to agent")
    p_bridge.set_defaults(func=cmd_bridge)

    p_auction = sub.add_parser("auction", help="Run autonomous capability Dutch auction for a task")
    p_auction.add_argument("--task", help="Task description to auction")
    p_auction.add_argument("--json", action="store_true", help="Output as JSON")
    p_auction.set_defaults(func=cmd_auction)

    p_fr = sub.add_parser("flight-recorder", help="Verify Merkle flight log or record an event")
    p_fr.add_argument("--record", help="Record an event into the flight log")
    p_fr.add_argument("--json", action="store_true", help="Output as JSON")
    p_fr.set_defaults(func=cmd_flight_recorder)

    p_dream = sub.add_parser("dream", help="Run nocturnal counterfactual hypothesis simulation")
    p_dream.add_argument("--json", action="store_true", help="Output as JSON")
    p_dream.set_defaults(func=cmd_dream)

    p_bench = sub.add_parser("benchmark", help="Run Disimage rasterizer performance benchmark")
    p_bench.add_argument("--frames", type=int, default=100, help="Frames to render")
    p_bench.set_defaults(func=cmd_benchmark)

    p_export = sub.add_parser("export", help="Export topology diagram to file (SVG/PNG)")
    p_export.add_argument("--format", choices=["svg", "png"], default="svg", help="Export format")
    p_export.add_argument("-o", "--output", help="Target output file path")
    p_export.set_defaults(func=cmd_export)

    p_daemon = sub.add_parser("daemon", help="Run persistent background observer daemon")
    p_daemon.add_argument("--interval", type=float, default=3.0, help="Heartbeat interval in seconds")
    p_daemon.add_argument("--once", action="store_true", help="Run a single heartbeat and exit")
    p_daemon.set_defaults(func=cmd_daemon)

    p_consensus = sub.add_parser("consensus", help="Run triadic dialectic consensus deliberation on an RFC")
    p_consensus.add_argument("--topic", help="RFC topic to deliberate")
    p_consensus.add_argument("--json", action="store_true", help="Output as raw JSON receipt")
    p_consensus.set_defaults(func=cmd_consensus)

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
