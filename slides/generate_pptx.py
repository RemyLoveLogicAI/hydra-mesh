#!/usr/bin/env python3
"""
Zero-dependency native PowerPoint (.pptx) generator for HYDRA-MESH v2.0-QUANTUM.
Builds an editable, multi-slide OpenXML presentation using pure Python standard library.
"""

import os
import zipfile

SLIDES_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_PPTX = os.path.join(SLIDES_DIR, "presentation.pptx")

# Slide dimensions in EMUs (16:9 widescreen: 12192000 x 6858000)
SLIDE_WIDTH = 12192000
SLIDE_HEIGHT = 6858000

SLIDE_DATA = [
    {
        "title": "HYDRA-MESH v2.0-QUANTUM",
        "subtitle": "Autonomous Multi-Agent Swarm Orchestration Engine",
        "bullets": [
            "Bleeding-Edge Multi-Agent Coordination Kernel for Apple Silicon M4",
            "Zero-External-Dependency Standard Library Mandate",
            "Algorithmic Capability Dutch Auctions & HMAC Lease Contracts",
            "Cryptographic Merkle Flight Recorder with 100% Integrity Proofs",
            "Shipped, Tested & Live on Web + GitHub + Gumroad"
        ]
    },
    {
        "title": "The Multi-Agent Coordination Crisis",
        "subtitle": "Why Traditional Agent Harnesses Fail at Scale",
        "bullets": [
            "Synchronous RPC Bottlenecks: Agents stall waiting for sequential turn round-trips.",
            "Unverifiable Execution: Flat text logs allow silent hallucination and state corruption.",
            "Naive Static Routing: Tasks assigned by heuristic rules instead of dynamic latency/cost fitness.",
            "Wheel Friction: Heavy external pip dependencies break during cross-platform deployment.",
            "The Solution: HYDRA-MESH micro-kernel with lockless POSIX IPC and cryptographic proofs."
        ]
    },
    {
        "title": "Autonomous Capability Dutch Auction",
        "subtitle": "Algorithmic Task Allocation Protocol (hydra.auction)",
        "bullets": [
            "Dynamic reverse bidding across 5 OpenBot satellite agents.",
            "Fitness Score: Weighted product of Domain Affinity, Execution Latency, and Token Cost.",
            "Algorithmic Settlement: Winning agent awarded in sub-15ms with zero human intervention.",
            "HMAC Lease Contracts: Cryptographically signed lease hash seals agent execution rights.",
            "Verified Run: DevTheDude claimed IPC refactor with score 6.44 and HMAC lease f951a1eb..."
        ]
    },
    {
        "title": "Cryptographic Merkle Flight Recorder",
        "subtitle": "Tamper-Proof Swarm Auditability (hydra.flight_recorder)",
        "bullets": [
            "Binary SHA-256 Merkle tree permanently accumulator-logging every inter-agent event.",
            "O(log N) Cryptographic Inclusion: Instant mathematical proof of any historical turn.",
            "Chain Tampering Immunity: Modifying any historical turn immediately invalidates the Merkle root.",
            "Active Root Accumulator: 8ac0b7cb900f2ed5e8b6cb0b4681939b0678724cb6d0d69fabeb770218cdd107",
            "100% Cryptographic Verification: Zero discrepancies detected across test & flight logs."
        ]
    },
    {
        "title": "Triadic Dialectical Consensus Protocol",
        "subtitle": "Consensus Before Execution (hydra.consensus)",
        "bullets": [
            "Stage 1 (Thesis): Architect agent (DevTheDude) submits proposed technical RFC.",
            "Stage 2 (Antithesis): Adversarial critic (Hermes / Skeptic Daemon) stresses failure modes.",
            "Stage 3 (Synthesis): Consensus Arbiter harmonizes objections into executable mandate.",
            "Signed Ledgers: Recorded RFC-001 (Distributed Ingress) and RFC-002 (Metal Acceleration).",
            "Zero Silent Flaws: Architectural compromises eliminated prior to git commits."
        ]
    },
    {
        "title": "Nocturnal Genetic Dreamer",
        "subtitle": "Autonomous Idle-Cycle Architecture Evolution (hydra.dreamer)",
        "bullets": [
            "Background genetic simulator operating during idle cycles without operator prompting.",
            "Counterfactual Permutations: Evaluates architectural mutations against fitness functions.",
            "Landmark Discovery MUT-003: Apple M4 Metal Shader Half-Block Rasterizer.",
            "Simulated Performance: 96.2% fitness score, projecting 1,200+ FPS terminal throughput.",
            "Self-Optimizing System: Generates verified hypothesis proofs for next engineering waves."
        ]
    },
    {
        "title": "Disimage TrueColor Rasterizer",
        "subtitle": "482.8 FPS Terminal Graphics & Silicon Optimization (hydra.disimage)",
        "bullets": [
            "Zero-Dependency ANSI 24-bit TrueColor rasterizer using Unicode half-blocks.",
            "Benchmark Throughput: 482.8 FPS (2.07 ms frame time) on Apple M4 Max 10-core silicon.",
            "Resolution-Independent Vector Export: Real-time SVG topology generation.",
            "Zero-Copy GC Optimization: Direct string buffer concatenation with zero heap churn.",
            "Multi-Surface Integration: Terminal stdout, web dashboard, and macOS status radar."
        ]
    },
    {
        "title": "Background Daemon & macOS Menu Bar",
        "subtitle": "Continuous System Telemetry & Launchd Integration (hydra.daemon)",
        "bullets": [
            "Native macOS Launchd Service: ai.lovelogic.hydrad.plist persistent background supervisor.",
            "Atomic Telemetry Heartbeats: Real-time JSON health state in shared memory.",
            "Executable Menu Bar Extra: BitBar / SwiftBar plugin displaying live swarm quorum & M4 load.",
            "GrokBot Safety Audit: System telemetry verification with zero credential leaks.",
            "Instant Operator Visibility: Swarm health visible at a glance in the macOS menu bar."
        ]
    },
    {
        "title": "Production Deployment & Commercial Release",
        "subtitle": "Shipped Across 5 Surfaces (v2.0.0-quantum)",
        "bullets": [
            "Global CLI Executables: ~/.local/bin/hydra and ~/.local/bin/hydrad in system $PATH.",
            "GitHub Repository: RemyLoveLogicAI/hydra-mesh with tagged releases v1.1.0, v1.2.0, v2.0.0.",
            "Live Web Documentation: Active on OpenBot Cloud with visual screenshot gallery.",
            "Model Context Protocol (MCP 2.0): 12 typed JSON-RPC tools for Claude, Gemini, and OpenBot.",
            "Commercial Gumroad Package: Ready for storefront launch with OAuth & automated publisher."
        ]
    }
]

