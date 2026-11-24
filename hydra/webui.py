"""
Lightweight Reactive WebUI Server
Serves the HYDRA HTML dashboard and SSE / JSON-RPC live telemetry stream.
Follows LifeOS Port Hygiene: designed for ephemeral on-demand viewing or static bundling.
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from hydra.telemetry import get_system_telemetry, run_grokbot_audit

SITE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "site")

class HydraWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            index_path = os.path.join(SITE_DIR, "index.html")
            if os.path.exists(index_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(index_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Site not found")
        elif self.path == "/api/telemetry":
            telem = get_system_telemetry()
            score, receipts = run_grokbot_audit(telem)
            payload = {"telemetry": telem, "score": score, "receipts": receipts}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        pass  # Quiet logging

def serve_webui(port: int = 49200):
    """Starts the WebUI server."""
    server = HTTPServer(("127.0.0.1", port), HydraWebHandler)
    print(f"\033[1;32m[HYDRA WEBUI]\033[0m Live at http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[HYDRA WEBUI] Stopped.")
        server.server_close()
