# Sprint 3 — CAG Integration

## Objective

Wire `apply_context` into `answer_question` so that stored user context influences the `/api/ask` response, completing the full CAG pipeline.

## Included stories

| Story | Title |
|-------|-------|
| HU-03 | Context-aware apply_context |
| HU-04 | answer_question integrates CAG |

## Tasks

| # | Task | Status |
|---|------|--------|
| 1 | Implement `apply_context()` in `cag.py` | Done |
| 2 | Update `answer_question()` to accept and use `context_items` | Done |
| 3 | Update `server.py` to fetch context and pass it to `answer_question` | Done |
| 4 | Verify base tests still pass | Pending |
| 5 | Verify all 3 validation tests pass | Pending |
| 6 | Capture evidence screenshots and add to `docs/evidencias/` | Pending |
| 7 | Finalize `PROMPTS.md` with Sprint 3 entry | Done |

## Status

**In progress.** Implementation complete, awaiting test verification by project owner.

## Architecture decision

`context_store` lives in `server.py`. Rather than importing `server.py` from `assistant.py` (circular import), `server.py` calls `context_store.list_for_user(user_id)` and passes the result as a `context_items` parameter to `answer_question`. This keeps `assistant.py` and `cag.py` completely decoupled from the HTTP layer and independently testable.

## Implementation notes

### cag.py

- Empty `context_items` → returns `base_answer` unchanged with `context_used: []`.
- Non-empty → concatenates all context values into a `[Contexto del usuario: ...]` suffix and returns all keys in `context_used`.

### assistant.py

- `context_items` defaults to `[]` so existing callers that omit it continue to work.
- Both the no-snippets and the normal path now call `apply_context` and use its returned dict.

### server.py

- One additional line before the `answer_question` call: `context_items = context_store.list_for_user(user_id)`.
- No other changes to the server.
