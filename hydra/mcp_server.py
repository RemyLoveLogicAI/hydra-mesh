"""
HYDRA Model Context Protocol (MCP) Server
Standard stdio JSON-RPC 2.0 MCP server for AI IDEs (Claude, Cursor, Gemini, Antigravity).
Exposes tools:
- get_swarm_status: Live telemetry, roster, and kernel state
- run_skeptic_audit: Grokbot reality audit and port hygiene
- dispatch_action: Direct task injection into the hivemind
"""

import sys
import json
from hydra.telemetry import get_system_telemetry, run_grokbot_audit
from hydra.bridge import HydraBridge

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
                "serverInfo": {"name": "hydra-mcp", "version": "1.0.0"}
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
