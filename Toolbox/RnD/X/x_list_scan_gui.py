# x_list_apify.py
# Minimal: fetch members of a Twitter/X List via Apify Actor and save CSV.
# Requires an Apify account + API token.
# Usage:
#   $env:APIFY_TOKEN="..."     # PowerShell
#   python x_list_apify.py https://x.com/i/lists/1234567890 --max 1000 --out output

import os, sys, re, json, csv
from pathlib import Path
from datetime import datetime

try:
    import requests  # pip install requests
except Exception:
    print("This script needs the 'requests' package.\nInstall it: python -m pip install requests", file=sys.stderr)
    sys.exit(1)

API_URL = "https://api.apify.com/v2/acts/powerai~twitter-list-members-scraper/run-sync-get-dataset-items"
TOKEN = os.getenv("APIFY_TOKEN")
LIST_RE = re.compile(r"(?:https?://)?(?:www\.)?(?:x|twitter)\.com/i/lists/(\d+)")

def extract_list_id(s: str) -> str:
    s = s.strip()
    if s.isdigit():
        return s
    m = LIST_RE.search(s)
    if not m:
        raise SystemExit("Provide a List URL like https://x.com/i/lists/<ID> or the numeric ID.")
    return m.group(1)

def post_apify(list_id: str, max_results: int):
    if not TOKEN:
        raise SystemExit("Set your Apify API token in the APIFY_TOKEN environment variable.")
    url = f"{API_URL}?token={TOKEN}"
    payload = {"list_id": list_id, "maxResults": max_results}
    r = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=300)
    if r.status_code >= 400:
        raise SystemExit(f"Apify API error {r.status_code}: {r.text[:500]}")
    try:
        data = r.json()
    except Exception:
        raise SystemExit("Apify returned non-JSON; raw:\n" + r.text[:500])
    # run-sync-get-dataset-items returns an array; fall back if wrapped
    if isinstance(data, dict) and "items" in data:
        return data["items"]
    if not isinstance(data, list):
        raise SystemExit("Unexpected response JSON:\n" + json.dumps(data)[:500])
    return data

def rows_to_csv(items, out_path: Path):
    if not items:
        out_path.write_text("", encoding="utf-8"); return
    flat = []
    for it in items:
        row = {}
        obj = it.get("user") if isinstance(it, dict) and isinstance(it.get("user"), dict) else it
        for k, v in (obj or {}).items():
            row[k] = json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v
        flat.append(row)
    keys = sorted({k for r in flat for k in r.keys()})
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader(); [w.writerow(r) for r in flat]

def main(argv):
    import argparse
    p = argparse.ArgumentParser(description="Download Twitter/X List members via Apify and save CSV")
    p.add_argument("list_url_or_id", help="List URL like https://x.com/i/lists/<ID> or the numeric ID itself")
    p.add_argument("--max", type=int, default=1000, help="Max members to fetch (default 1000)")
    p.add_argument("--out", default="output", help="Output folder (default ./output)")
    a = p.parse_args(argv)

    list_id = extract_list_id(a.list_url_or_id)
    out_dir = Path(a.out); out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_csv = out_dir / f"list_{list_id}_members_{ts}.csv"

    print(f"[+] Fetching members for list {list_id} (max={a.max}) via Apify…")
    items = post_apify(list_id, a.max)
    print(f"[+] Received {len(items)} items. Writing CSV → {out_csv}")
    rows_to_csv(items, out_csv)
    print("[✓] Done.")

if __name__ == "__main__":
    main(sys.argv[1:])
