"""
HYDRA Model Context Protocol (MCP) Server (v2.0.0 Quantum)
Exposes tools:
- get_swarm_status: Live telemetry, roster, and kernel state
- run_skeptic_audit: Grokbot reality audit and port hygiene
- dispatch_action: Direct task injection into the hivemind
- export_topology_svg: Generates standalone SVG vector visualization of the swarm
- run_capability_auction: Executes autonomous Dutch auction for a task
- verify_merkle_flight_log: Verifies cryptographic integrity of the flight recorder
- run_nocturnal_synthesis: Generates counterfactual speculative mutations
"""

import sys
import json
from hydra.telemetry import get_system_telemetry, run_grokbot_audit
from hydra.bridge import HydraBridge
from hydra.disimage import generate_swarm_svg
from hydra.auction import CapabilityAuctionEngine
from hydra.flight_recorder import SwarmFlightRecorder
from hydra.dreamer import NocturnalSynthesisEngine

TOOLS = [
    {
        "name": "get_swarm_status",
        "description": "Returns live HYDRA-MESH telemetry, active Darwin hardware anchors, and OpenBot agent roster.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "include_ports": {"type": "boolean", "description": "Include listening ports list"}
            }
        }
    },
    {
        "name": "run_skeptic_audit",
        "description": "Executes Grokbot reality check verifying port hygiene, compute saturation, and memory vaults.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "dispatch_action",
        "description": "Dispatches an action or task through the HYDRA multi-channel event bridge.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target agent: DevTheDude, Telegram, Slack, Hermes"},
                "action": {"type": "string", "description": "Directive payload"}
            },
            "required": ["target", "action"]
        }
    },
    {
        "name": "export_topology_svg",
        "description": "Returns resolution-independent SVG vector diagram of the active agent swarm.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "width": {"type": "integer", "description": "Canvas width (default 600)"},
                "height": {"type": "integer", "description": "Canvas height (default 400)"}
            }
        }
    },
    {
        "name": "run_capability_auction",
        "description": "Executes autonomous capability Dutch auction across agents to determine optimal task lease.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "Task description to auction"}
            },
            "required": ["task"]
        }
    },
    {
        "name": "verify_merkle_flight_log",
        "description": "Verifies cryptographic integrity of the swarm's Merkle flight recorder.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "run_nocturnal_synthesis",
        "description": "Executes exploratory counterfactual hypothesis simulation cycle.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]

def handle_request(req: dict) -> dict:
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "hydra-mcp", "version": "2.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS}
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "get_swarm_status":
            telem = get_system_telemetry()
            if not args.get("include_ports", False):
                telem.pop("ports", None)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(telem, indent=2)}]}
            }
        elif tool_name == "run_skeptic_audit":
            telem = get_system_telemetry()
            score, receipts = run_grokbot_audit(telem)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps({"score": score, "receipts": receipts}, indent=2)
                    }]
                }
            }
        elif tool_name == "dispatch_action":
            bridge = HydraBridge()
            res = bridge.route_broadcast(sender="mcp_client", text=f"@{args.get('target')} {args.get('action')}")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        elif tool_name == "export_topology_svg":
            w = args.get("width", 600)
            h = args.get("height", 400)
            svg = generate_swarm_svg(width=w, height=h)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": svg}]}
            }
        elif tool_name == "run_capability_auction":
            engine = CapabilityAuctionEngine()
            res = engine.run_auction(args.get("task", "Generic Swarm Task"))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        elif tool_name == "verify_merkle_flight_log":
            recorder = SwarmFlightRecorder()
            res = recorder.verify_event_integrity()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        elif tool_name == "run_nocturnal_synthesis":
            dreamer = NocturnalSynthesisEngine()
            res = dreamer.run_dream_cycle()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {tool_name}"}
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Unhandled method: {method}"}
        }

def run_mcp_server():
    """Runs standard stdio JSON-RPC loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run_mcp_server()
