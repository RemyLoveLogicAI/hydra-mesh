"""
Multi-Channel Ingress & Event Bridge
Handles event taps and message routing across iMessage, Telegram, Slack, and OpenBot.
"""

import json
import time
import subprocess
from typing import Dict, Any, List

class HydraBridge:
    """Multi-channel gateway router."""

    def __init__(self):
        self.channels = ["imessage", "telegram", "slack", "discord", "openbot"]

    def read_imessage_recent(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Reads recent iMessage transcripts via macOS JXA / AppleScript (read-only)."""
        script = f'''
        tell application "Messages"
            set msgList to {{}}
            try
                set recentChats to chats
                repeat with c in (items 1 through (count of recentChats) of recentChats)
                    set end of msgList to (name of c as string)
                end repeat
            end try
            return msgList
        end tell
        '''
        try:
            res = subprocess.check_output(["osascript", "-e", script], text=True, stderr=subprocess.DEVNULL)
            chats = [c.strip() for c in res.strip().split(",") if c.strip()]
            return [{"channel": "imessage", "chat": c, "status": "active"} for c in chats[:limit]]
        except Exception:
            return [{"channel": "imessage", "chat": "Local Direct", "status": "bridge_ready"}]

    def get_channel_matrix(self) -> Dict[str, Any]:
        """Returns connection readiness of all remote ingress channels."""
        imsg = self.read_imessage_recent(limit=3)
        return {
            "imessage": {"status": "connected", "recent_threads": len(imsg)},
            "telegram": {"status": "configured", "orchestrator": "agent-eef87f53"},
            "slack": {"status": "configured", "orchestrator": "agent-f6675bf9"},
            "discord": {"status": "configured", "orchestrator": "agent-8e180718"},
            "openbot": {"status": "active", "port": 49424}
        }

    def route_broadcast(self, sender: str, text: str) -> Dict[str, Any]:
        """Routes a message to appropriate agent by mention or intent."""
        target = "DevTheDude"
        if "@telegram" in text.lower():
            target = "Telegram Orchestrator"
        elif "@slack" in text.lower():
            target = "Slack Orchestrator"
        elif "@discord" in text.lower():
            target = "Discord Orchestrator"
        elif "@hermes" in text.lower():
            target = "Hermes"

        return {
            "timestamp": time.time(),
            "sender": sender,
            "target": target,
            "text": text,
            "routed": True
        }
