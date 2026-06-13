# Sprint 4 — Final Documentation and Project Closure

## Objective

Write the final documentation that closes the project academically: a complete README, the last PROMPTS.md entry, this sprint file, and the Pull Request that merges all work into main.

## Included stories

| Story | Title |
|-------|-------|
| HU-05 | Final documentation and evidence (complete) |

## Tasks

| # | Task | Status |
|---|------|--------|
| 1 | Write complete README.md (architecture, endpoints, Scrum summary, technical decisions) | Done |
| 2 | Append Entry 4 to PROMPTS.md | Done |
| 3 | Create docs/SPRINT4.md (this file) | Done |
| 4 | Create Pull Request feature/cag-implementation → main | Done |

## Status

**CLOSED.**

---

## Retrospective

### What worked well

- **Prompt-driven sprints.** Breaking the project into four focused prompts — documentation, ContextStore, CAG integration, final docs — made each AI session short and verifiable. Each session produced exactly one testable increment.
- **Constraint-first prompting.** Stating hard constraints upfront (no circular imports, thread-safe, no external libraries, exact test signatures) eliminated back-and-forth corrections. Jarvis produced compliant code on the first attempt in every sprint.
- **Reading before writing.** Every implementation sprint began with Jarvis reading all relevant files before touching anything. This prevented assumptions and caught the exact API contracts the tests expected.
- **Separation of layers.** Keeping `cag.py` and `assistant.py` free of any HTTP or server knowledge made them trivially testable and kept the dependency graph clean.

### What I would improve

- **Earlier test execution.** Tests were described as "all passing" but were not actually run inside the AI session. In future sprints I would add a mandatory `pytest` run step at the end of each implementation sprint so evidence is generated immediately, not deferred to a later sprint.
- **ContextStore isolation between tests.** The module-level `context_store` singleton in `server.py` is shared across all test classes that call `create_server()`. This works now because users are distinct across tests, but a `setUp` reset would make the tests more robust as the suite grows.
- **Knowledge base keyword retrieval.** The RAG layer uses simple term overlap. A real project would use embeddings or BM25, but that was out of scope for Module 3.
