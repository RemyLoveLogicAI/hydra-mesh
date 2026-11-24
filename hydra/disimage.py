"""
Disimage Terminal Graphics Engine
Pure-Python 24-bit TrueColor rasterizer, PNG stream encoder, and SVG vector generator.
Supports iTerm2 inline images, Kitty graphics protocol, and ANSI Half-block fallback.
"""

import math
import zlib
import struct
import base64
from typing import Dict, Any, List

def create_png(width: int, height: int, rgb_buffer: bytearray) -> bytes:
    """Encodes raw RGB bytearray (width * height * 3) into valid PNG bytes."""
    raw_scanlines = bytearray()
    row_bytes = width * 3
    for y in range(height):
        raw_scanlines.append(0)  # Filter type 0 (None)
        start = y * row_bytes
        raw_scanlines.extend(rgb_buffer[start:start + row_bytes])

    compressed = zlib.compress(bytes(raw_scanlines), 9)

    def png_chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += png_chunk(b"IDAT", compressed)
    png += png_chunk(b"IEND", b"")
    return png


class DisimageRenderer:
    """Multi-protocol terminal graphics engine."""

    @staticmethod
    def render_iterm2(png_bytes: bytes) -> str:
        b64 = base64.b64encode(png_bytes).decode('ascii')
        return f"\033]1337;File=inline=1;width=auto;height=auto:{b64}\a\n"

    @staticmethod
    def render_kitty(png_bytes: bytes, width: int, height: int) -> str:
        b64 = base64.b64encode(png_bytes).decode('ascii')
        return f"\033_Ga=T,f=100,s={width},v={height},m=0;{b64}\033\\\n"

    @staticmethod
    def render_half_block(rgb_buffer: bytearray, width: int, height: int) -> str:
        """Universal 24-bit ANSI TrueColor half-block rasterizer with run-length color state compression."""
        out = []
        for y in range(0, height, 2):
            line = []
            cur_r1 = cur_g1 = cur_b1 = -1
            cur_r2 = cur_g2 = cur_b2 = -1
            row1_off = y * width * 3
            has_second = (y + 1 < height)
            row2_off = (y + 1) * width * 3 if has_second else 0

            for x in range(width):
                off1 = row1_off + x * 3
                r1, g1, b1 = rgb_buffer[off1], rgb_buffer[off1 + 1], rgb_buffer[off1 + 2]
                if has_second:
                    off2 = row2_off + x * 3
                    r2, g2, b2 = rgb_buffer[off2], rgb_buffer[off2 + 1], rgb_buffer[off2 + 2]
                else:
                    r2, g2, b2 = 0, 0, 0

                if r1 != cur_r1 or g1 != cur_g1 or b1 != cur_b1:
                    line.append(f"\033[38;2;{r1};{g1};{b1}m")
                    cur_r1, cur_g1, cur_b1 = r1, g1, b1

                if r2 != cur_r2 or g2 != cur_g2 or b2 != cur_b2:
                    line.append(f"\033[48;2;{r2};{g2};{b2}m")
                    cur_r2, cur_g2, cur_b2 = r2, g2, b2

                line.append("▀")

            line.append("\033[0m")
            out.append("".join(line))
        return "\n".join(out) + "\n"


def generate_swarm_radar_image(width: int = 72, height: int = 36, pulse_tick: int = 0) -> bytearray:
    """Synthesizes circular swarm radar buffer with interconnected agent nodes."""
    buffer = bytearray(width * height * 3)
    cx = width / 2.0
    cy = height / 2.0
    max_radius = min(cx, cy) - 2.0

    # Background grid
    for y in range(height):
        for x in range(width):
            idx = (y * width + x) * 3
            if x % 12 == 0 or y % 6 == 0:
                buffer[idx] = 15
                buffer[idx + 1] = 25
                buffer[idx + 2] = 38
            else:
                buffer[idx] = 5
                buffer[idx + 1] = 8
                buffer[idx + 2] = 14

    def set_pixel(px: float, py: float, r: int, g: int, b: int, alpha: float = 1.0):
        if 0 <= px < width and 0 <= py < height:
            idx = (int(py) * width + int(px)) * 3
            buffer[idx] = int(buffer[idx] * (1.0 - alpha) + r * alpha)
            buffer[idx + 1] = int(buffer[idx + 1] * (1.0 - alpha) + g * alpha)
            buffer[idx + 2] = int(buffer[idx + 2] * (1.0 - alpha) + b * alpha)

    def draw_circle(ox: float, oy: float, radius: float, r: int, g: int, b: int):
        steps = int(2 * math.pi * radius * 1.5) + 8
        for i in range(steps):
            theta = (i / steps) * 2 * math.pi
            px = ox + radius * math.cos(theta) * 1.8
            py = oy + radius * math.sin(theta)
            set_pixel(px, py, r, g, b, 0.75)

    for r_ratio in [0.3, 0.6, 0.9]:
        draw_circle(cx, cy, max_radius * r_ratio, 25, 55, 80)

    angle = (pulse_tick * 0.15) % (2 * math.pi)
    for dist in range(int(max_radius)):
        sx = cx + dist * math.cos(angle) * 1.8
        sy = cy + dist * math.sin(angle)
        set_pixel(sx, sy, 0, 255, 180, 0.5)

    nodes = [
        {"name": "REMY", "angle": 0, "dist": 0.0, "color": (255, 215, 0)},
        {"name": "DEV", "angle": -math.pi/2, "dist": 0.55, "color": (0, 255, 200)},
        {"name": "TEL", "angle": -math.pi/6, "dist": 0.75, "color": (0, 180, 255)},
        {"name": "SLK", "angle": math.pi/4, "dist": 0.75, "color": (224, 30, 90)},
        {"name": "DSC", "angle": 3*math.pi/4, "dist": 0.75, "color": (88, 101, 242)},
        {"name": "HER", "angle": 7*math.pi/6, "dist": 0.65, "color": (255, 140, 0)},
    ]

    for node in nodes:
        nx = cx + node["dist"] * max_radius * math.cos(node["angle"]) * 1.8
        ny = cy + node["dist"] * max_radius * math.sin(node["angle"])
        node["px"] = nx
        node["py"] = ny

        if node["dist"] > 0:
            for s in range(20):
                t = s / 20.0
                lx = cx + (nx - cx) * t
                ly = cy + (ny - cy) * t
                cr, cg, cb = node["color"]
                set_pixel(lx, ly, int(cr * 0.35), int(cg * 0.35), int(cb * 0.35), 0.45)

    outer = [n for n in nodes if n["dist"] > 0]
    for i in range(len(outer)):
        n1 = outer[i]
        n2 = outer[(i + 1) % len(outer)]
        for s in range(16):
            t = s / 16.0
            lx = n1["px"] + (n2["px"] - n1["px"]) * t
            ly = n1["py"] + (n2["py"] - n1["py"]) * t
            set_pixel(lx, ly, 40, 75, 100, 0.35)

    for node in nodes:
        nx, ny = node["px"], node["py"]
        cr, cg, cb = node["color"]
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                set_pixel(nx + dx, ny + dy, cr, cg, cb, 0.95)

    return buffer