def xml_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def generate_pptx():
    with zipfile.ZipFile(OUTPUT_PPTX, "w", zipfile.ZIP_DEFLATED) as zf:
        # [Content_Types].xml
        content_types = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
            '<Default Extension="xml" ContentType="application/xml"/>',
            '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>']
        for i in range(1, len(SLIDE_DATA) + 1):
            content_types.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
        content_types.append('</Types>')
        zf.writestr("[Content_Types].xml", "".join(content_types))

        # _rels/.rels
        zf.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
            '</Relationships>')

        # ppt/presentation.xml
        pres_xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">',
            f'<p:sldSz cx="{SLIDE_WIDTH}" cy="{SLIDE_HEIGHT}" type="screen16x9"/>',
            '<p:sldIdLst>']
        for i in range(1, len(SLIDE_DATA) + 1):
            pres_xml.append(f'<p:sldId id="{255 + i}" r:id="rId{i}"/>')
        pres_xml.append('</p:sldIdLst></p:presentation>')
        zf.writestr("ppt/presentation.xml", "".join(pres_xml))

        # ppt/_rels/presentation.xml.rels
        pres_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
        for i in range(1, len(SLIDE_DATA) + 1):
            pres_rels.append(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>')
        pres_rels.append('</Relationships>')
        zf.writestr("ppt/_rels/presentation.xml.rels", "".join(pres_rels))

        # ppt/slides/slide{i}.xml
        for idx, slide in enumerate(SLIDE_DATA, start=1):
            bullets_xml = []
            for b in slide["bullets"]:
                bullets_xml.append(f'''<a:p>
                    <a:pPr marL="288000" indent="-288000"/>
                    <a:r>
                        <a:rPr lang="en-US" sz="2200">
                            <a:solidFill><a:srgbClr val="E5E7EB"/></a:solidFill>
                        </a:rPr>
                        <a:t>• {xml_escape(b)}</a:t>
                    </a:r>
                </a:p>''')
            bullets_str = "".join(bullets_xml)

            slide_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
    <p:cSld>
        <p:spTree>
            <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
            <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
            
            <p:sp>
                <p:nvSpPr><p:cNvPr id="2" name="Background"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
                <p:spPr>
                    <a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_WIDTH}" cy="{SLIDE_HEIGHT}"/></a:xfrm>
                    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                    <a:solidFill><a:srgbClr val="090D16"/></a:solidFill>
                </p:spPr>
            </p:sp>

            <p:sp>
                <p:nvSpPr><p:cNvPr id="3" name="TitleBox"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
                <p:spPr>
                    <a:xfrm><a:off x="800000" y="600000"/><a:ext cx="10592000" cy="1400000"/></a:xfrm>
                    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                    <a:noFill/>
                </p:spPr>
                <p:txBody>
                    <a:bodyPr rtlCol="0" anchor="t"/>
                    <a:p>
                        <a:r>
                            <a:rPr lang="en-US" sz="3600" b="1">
                                <a:solidFill><a:srgbClr val="00F0FF"/></a:solidFill>
                            </a:rPr>
                            <a:t>{xml_escape(slide["title"])}</a:t>
                        </a:r>
                    </a:p>
                    <a:p>
                        <a:r>
                            <a:rPr lang="en-US" sz="1800">
                                <a:solidFill><a:srgbClr val="9CA3AF"/></a:solidFill>
                            </a:rPr>
                            <a:t>{xml_escape(slide["subtitle"])}</a:t>
                        </a:r>
                    </a:p>
                </p:txBody>
            </p:sp>

            <p:sp>
                <p:nvSpPr><p:cNvPr id="4" name="ContentBox"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
                <p:spPr>
                    <a:xfrm><a:off x="800000" y="2100000"/><a:ext cx="10592000" cy="4200000"/></a:xfrm>
                    <a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>
                    <a:solidFill><a:srgbClr val="111827"/></a:solidFill>
                    <a:ln w="12700"><a:solidFill><a:srgbClr val="1F293D"/></a:solidFill></a:ln>
                </p:spPr>
                <p:txBody>
                    <a:bodyPr rtlCol="0" lIns="360000" tIns="360000" rIns="360000" bIns="360000" anchor="t"/>
                    {bullets_str}
                </p:txBody>
            </p:sp>

            <p:sp>
                <p:nvSpPr><p:cNvPr id="5" name="Footer"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
                <p:spPr>
                    <a:xfrm><a:off x="800000" y="6400000"/><a:ext cx="10592000" cy="300000"/></a:xfrm>
                    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                    <a:noFill/>
                </p:spPr>
                <p:txBody>
                    <a:bodyPr rtlCol="0" anchor="b"/>
                    <a:p>
                        <a:r>
                            <a:rPr lang="en-US" sz="1200">
                                <a:solidFill><a:srgbClr val="4B5563"/></a:solidFill>
                            </a:rPr>
                            <a:t>HYDRA-MESH v2.0-QUANTUM │ Slide {idx} of {len(SLIDE_DATA)} │ LoveLogicAI LLC</a:t>
                        </a:r>
                    </a:p>
                </p:txBody>
            </p:sp>
        </p:spTree>
    </p:cSld>
</p:sld>'''
            zf.writestr(f"ppt/slides/slide{idx}.xml", slide_xml)

    print(f"Generated {OUTPUT_PPTX} ({os.path.getsize(OUTPUT_PPTX)} bytes)")

if __name__ == "__main__":
    generate_pptx()
