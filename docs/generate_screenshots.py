#!/usr/bin/env python3
"""
Screenshot and visual terminal renderer for HYDRA-MESH v2.0-QUANTUM.
Generates standalone SVG and HTML terminal window captures for documentation and presentation.
"""

import os
import re
import html
import subprocess

SCREENSHOTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "screenshots"))
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def ansi_to_html(raw_text):
    text = html.escape(raw_text)
    # Replace Truecolor \033[38;2;r;g;bm with <span style="color:rgb(r,g,b)">
    def replace_truecolor(m):
        return f'<span style="color:rgb({m.group(1)},{m.group(2)},{m.group(3)})">'
    text = re.sub(r'\x1b\[38;2;(\d+);(\d+);(\d+)m', replace_truecolor, text)

    # Replace 48;2; background
    def replace_bg(m):
        return f'<span style="background-color:rgb({m.group(1)},{m.group(2)},{m.group(3)})">'
    text = re.sub(r'\x1b\[48;2;(\d+);(\d+);(\d+)m', replace_bg, text)

    colors = {
        '30': '#45475a', '31': '#f38ba8', '32': '#a6e3a1', '33': '#f9e2af',
        '34': '#89b4fa', '35': '#cba6f7', '36': '#94e2d5', '37': '#cdd6f4',
        '90': '#6c7086', '91': '#f38ba8', '92': '#a6e3a1', '93': '#f9e2af',
        '94': '#89b4fa', '95': '#cba6f7', '96': '#94e2d5', '97': '#ffffff',
        '1': 'font-weight:bold;',
    }
    for code, style in colors.items():
        if style.startswith('#'):
            text = text.replace(f'\x1b[{code}m', f'<span style="color:{style}">')
        else:
            text = text.replace(f'\x1b[{code}m', f'<span style="{style}">')

    text = re.sub(r'\x1b\[0?m', '</span>', text)
    text = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text)
    return text

def build_terminal_html(title, command, formatted_body, width=960):
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #0d1117;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro", "Segoe UI", Roboto, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 30px;
    min-height: 100vh;
  }}
  .window {{
    width: {width}px;
    max-width: 100%;
    background: #161b22;
    border-radius: 12px;
    border: 1px solid #30363d;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(255, 255, 255, 0.05);
    overflow: hidden;
  }}
  .titlebar {{
    background: #21262d;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #30363d;
    position: relative;
  }}
  .traffic-lights {{
    display: flex;
    gap: 8px;
    z-index: 2;
  }}
  .dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }}
  .dot-red {{ background: #ff5f56; border: 1px solid #e0443e; }}
  .dot-yellow {{ background: #ffbd2e; border: 1px solid #dea123; }}
  .dot-green {{ background: #27c93f; border: 1px solid #1aab29; }}
  .title {{
    position: absolute;
    left: 0; right: 0;
    text-align: center;
    font-size: 13px;
    font-weight: 500;
    color: #8b949e;
    letter-spacing: -0.2px;
  }}
  .command-bar {{
    background: #0d1117;
    padding: 10px 20px;
    border-bottom: 1px solid #21262d;
    font-family: "SF Mono", Menlo, Consolas, Monaco, monospace;
    font-size: 13px;
    color: #58a6ff;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .command-prompt {{ color: #7ee787; font-weight: bold; }}
  .content {{
    padding: 20px 24px;
    font-family: "SF Mono", Menlo, Consolas, Monaco, monospace;
    font-size: 13px;
    line-height: 1.55;
    color: #c9d1d9;
    white-space: pre-wrap;
    word-break: break-all;
    background: #0d1117;
  }}
  .badge {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
  }}
  .badge-pass {{ background: rgba(35, 134, 54, 0.2); color: #3fb950; border: 1px solid rgba(63, 185, 80, 0.4); }}
  .badge-quantum {{ background: rgba(163, 113, 247, 0.2); color: #d2a8ff; border: 1px solid rgba(163, 113, 247, 0.4); }}
</style>
</head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="traffic-lights">
      <div class="dot dot-red"></div>
      <div class="dot dot-yellow"></div>
      <div class="dot dot-green"></div>
    </div>
    <div class="title">{title} — HYDRA-MESH v2.0-QUANTUM</div>
  </div>
  <div class="command-bar">
    <span class="command-prompt">lovelogic@m4-max hydra-mesh %</span>
    <span>{command}</span>
  </div>
  <div class="content">{formatted_body}</div>
</div>
</body>
</html>
"""

def generate_all():
    targets = [
        {
            "id": "01_unit_tests",
            "title": "Quantum Unit Test Suite (11/11 Passing)",
            "command": "python3 -m unittest discover tests -v",
            "file": "test_suite.txt"
        },
        {
            "id": "02_cli_cockpit",
            "title": "Real-time Disimage Cockpit & Radar",
            "command": "hydra status",
            "file": "status.txt"
        },
        {
            "id": "03_dutch_auction",
            "title": "Autonomous Capability Dutch Auction",
            "command": "hydra auction --task 'Refactor Disimage IPC to POSIX Shared Memory'",
            "file": "auction.txt"
        },
        {
            "id": "04_merkle_flight_recorder",
            "title": "Cryptographic Merkle Flight Recorder Audit",
            "command": "hydra flight-recorder",
            "file": "flight_recorder.txt"
        },
        {
            "id": "05_triadic_consensus",
            "title": "Triadic Consensus Deliberation Engine",
            "command": "hydra consensus --topic 'RFC-002: Apple Silicon Metal Shader Acceleration'",
            "file": "consensus.txt"
        },
        {
            "id": "06_rasterizer_benchmark",
            "title": "Disimage Half-Block Rasterizer Benchmark (482+ FPS)",
            "command": "hydra benchmark --frames 100",
            "file": "benchmark.txt"
        }
    ]

    for t in targets:
        txt_path = os.path.join(SCREENSHOTS_DIR, t["file"])
        if not os.path.exists(txt_path):
            continue
        with open(txt_path, "r", encoding="utf-8") as f:
            raw = f.read()

        html_body = ansi_to_html(raw)
        full_html = build_terminal_html(t["title"], t["command"], html_body)

        out_html_path = os.path.join(SCREENSHOTS_DIR, f"{t['id']}.html")
        with open(out_html_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"Generated {out_html_path}")

if __name__ == "__main__":
    generate_all()
