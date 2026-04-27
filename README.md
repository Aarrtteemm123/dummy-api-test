# Dummy API Test

A small **Python** sample: it calls the public **[DummyJSON](https://dummyjson.com)** API asynchronously, maps JSON into **dataclass** models, and keeps them in an **in-memory** store.

## What it does

1. Uses `PostLoaderService` to load post `1` from the API, then `PostStorageService` to store it with key `1` (`save_post`).
2. Searches via the loader (`fetch_posts_by_query`), then persists with `PostStorageService.save_posts`.
3. Loads comments (`fetch_comments`), then `PostStorageService.save_comments`.
4. Logs both collections to the console via `logging` (not raw `print` in the current `main.py`).

`main.py` wires `PostLoaderService` (HTTP + mapping) and `PostStorageService` (in-memory `Storage`). It handles HTTP and network failures (`httpx.HTTPStatusError`, `httpx.RequestError`); a broad `except Exception` covers other cases.

## Project layout

| Path | Role |
|------|------|
| `main.py` | Entry point: client, storage, service calls |
| `clients/dummy_client.py` | `httpx` async client for `https://dummyjson.com` |
| `services/` | `PostLoaderService` (API → models) and `PostStorageService` (models → `Storage`) |
| `models/post.py`, `models/comment.py` | `Post` and `Comment` models (comment includes nested author) |
| `storage.py` | `Storage` protocol and `InMemoryStorage` implementation |
| `tests/` | Pytest suite (storage, models, loader/storage services, `DummyClient` with `MockTransport`) |

Run commands from the **repository root** so `clients`, `services`, and `models` resolve on `PYTHONPATH` (see `pytest.ini` → `pythonpath = .`).

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

## Tests

Install dev dependencies (includes **pytest**, **pytest-asyncio**, and the app requirements from `requirements.txt`):

```bash
cd /path/to/dummy-api-test
source .venv/bin/activate   # if you use a venv
pip install -r requirements-dev.txt
```

Run the full suite from the repo root:

```bash
python3 -m pytest tests/ 
```

Use `python3 -m pytest tests/ -v` for per-test names, or `python3 -m pytest tests/test_storage.py` to run a single file.

## Dependencies

- **Runtime:** `requirements.txt` (main library: **httpx**).
- **Development / tests:** `requirements-dev.txt` (adds **pytest** and **pytest-asyncio**).
