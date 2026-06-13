# RAG + CAG System — Final Project Module 3

An HTTP assistant that answers questions using **Retrieval-Augmented Generation (RAG)** and personalises those answers with **Context-Augmented Generation (CAG)** based on per-user stored preferences.

---

## What it does and what problem it solves

A plain RAG system retrieves relevant knowledge snippets and returns a generic answer — the same answer for every user regardless of who is asking. This project adds a CAG layer on top: users can declare their preferences (audience level, project type, preferred style, etc.) once, and every subsequent answer is automatically adapted to those preferences.

**Problem solved:** generic AI responses that ignore user context. **Solution:** a lightweight, in-memory context store that enriches any RAG response without touching the retrieval logic or requiring a database.

---

## Architecture

```
Client
  │
  ▼
server.py  (ThreadingHTTPServer)
  ├── GET  /health
  ├── GET  /api/context?user_id=X   ──► context_store.list_for_user(X)
  ├── POST /api/context              ──► context_store.save(user_id, key, value)
  └── POST /api/ask
        ├── context_store.list_for_user(user_id)   [1] fetch context
        ├── answer_question(user_id, question, context_items)
        │     ├── retrieve_snippets(question)       [2] RAG retrieval
        │     └── apply_context(..., context_items) [3] CAG enrichment
        └── return {answer, sources, context_used}
```

### Base RAG layer
`knowledge.py` scores every entry in `data/knowledge_base.json` by term overlap with the question and returns the top-2 matches. `assistant.py` joins their content into a base answer.

### Added CAG module
`cag.py` receives the base answer plus the user's stored context items. If context exists, it appends the context values to the answer and returns the list of keys used. `context_store.py` holds all context in a plain Python dict guarded by a `threading.Lock`.

---

## Folder structure

```
.
├── backend/
│   ├── server.py          # HTTP server, routes, global context_store instance
│   ├── assistant.py       # answer_question — RAG + CAG integration point
│   ├── cag.py             # apply_context — enriches base answer with user context
│   ├── context_store.py   # ContextStore — thread-safe in-memory key/value store
│   └── knowledge.py       # retrieve_snippets — keyword-scored RAG retrieval
├── data/
│   └── knowledge_base.json  # Course knowledge entries (id, title, content)
├── frontend/
│   ├── index.html         # Static UI
│   ├── app.js             # Fetch calls to /api/ask and /api/context
│   └── styles.css
├── tests/
│   ├── base/
│   │   └── test_base_api.py        # Base tests (must always pass)
│   └── validation/
│       └── test_cag_contract.py    # Validation tests for CAG contract
├── docs/
│   ├── BACKLOG.md          # Product backlog (HU-01 to HU-05)
│   ├── BDD.md              # Gherkin scenarios for all 3 validation tests
│   ├── SPRINT1.md          # Sprint 1 — documentation and planning
│   ├── SPRINT2.md          # Sprint 2 — ContextStore implementation
│   ├── SPRINT3.md          # Sprint 3 — CAG integration
│   ├── SPRINT4.md          # Sprint 4 — final documentation and closure
│   └── evidencias/         # Screenshots of passing tests
├── scripts/
│   ├── run_base_tests.sh   # Runs tests/base/
│   └── validate_student_cag.sh  # Runs tests/validation/
├── PROMPTS.md              # Prompt engineering log (one entry per AI session)
└── test.sh                 # Runs the full validation suite
```

---

## Installation and execution

### Prerequisites

- Python 3.9 or higher
- No external packages required — only the standard library

### Clone and set up

```bash
git clone <repo-url>
cd final_project_AI_CUSTOM_wg
```

### Run the backend

```bash
PYTHONPATH=. python3 -m backend.server
# Server available at http://127.0.0.1:8000
```

### Run base tests

```bash
PYTHONPATH=. python -m pytest tests/base/ -v
```

Expected: 3 tests pass.

### Run validation tests (CAG contract)

```bash
PYTHONPATH=. python -m pytest tests/validation/ -v
```

Expected: 3 tests pass.

