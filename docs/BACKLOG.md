# Product Backlog

## HU-01 — Functional ContextStore (save)

**As a** system,
**I need** a functional `ContextStore` that saves key/value pairs per user in memory,
**so that** user context persists for the duration of the session.

**Acceptance criteria:**
- `ContextStore.save(user_id, key, value)` stores the entry without raising an error.
- Multiple entries for the same `user_id` are all retained.
- Data is held in memory (no persistence to disk required).

---

## HU-02 — Functional ContextStore (retrieve)

**As a** system,
**I need** `list_for_user` to return a list of `{key, value}` dicts for a given user,
**so that** stored context can be retrieved and used downstream.

**Acceptance criteria:**
- `ContextStore.list_for_user(user_id)` returns a list of `{"key": ..., "value": ...}` dicts.
- Returns an empty list when no context has been saved for that user.
- Does not return entries belonging to other users.

---

## HU-03 — Context-aware apply_context

**As a** system,
**I need** `apply_context` to modify the base answer by incorporating values from the user's stored context,
**so that** responses are personalised to the user's declared preferences.

**Acceptance criteria:**
- `apply_context(user_id, base_answer)` returns a string that includes at least one value from the user's context.
- Returns `(modified_answer, keys_used)` where `keys_used` is the list of context keys that influenced the answer.
- When no context exists for the user the base answer is returned unchanged and `keys_used` is empty.

---

## HU-04 — answer_question integrates CAG

**As a** system,
**I need** `answer_question` to call `apply_context` and return `context_used` alongside the answer,
**so that** the `/api/ask` endpoint exposes which context keys shaped the response.

**Acceptance criteria:**
- `answer_question(user_id, question)` returns a dict with at least `"answer"` and `"context_used"` keys.
- `"context_used"` lists every context key that was applied.
- The integration does not break the existing base-test suite.

---

## HU-05 — Final documentation and evidence

**As a** student,
**I need** complete final documentation including README, evidence screenshots, and a fully populated PROMPTS.md,
**so that** the project satisfies all academic submission requirements.

**Acceptance criteria:**
- `PROMPTS.md` contains one entry per AI-assisted session with objective, prompt, response summary, human decision, changes made, and verification method.
- `docs/BACKLOG.md` lists all user stories with acceptance criteria.
- `docs/SPRINT1.md` and `docs/SPRINT2.md` document both sprints.
- `docs/BDD.md` contains Gherkin scenarios for all three validation tests.
- `README.md` describes how to install, run, and test the project.
- `docs/evidencias/` contains at least one screenshot of the passing validation tests.