def generate_swarm_svg(width: int = 600, height: int = 400) -> str:
    """Generates standalone resolution-independent SVG vector visualization of the swarm."""
    cx = width / 2.0
    cy = height / 2.0
    r_max = min(cx, cy) - 40

    nodes = [
        {"name": "REMY (CORE)", "x": cx, "y": cy, "color": "#ffd700", "role": "Operator"},
        {"name": "DevTheDude", "x": cx, "y": cy - r_max * 0.65, "color": "#00ffc8", "role": "Architect"},
        {"name": "Telegram Bot", "x": cx + r_max * 0.8, "y": cy - r_max * 0.35, "color": "#00b4ff", "role": "Mobile Ingress"},
        {"name": "Slack Bot", "x": cx + r_max * 0.7, "y": cy + r_max * 0.6, "color": "#e01e5a", "role": "Team Canvas"},
        {"name": "Discord Bot", "x": cx - r_max * 0.7, "y": cy + r_max * 0.6, "color": "#5865f2", "role": "Community"},
        {"name": "Hermes (Claw)", "x": cx - r_max * 0.8, "y": cy - r_max * 0.35, "color": "#ff8c00", "role": "Agent Presence"},
    ]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '<defs>',
        '  <radialGradient id="radarGlow" cx="50%" cy="50%" r="50%">',
        '    <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.12"/>',
        '    <stop offset="100%" stop-color="#07090e" stop-opacity="0"/>',
        '  </radialGradient>',
        '  <filter id="glow">',
        '    <feGaussianBlur stdDeviation="3" result="blur"/>',
        '    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        '  </filter>',
        '</defs>',
        f'<rect width="{width}" height="{height}" fill="#07090e"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r_max}" fill="url(#radarGlow)"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r_max * 0.35}" fill="none" stroke="rgba(0, 240, 255, 0.2)" stroke-dasharray="4 4"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r_max * 0.7}" fill="none" stroke="rgba(0, 240, 255, 0.2)" stroke-dasharray="4 4"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r_max}" fill="none" stroke="rgba(0, 240, 255, 0.35)"/>',
    ]

    # Star rays & mesh
    for i in range(1, len(nodes)):
        n = nodes[i]
        svg.append(f'<line x1="{cx}" y1="{cy}" x2="{n["x"]}" y2="{n["y"]}" stroke="rgba(0, 240, 255, 0.3)" stroke-width="1.5"/>')
        nxt = nodes[1] if i == len(nodes) - 1 else nodes[i + 1]
        svg.append(f'<line x1="{n["x"]}" y1="{n["y"]}" x2="{nxt["x"]}" y2="{nxt["y"]}" stroke="rgba(100, 200, 255, 0.15)" stroke-width="1"/>')

    # Nodes
    for n in nodes:
        svg.append(f'<circle cx="{n["x"]}" cy="{n["y"]}" r="8" fill="{n["color"]}" filter="url(#glow)"/>')
        svg.append(f'<text x="{n["x"]}" y="{n["y"] - 14}" fill="#e2e8f0" font-family="system-ui, monospace" font-size="11" font-weight="bold" text-anchor="middle">{n["name"]}</text>')
        svg.append(f'<text x="{n["x"]}" y="{n["y"] + 20}" fill="#94a3b8" font-family="system-ui, monospace" font-size="9" text-anchor="middle">{n["role"]}</text>')

    svg.append('</svg>')
    return "\n".join(svg)
