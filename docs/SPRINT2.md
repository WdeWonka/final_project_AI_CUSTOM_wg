# Sprint 2 — CAG Implementation

## Objective

Implement the CAG (Context-Augmented Generation) module so that all three validation tests in `tests/validation/test_cag_contract.py` pass without breaking the existing base tests.

## Included stories

| Story | Title |
|-------|-------|
| HU-01 | Functional ContextStore (save) |
| HU-02 | Functional ContextStore (retrieve) |
| HU-03 | Context-aware apply_context |
| HU-04 | answer_question integrates CAG |
| HU-05 | Final documentation and evidence (complete) |

## Tasks

| # | Task | Status |
|---|------|--------|
| 1 | Implement `ContextStore.save()` and `ContextStore.list_for_user()` | Done |
| 2 | Implement `apply_context()` in `cag.py` | Pending |
| 3 | Update `answer_question()` to call `apply_context` and return `context_used` | Pending |
| 4 | Verify all base tests still pass | Pending |
| 5 | Verify all 3 validation tests pass | Pending |
| 6 | Capture evidence screenshots and add to `docs/evidencias/` | Pending |
| 7 | Finalize `PROMPTS.md` with Sprint 2 entries | In progress |

## Status

**In progress.** HU-01 and HU-02 complete. HU-03 and HU-04 pending.

## Implementation notes

### ContextStore (backend/context_store.py)

- Storage: `dict` keyed by `user_id`, each value a `list` of `{"key", "value"}` dicts.
- Thread safety: single `threading.Lock()` wraps all reads and writes — required because the server is `ThreadingHTTPServer`.
- `save()` appends the entry and returns `True`.
- `list_for_user()` returns a shallow copy via `list(...)` so callers cannot mutate internal state.
- No external dependencies.
