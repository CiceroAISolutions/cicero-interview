import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")
WEBHOOK = f"{BASE}/webhooks/voice"

for folder in (HERE / "data", HERE.parent / "call-ended-ingest" / "data"):
    if (folder / "call_ended.json").exists():
        DATA = folder
        break
else:
    raise FileNotFoundError("Could not find data/call_ended.json")

CASES = [
    ("Rivera first delivery", "call_ended.json", {200, 201}),
    ("same call_id is not a second row", "call_ended_retry.json", {200, 201, 409}),
    ("unknown firm is rejected", "unknown_firm.json", set(range(400, 500))),
    ("North Shore inbound", "other_firm.json", {200, 201}),
]


def post(name):
    request = urllib.request.Request(
        WEBHOOK,
        data=(DATA / name).read_bytes(),
        headers={"content-type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except urllib.error.URLError:
        return None


failed = 0
for label, name, allowed in CASES:
    status = post(name)
    if status in allowed:
        print(f"✓  {label}")
    else:
        failed += 1
        print(f"✗  {label}  (got HTTP {status})")

print()
print("failed" if failed else "all passed")
raise SystemExit(1 if failed else 0)
