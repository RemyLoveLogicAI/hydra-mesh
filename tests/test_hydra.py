"""
Comprehensive Test Suite for HYDRA-MESH (v1.2.0)
Verifies:
1. Disimage PNG generation & valid header chunks
2. Disimage Half-block rasterizer dimensions & formatting
3. Disimage SVG vector export
4. Telemetry & Grokbot skeptic audit receipts
5. Hardened multi-channel bridge routing & live agent dispatch
6. MCP Server schema compliance & vector export tool
7. HydraDaemon single-shot heartbeat state emission
8. Triadic Consensus Engine deliberation & cryptographic ledger hash
"""

import unittest
import json
import os
from hydra.disimage import create_png, generate_swarm_radar_image, DisimageRenderer, generate_swarm_svg
from hydra.telemetry import get_system_telemetry, run_grokbot_audit
from hydra.bridge import HydraBridge, OPENBOT_AGENTS
from hydra.mcp_server import handle_request, TOOLS
from hydra.daemon import HydraDaemon, STATE_PATH
from hydra.consensus import DialecticalConsensusEngine

class TestHydraMesh(unittest.TestCase):

    def test_disimage_png_encoding(self):
        buf = generate_swarm_radar_image(width=32, height=16)
        png = create_png(width=32, height=16, rgb_buffer=buf)
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertIn(b"IHDR", png)
        self.assertIn(b"IDAT", png)
        self.assertIn(b"IEND", png)

    def test_disimage_half_block_rasterizer(self):
        buf = bytearray(10 * 10 * 3)
        res = DisimageRenderer.render_half_block(buf, width=10, height=10)
        lines = res.strip().split("\n")
        self.assertEqual(len(lines), 5)
        self.assertIn("\033[38;2;", lines[0])

    def test_disimage_svg_export(self):
        svg = generate_swarm_svg(600, 400)
        self.assertTrue(svg.startswith("<svg"))
        self.assertIn("REMY (CORE)", svg)
        self.assertIn("DevTheDude", svg)
        self.assertTrue(svg.strip().endswith("</svg>"))

    def test_telemetry_and_grokbot_audit(self):
        telem = get_system_telemetry()
        self.assertIn("cpu_brand", telem)
        self.assertIn("load", telem)
        self.assertIn("agents_count", telem)

        score, receipts = run_grokbot_audit(telem)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertGreater(len(receipts), 0)

    def test_hardened_bridge_and_agent_dispatch(self):
        bridge = HydraBridge()
        matrix = bridge.get_channel_matrix()
        self.assertIn("imessage", matrix)
        self.assertIn("telegram", matrix)
        self.assertIn("slack", matrix)

        # Agent dispatch test
        ipc = bridge.dispatch_to_agent("telegram", "sync status verification")
        self.assertEqual(ipc["target_agent"], "Telegram Orchestrator")
        self.assertEqual(ipc["delivery_status"], "delivered_to_mesh")

    def test_daemon_heartbeat_state(self):
        daemon = HydraDaemon()
        state = daemon.tick()
        self.assertIn("timestamp", state)
        self.assertIn("skeptic_score", state)
        self.assertIn("hardware", state)
        self.assertTrue(os.path.exists(STATE_PATH))

    def test_triadic_consensus_engine(self):
        engine = DialecticalConsensusEngine()
        receipt = engine.deliberate("RFC-001: Multi-Agent Mesh Topology")
        self.assertEqual(receipt["status"], "CONSENSUS_REACHED")
        self.assertTrue(len(receipt["ledger_hash"]) == 64)
        self.assertIn("thesis", receipt)
        self.assertIn("antithesis", receipt)
        self.assertIn("synthesis", receipt)

        md = engine.format_markdown_ledger(receipt)
        self.assertIn("# RFC: RFC-001: Multi-Agent Mesh Topology", md)
        self.assertIn(receipt["ledger_hash"], md)

    def test_mcp_server_protocol(self):
        init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize"}
        init_res = handle_request(init_req)
        self.assertEqual(init_res["result"]["serverInfo"]["name"], "hydra-mcp")

        tools_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
        tools_res = handle_request(tools_req)
        self.assertEqual(len(tools_res["result"]["tools"]), len(TOOLS))

if __name__ == "__main__":
    unittest.main()
