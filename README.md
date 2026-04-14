# Dummy API Test

A small **Python** sample: it calls the public **[DummyJSON](https://dummyjson.com)** API asynchronously, maps JSON into **dataclass** models, and keeps them in an **in-memory** store.

## What it does

1. Fetches post `id=1` and saves it under the `posts` collection.
2. Searches posts for the query `"love"` and saves all matches to the same collection.
3. Loads comments for post `id=2` and saves them under the `comments` collection.
4. Prints both collections to the console.

`main.py` handles HTTP and network failures (`httpx.HTTPStatusError`, `httpx.RequestError`); anything else is caught by a broad `except Exception`.

## Project layout

| Path | Role |
|------|------|
| `main.py` | Entry point: client, storage, service calls |
| `clients/dummy_client.py` | `httpx` async client for `https://dummyjson.com` |
| `services/post_service.py` | Workflows: fetch → parse → persist via `Storage` |
| `models/post.py`, `models/comment.py` | `Post` and `Comment` models (comment includes nested author) |
| `storage.py` | `Storage` protocol and `InMemoryStorage` implementation |

Run commands from the **repository root** so `clients`, `services`, and `models` resolve on `PYTHONPATH`.

## Requirements

- **Python 3.10+**.
- **Network** access to `dummyjson.com`.

## How to run

```bash
cd /path/to/dummy-api-test
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 main.py
```

You should see `Stored posts:` and `Stored comments:` on **stdout** (dict-like maps: keys are ids, values are model instances). Failed requests print to **stderr**.

## Dependencies

See `requirements.txt` (main library: **httpx**).
