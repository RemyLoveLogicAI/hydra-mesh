#!/usr/bin/env python3
"""
HYDRA-MESH Gumroad MCP Server
-----------------------------
Stdio JSON-RPC 2.0 Model Context Protocol server providing typed tools
for Gumroad digital product creation, catalog management, and OAuth sales synchronization.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List

def get_token() -> str:
    return os.environ.get("GUMROAD_ACCESS_TOKEN", "").strip()

def call_gumroad(endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
    token = get_token()
    if not token:
        return {
            "success": False,
            "error": "GUMROAD_ACCESS_TOKEN not configured. Complete OAuth at the Composio auth link or set GUMROAD_ACCESS_TOKEN."
        }
    
    url = f"https://api.gumroad.com/v2/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "LoveLogicAI-HydraGumroadMCP/2.0"
    }
    
    encoded_data = None
    if data:
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return {"success": False, "http_code": e.code, "error": json.loads(body)}
        except Exception:
            return {"success": False, "http_code": e.code, "error": body}
    except Exception as e:
        return {"success": False, "error": str(e)}

TOOLS = [
    {
        "name": "gumroad_list_products",
        "description": "List all products in the authenticated Gumroad catalog.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "gumroad_get_product",
        "description": "Retrieve product details by product ID or permalink.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "Gumroad product ID"}
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "gumroad_create_product",
        "description": "Create a new digital product on Gumroad.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Product display title"},
                "price": {"type": "integer", "description": "Price in cents (e.g. 4900 for $49.00)"},
                "description": {"type": "string", "description": "Product description (Markdown or HTML)"},
                "custom_permalink": {"type": "string", "description": "Custom URL permalink slug"},
                "tags": {"type": "string", "description": "Comma-separated list of tags"},
                "custom_summary": {"type": "string", "description": "Short summary line"}
            },
            "required": ["name", "price"]
        }
    },
    {
        "name": "gumroad_get_sales",
        "description": "List successful sales transactions for the authenticated account.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {"type": "integer", "description": "Page number (minimum 1)", "default": 1}
            }
        }
    },
    {
        "name": "gumroad_oauth_status",
        "description": "Check whether Gumroad OAuth / API token is active and authorized.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]

def handle_rpc(request: Dict[str, Any]) -> Dict[str, Any]:
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "hydra-gumroad-mcp",
                    "version": "2.0.0"
                }
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS}
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "gumroad_oauth_status":
            token = get_token()
            res = {
                "configured": bool(token),
                "token_prefix": (token[:4] + "..." + token[-4:]) if len(token) > 8 else ("present" if token else "none"),
                "auth_provider": "OAuth via Composio / Environment"
            }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        elif name == "gumroad_list_products":
            res = call_gumroad("products")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        elif name == "gumroad_get_product":
            pid = args.get("product_id")
            res = call_gumroad(f"products/{pid}")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        elif name == "gumroad_create_product":
            res = call_gumroad("products", method="POST", data=args)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        elif name == "gumroad_get_sales":
            page = args.get("page", 1)
            res = call_gumroad(f"sales?page={page}")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {name} not found"}
            }
            
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid request"}
    }

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {e}"}
            }
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
