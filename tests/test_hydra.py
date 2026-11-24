"""
Comprehensive Test Suite for HYDRA-MESH
Verifies:
1. Disimage PNG generation & valid header chunks
2. Disimage Half-block rasterizer dimensions & formatting
3. Telemetry & Grokbot skeptic audit receipts
4. Multi-channel bridge routing logic
5. MCP Server schema compliance
"""

import unittest
import json
from hydra.disimage import create_png, generate_swarm_radar_image, DisimageRenderer
from hydra.telemetry import get_system_telemetry, run_grokbot_audit
from hydra.bridge import HydraBridge
from hydra.mcp_server import handle_request, TOOLS

class TestHydraMesh(unittest.TestCase):

    def test_disimage_png_encoding(self):
        """Verifies pure-Python PNG encoder produces valid PNG magic bytes and IHDR."""
        buf = generate_swarm_radar_image(width=32, height=16)
        png = create_png(width=32, height=16, rgb_buffer=buf)
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertIn(b"IHDR", png)
        self.assertIn(b"IDAT", png)
        self.assertIn(b"IEND", png)

    def test_disimage_half_block_rasterizer(self):
        """Verifies universal 24-bit ANSI half-block rasterizer output."""
        buf = bytearray(10 * 10 * 3)
        res = DisimageRenderer.render_half_block(buf, width=10, height=10)
        lines = res.strip().split("\n")
        self.assertEqual(len(lines), 5)  # 10 height / 2 = 5 half-block rows
        self.assertIn("\033[38;2;", lines[0])

    def test_telemetry_and_grokbot_audit(self):
        """Verifies telemetry collection and Grokbot audit scoring."""
        telem = get_system_telemetry()
        self.assertIn("cpu_brand", telem)
        self.assertIn("load", telem)
        self.assertIn("agents_count", telem)

        score, receipts = run_grokbot_audit(telem)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertGreater(len(receipts), 0)

    def test_bridge_routing(self):
        """Verifies multi-channel intent routing."""
        bridge = HydraBridge()
        matrix = bridge.get_channel_matrix()
        self.assertIn("imessage", matrix)
        self.assertIn("telegram", matrix)
        self.assertIn("slack", matrix)

        res = bridge.route_broadcast("remy", "@telegram deploy status check")
        self.assertEqual(res["target"], "Telegram Orchestrator")
        self.assertTrue(res["routed"])

    def test_mcp_server_protocol(self):
        """Verifies MCP JSON-RPC initialize and tool listing."""
        init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize"}
        init_res = handle_request(init_req)
        self.assertEqual(init_res["result"]["serverInfo"]["name"], "hydra-mcp")

        tools_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
        tools_res = handle_request(tools_req)
        self.assertEqual(len(tools_res["result"]["tools"]), len(TOOLS))

        call_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "run_skeptic_audit", "arguments": {}}
        }
        call_res = handle_request(call_req)
        self.assertIn("score", call_res["result"]["content"][0]["text"])

if __name__ == "__main__":
    unittest.main()
