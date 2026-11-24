"""
Comprehensive Test Suite for HYDRA-MESH v2.0-QUANTUM
Verifies:
1. Disimage PNG generation & valid header chunks
2. Disimage Half-block rasterizer dimensions & formatting
3. Disimage SVG vector export
4. Telemetry & Grokbot skeptic audit receipts
5. Hardened multi-channel bridge routing & live agent dispatch
6. MCP Server schema compliance & 7 quantum tools
7. HydraDaemon single-shot heartbeat state emission
8. Triadic Consensus Engine deliberation & cryptographic ledger hash
9. Autonomous Capability Dutch Auction bidding & lease contract
10. Merkle Flight Recorder event appending & cryptographic root proof
11. Nocturnal Synthesis Engine counterfactual hypothesis ranking
"""

import unittest
import json
import os
from hydra.disimage import create_png, generate_swarm_radar_image, DisimageRenderer, generate_swarm_svg
from hydra.telemetry import get_system_telemetry, run_grokbot_audit
from hydra.bridge import HydraBridge
from hydra.mcp_server import handle_request, TOOLS
from hydra.daemon import HydraDaemon, STATE_PATH
from hydra.consensus import DialecticalConsensusEngine
from hydra.auction import CapabilityAuctionEngine
from hydra.flight_recorder import SwarmFlightRecorder, MerkleTree
from hydra.dreamer import NocturnalSynthesisEngine

class TestHydraMeshQuantum(unittest.TestCase):

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
        score, receipts = run_grokbot_audit(telem)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_hardened_bridge_and_agent_dispatch(self):
        bridge = HydraBridge()
        ipc = bridge.dispatch_to_agent("telegram", "sync status verification")
        self.assertEqual(ipc["target_agent"], "Telegram Orchestrator")
        self.assertEqual(ipc["delivery_status"], "delivered_to_mesh")

    def test_daemon_heartbeat_state(self):
        daemon = HydraDaemon()
        state = daemon.tick()
        self.assertIn("timestamp", state)
        self.assertIn("skeptic_score", state)
        self.assertTrue(os.path.exists(STATE_PATH))

    def test_triadic_consensus_engine(self):
        engine = DialecticalConsensusEngine()
        receipt = engine.deliberate("RFC-002: Kernel Sharding")
        self.assertEqual(receipt["status"], "CONSENSUS_REACHED")
        self.assertEqual(len(receipt["ledger_hash"]), 64)
        md = engine.format_markdown_ledger(receipt)
        self.assertIn("# RFC: RFC-002: Kernel Sharding", md)

    def test_capability_auction_engine(self):
        engine = CapabilityAuctionEngine()
        res = engine.run_auction("Refactor kernel IPC architecture")
        self.assertEqual(res["status"], "LEASE_AWARDED")
        self.assertEqual(res["winning_agent"], "DevTheDude")
        self.assertEqual(len(res["lease_hash"]), 64)
        self.assertEqual(len(res["competing_bids"]), 5)

    def test_merkle_flight_recorder(self):
        recorder = SwarmFlightRecorder()
        entry = recorder.record_event("TEST_EVENT", "DevTheDude", {"test": True})
        self.assertEqual(len(entry["leaf_hash"]), 64)

        report = recorder.verify_event_integrity()
        self.assertIn(report["status"], ["VERIFIED_SECURE", "CORRUPTION_DETECTED"])
        self.assertEqual(len(report["merkle_root"]), 64)

    def test_nocturnal_synthesis_engine(self):
        dreamer = NocturnalSynthesisEngine()
        report = dreamer.run_dream_cycle()
        self.assertEqual(report["status"], "FRONTIER_OPTIMIZATION_IDENTIFIED")
        self.assertGreater(len(report["ranked_hypotheses"]), 0)
        self.assertEqual(len(report["dream_proof_hash"]), 64)
        digest = dreamer.format_digest(report)
        self.assertIn("HYDRA Nocturnal Synthesis Report", digest)

    def test_mcp_server_protocol(self):
        init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize"}
        init_res = handle_request(init_req)
        self.assertEqual(init_res["result"]["serverInfo"]["name"], "hydra-mcp")

        tools_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
        tools_res = handle_request(tools_req)
        self.assertEqual(len(tools_res["result"]["tools"]), 7)

    def test_merkle_inclusion_proof_verification(self):
        from hydra.flight_recorder import sha256_hex
        leaves = [sha256_hex(f"leaf_{i}") for i in range(7)]
        tree = MerkleTree(leaves)
        self.assertEqual(len(tree.root), 64)
        for i in range(len(leaves)):
            proof = tree.get_inclusion_proof(i)
            self.assertTrue(MerkleTree.verify_inclusion_proof(leaves[i], proof, tree.root))
        # Tampered leaf should fail verification
        tampered_leaf = sha256_hex("tampered_leaf")
        self.assertFalse(MerkleTree.verify_inclusion_proof(tampered_leaf, proof, tree.root))

    def test_disimage_compressed_half_block_rasterizer(self):
        buf = generate_swarm_radar_image(width=16, height=8)
        res = DisimageRenderer.render_half_block(buf, width=16, height=8)
        self.assertTrue(res.endswith("\033[0m\n"))
        self.assertIn("▀", res)
        # Verify line count
        lines = res.strip().split("\n")
        self.assertEqual(len(lines), 4)

if __name__ == "__main__":
    unittest.main()
