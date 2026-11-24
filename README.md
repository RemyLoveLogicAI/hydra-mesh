# HYDRA-MESH (2027 Prototype)
> Distributed Multi-Channel Agent Hivemind, Disimage Terminal Cockpit & MCP Gateway

Built for **Remy / LoveLogicAI LLC** by **DevTheDude**.

---

## Capabilities Overview

1. **CLI & TUI (`hydra`)**:
   - `hydra status`: Disimage vector radar & live telemetry snapshot.
   - `hydra tui`: Interactive live-refreshing terminal cockpit.
   - `hydra audit`: Grokbot reality audit scoring (port hygiene, core saturation, quorum).
   - `hydra bridge`: Channel connection matrix (iMessage, Telegram, Slack, Discord, OpenBot).
   - `hydra mcp`: Stdio JSON-RPC 2.0 MCP server for Claude Code, Cursor, and Antigravity.
   - `hydra serve`: Local reactive WebUI server on `127.0.0.1:49200`.

2. **Disimage Protocol Engine (`hydra/disimage.py`)**:
   - Pure-Python zero-dependency PNG encoder (`zlib` + `struct`).
   - Supports **iTerm2 inline protocol**, **Kitty graphics protocol**, and **24-bit ANSI TrueColor Half-Block (`▀`) rasterization**.

3. **Multi-Channel Bridge (`hydra/bridge.py`)**:
   - Unified ingress router connecting iPhone iMessage (macOS JXA/AppleScript), Telegram, Slack, and OpenBot agents.

4. **MCP Server (`hydra/mcp_server.py`)**:
   - Standard tools: `get_swarm_status`, `run_skeptic_audit`, `dispatch_action`.

5. **Surfaces**:
   - **TUI**: Universal 24-bit TrueColor terminal cockpit.
   - **WebUI**: Reactive browser dashboard (`site/index.html`).
   - **iOS UI**: SwiftUI component for iPhone / iPad / iMessage Live Activities (`ios/HydraCockpitView.swift`).

---

## Quickstart

```bash
# Direct CLI execution
python3 -m hydra.cli status

# Grokbot Skeptic Reality Audit
python3 -m hydra.cli audit

# Run Interactive TUI
python3 -m hydra.cli tui --iterations 3

# Run Unit Tests
python3 -m unittest discover tests
```
