#!/usr/bin/env python3
"""
HYDRA-MESH v2.0-QUANTUM — Automated Gumroad Product Publisher
-------------------------------------------------------------
Publishes or stages HYDRA-MESH as a digital product on Gumroad using the Gumroad API v2.
If GUMROAD_ACCESS_TOKEN is present in the environment or passed via --token, creates/updates
the product directly. Otherwise, prints formatted cURL commands and web listing payloads.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

LISTING_JSON = Path(__file__).parent / "listing.json"
LISTING_MD = Path(__file__).parent / "GUMROAD_LISTING.md"
DIST_DIR = Path(__file__).parent.parent / "dist"
ARCHIVE_PATH = DIST_DIR / "hydra-mesh-2.0.0.tar.gz"

def load_payload():
    if not LISTING_JSON.exists():
        print(f"Error: {LISTING_JSON} not found.", file=sys.stderr)
        sys.exit(1)
    with open(LISTING_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["product"]

def read_markdown_description():
    if LISTING_MD.exists():
        return LISTING_MD.read_text(encoding="utf-8")
    return "HYDRA-MESH v2.0-QUANTUM Distributed Agent Hivemind"

def publish_to_gumroad(token: str, payload: dict):
    print("🚀 Connecting to Gumroad API (v2)...")
    url = "https://api.gumroad.com/v2/products"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "LoveLogicAI-HydraPublisher/2.0"
    }
    
    form_data = {
        "name": payload["name"],
        "price": payload["price_cents"],
        "description": read_markdown_description(),
        "custom_permalink": payload["permalink"],
        "custom_receipt": payload["custom_receipt"],
        "custom_summary": payload["custom_summary"],
        "tags": ",".join(payload["tags"]),
        "currency": payload.get("currency", "usd")
    }
    
    encoded_data = urllib.parse.urlencode(form_data).encode("utf-8")
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            if resp_data.get("success"):
                product = resp_data.get("product", {})
                short_url = product.get("short_url") or f"https://gumroad.com/l/{payload['permalink']}"
                print("\n✅ Successfully published product to Gumroad!")
                print(f"🔗 Live URL: {short_url}")
                print(f"🆔 Product ID: {product.get('id')}")
                return product
            else:
                print(f"❌ Gumroad API returned failure: {resp_data}", file=sys.stderr)
                return None
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"❌ HTTP Error {e.code}: {err_msg}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error communicating with Gumroad API: {e}", file=sys.stderr)
        return None

def print_manual_instructions(payload: dict):
    print("\n" + "=" * 70)
    print("📦 HYDRA-MESH v2.0-QUANTUM — GUMROAD PRODUCT LISTING PACKAGE")
    print("=" * 70)
    print(f"Title:         {payload['name']}")
    print(f"Price:         ${payload['price_cents'] / 100:.2f} {payload.get('currency', 'USD').upper()}")
    print(f"Permalink:     https://gumroad.com/l/{payload['permalink']}")
    print(f"Tags:          {', '.join(payload['tags'])}")
    print(f"File Bundle:   {ARCHIVE_PATH} ({ARCHIVE_PATH.stat().st_size if ARCHIVE_PATH.exists() else 0} bytes)")
    print("\n💡 Automated publishing requires a GUMROAD_ACCESS_TOKEN.")
    print("   To publish automatically, set the environment variable:")
    print("     export GUMROAD_ACCESS_TOKEN='your_gumroad_token'")
    print("     python3 gumroad/publish.py")
    print("\n🌐 Or manually create the product in 1 click at:")
    print("     https://app.gumroad.com/products/new")
    print("\n📋 cURL Publishing Command:")
    print("-" * 70)
    print(f"""curl -X POST https://api.gumroad.com/v2/products \\
  -H "Authorization: Bearer $GUMROAD_ACCESS_TOKEN" \\
  -d "name={urllib.parse.quote(payload['name'])}" \\
  -d "price={payload['price_cents']}" \\
  -d "custom_permalink={payload['permalink']}" \\
  -d "custom_summary={urllib.parse.quote(payload['custom_summary'])}" \\
  -d "tags={','.join(payload['tags'])}"
""")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Publish HYDRA-MESH to Gumroad")
    parser.add_argument("--token", help="Gumroad Access Token (or via GUMROAD_ACCESS_TOKEN env var)")
    args = parser.parse_args()
    
    payload = load_payload()
    token = args.token or os.environ.get("GUMROAD_ACCESS_TOKEN") or os.environ.get("GUMROAD_API_KEY")
    
    if token:
        publish_to_gumroad(token, payload)
    else:
        print_manual_instructions(payload)

if __name__ == "__main__":
    main()
