# Instructions

You are ingesting `call_ended` webhooks from a voice vendor for several law firms that share one backend. The vendor may POST the same `call_id` more than once.

Implement `POST /webhooks/voice`. Do not build analysis, documents, auth, or a queue.

## What is already here

| Path | What it is |
|------|------------|
| `app.py` | FastAPI routes: `GET /authors`, stub webhook |
| `db.py` | SQLite engine, session, `get_db`, seed |
| `models.py` | Example one-to-many schema (`Author` → `Book`). Not the ingest schema. |
| `llm.py` | Optional `complete(prompt) -> str`. Fake model; no API key. |
| `data/` | Sample vendor payloads |
| `requirements.txt` | FastAPI, Uvicorn, SQLAlchemy |

SQLite is a file in this folder (`interview.db`). It is created when you start the app. You do not need Postgres or Docker.

## Run

Work in this folder. Python 3.9+ (3.10+ preferred).

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Smoke test: http://127.0.0.1:8000/authors — you should see Ada Lovelace and Grace Hopper

## SQLite

The engine lives in `db.py` (`sqlite:///interview.db`). `init_db()` runs `create_all` from `models.py` and seeds authors.

Inspect:

```bash
sqlite3 interview.db
```

```sql
.tables
.schema authors
.schema books
SELECT * FROM authors;
```

After you add or change tables/columns, delete the file and restart. SQLite will not migrate for you.

```bash
rm interview.db
```

## Foreign keys (`models.py`)

This is a teaching example. One author has many books.

- `authors.id` is the parent primary key
- `books.author_id` stores that id
- `ForeignKey("authors.id")` is the database constraint
- `relationship()` is optional Python sugar (`book.author`, `author.books`)

Add your own tables for this problem. You will want something like a firm and its calls. Copy the same `ForeignKey` / `relationship` pattern.

Put the new classes in `models.py` on the existing `Base`. If you seed firms, import those models in `db.py` and add them in `init_db()` the same way authors are seeded. Do not model every vendor field — keep the raw JSON and read `call_id` / `to_number` from it.

## LLM (optional)

`llm.complete(prompt: str) -> str` stands in for a model call. You do not have to use it. If you do, you decide what to send and what to do with the result.

In production that call is slow and costs money. The stub sleeps briefly and returns untrusted placeholder text.

## Problem

A voice vendor POSTs JSON like `data/call_ended.json`:

```json
{
  "event": "call_ended",
  "call": {
    "call_id": "call_abc123",
    "direction": "inbound",
    "from_number": "+15551230001",
    "to_number": "+17135559999",
    "transcript": "..."
  }
}
```

The call object is under `call`, not at the top level.

Known inbound firm numbers:

| Firm | Phone |
|------|--------|
| Rivera & Associates | `+17135559999` |
| North Shore Legal | `+12815550000` |

## Implement

1. Add tables (and seed firms if you need them).
2. Fill in `POST /webhooks/voice` in `app.py`.
3. Persist enough to list calls per firm later and to debug a payload.

A list/get endpoint is optional if you have time.

### Rules

- Inbound firm is `call.to_number`.
- Same `call_id` twice → one row, not two.
- Unknown `to_number` → reject. Do not create an orphan call.
- Keep the raw payload so you could reprocess later.

### Try it

```bash
curl -s -X POST http://127.0.0.1:8000/webhooks/voice \
  -H 'content-type: application/json' \
  --data @data/call_ended.json
```

| File | What it is |
|------|------------|
| `data/call_ended.json` | Rivera inbound (first delivery) |
| `data/call_ended_retry.json` | Same `call_id`, slightly richer transcript |
| `data/unknown_firm.json` | `to_number` matches no firm |
| `data/other_firm.json` | North Shore inbound |

You can also POST from `/docs`.