### Run all tests at once

```bash
PYTHONPATH=. python -m pytest tests/ -v
```

Expected: 6 tests pass, 0 failures.

### Open the frontend

Open `frontend/index.html` directly in a browser while the backend is running.

---

## API endpoints

### `GET /health`

Returns server status.

**Response `200`:**
```json
{"status": "ok"}
```

---

### `POST /api/ask`

Answers a question using RAG, enriched with the user's stored context via CAG.

**Request body:**
```json
{"user_id": "ana", "question": "Que es CAG?"}
```

**Response `200`:**
```json
{
  "user_id": "ana",
  "answer": "Segun la base de conocimiento del curso: CAG usa contexto persistente... [Contexto del usuario: explicar como principiante]",
  "sources": ["cag"],
  "context_used": ["audience"]
}
```

- `answer` — base RAG answer, optionally enriched with user context values
- `sources` — knowledge base entry IDs used
- `context_used` — list of context keys that influenced the answer (`[]` if no context)

**Response `400`** — if `user_id` or `question` is missing.

---

### `POST /api/context`

Saves a key/value preference for a user.

**Request body:**
```json
{"user_id": "ana", "key": "audience", "value": "explicar como principiante"}
```

**Response `201`:**
```json
{"saved": true}
```

**Response `400`** — if any required field is missing.

---

### `GET /api/context?user_id=ana`

Retrieves all saved context entries for a user.

**Response `200`:**
```json
{
  "user_id": "ana",
  "context": [
    {"key": "audience", "value": "explicar como principiante"},
    {"key": "project",  "value": "usa arquitectura monolitica moderna"}
  ]
}
```

Returns `"context": []` if no context has been saved for that user.

**Response `400`** — if `user_id` query parameter is missing.

---

## Scrum summary

| Sprint | Goal | Key deliverables | Status |
|--------|------|-----------------|--------|
| Sprint 1 | Documentation and planning | BACKLOG.md, BDD.md, SPRINT1-4.md, PROMPTS.md | Closed |
| Sprint 2 | ContextStore implementation | `context_store.py` — HU-01, HU-02 | Closed |
| Sprint 3 | CAG integration | `cag.py`, `assistant.py`, `server.py` — HU-03, HU-04 | Closed |
| Sprint 4 | Final documentation and closure | README.md, SPRINT4.md, PROMPTS.md Entry 4, PR | Closed |

User stories: HU-01 through HU-05 (see `docs/BACKLOG.md`).
BDD scenarios: three Gherkin scenarios mapping 1:1 to the validation tests (see `docs/BDD.md`).

---

## Technical decisions

### In-memory storage instead of a database

The validation tests spin up a fresh server instance per test class using `port=0` (OS-assigned port). A persistent store (SQLite, file, Redis) would require setup, teardown, and isolation between test runs. An in-memory `dict` is sufficient for the course scope, is instantaneous to initialise, and is automatically isolated between server instances. The trade-off is that context is lost when the process exits — acceptable here, not acceptable in production.

### Avoiding circular imports

`context_store` is instantiated at module level in `server.py`. `assistant.py` must not import from `server.py` or the import chain would be circular (`server → assistant → server`). The solution: `server.py` calls `context_store.list_for_user(user_id)` before invoking `answer_question`, and passes the result as a plain `context_items` parameter. `assistant.py` and `cag.py` receive a list of dicts — they have no knowledge of the HTTP layer and no import dependency on it.

### Thread safety

`ThreadingHTTPServer` handles each request in its own thread. Without a lock, two concurrent `save()` calls on the same `user_id` could corrupt the list (e.g., lost update on `dict.__setitem__`). A single `threading.Lock` instance inside `ContextStore` serialises all reads and writes. The lock is held only for the duration of the dict operation, keeping contention minimal.

---

## Evidence

Test run screenshots are located in `docs/evidencias/`.

- `evidencias/base_tests_pass.png` — output of `pytest tests/base/ -v`
- `evidencias/validation_tests_pass.png` — output of `pytest tests/validation/ -v`
