# Call-ended ingest

Candidate brief: **[INSTRUCTIONS.md](INSTRUCTIONS.md)**.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app.py
```

`GET /authors` is a smoke test that SQLite is up.

## Models

`models.py` is an example of a one-to-many foreign key (`Author` → `Book`). It is not the ingest schema.

Add your own tables for this problem (you will want a firm and its calls). Copy the `ForeignKey` / `relationship` pattern. After you add columns or tables, delete `interview.db` and restart.

Known inbound numbers:

| firm | phone |
|------|--------|
| Rivera & Associates | `+17135559999` |
| North Shore Legal | `+12815550000` |

## Rules

- Inbound firm is `call.to_number`.
- Same `call_id` → one row.
- Unknown `to_number` → reject, no orphan row.
- Keep the raw payload so you could reprocess later.

```bash
curl -s -X POST http://127.0.0.1:8000/webhooks/voice \
  -H 'content-type: application/json' \
  --data @data/call_ended.json
```

Other fixtures: `call_ended_retry.json` (same `call_id`), `unknown_firm.json`, `other_firm.json`.
