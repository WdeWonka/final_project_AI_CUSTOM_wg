================================================================================
INFORME FINAL — PROYECTO RAG + CAG
Módulo 3 · Examen Final
Estudiante: William (WdeWonka)
Repositorio: https://github.com/WdeWonka/final_project_AI_CUSTOM_wg
================================================================================

DESCRIPCIÓN DEL PROYECTO
--------------------------------------------------------------------------------
Se partió de un proyecto monolítico base con frontend, backend y un sistema RAG
(Retrieval-Augmented Generation) que respondía preguntas desde una base documental
pequeña. El problema era que el sistema no conservaba contexto del usuario entre
consultas — cada respuesta era genérica sin importar quién preguntaba.

Se implementó un módulo CAG (Context-Augmented Generation) que guarda preferencias
del usuario (clave/valor), las recupera en cada consulta y las usa para enriquecer
la respuesta del asistente. El resultado: el mismo sistema RAG ahora personaliza
sus respuestas según el contexto guardado de cada usuario.

METODOLOGÍA
--------------------------------------------------------------------------------
Se trabajó con metodología Scrum en 4 sprints, usando Claude CLI como asistente
(Jarvis). El estudiante dirigió todas las decisiones de diseño y arquitectura.
Cada prompt fue registrado cronológicamente en PROMPTS.md con decisión humana,
cambios realizados y verificación aplicada.

================================================================================
SPRINT 1 — DOCUMENTACIÓN Y PLANIFICACIÓN
================================================================================

QUÉ SE HIZO:
Se estableció toda la estructura de documentación antes de escribir cualquier
línea de código. Se definieron las 5 historias de usuario, se redactaron los 3
escenarios BDD que mapean con las pruebas de validación, y se inicializó el log
PROMPTS.md. Ningún archivo Python fue modificado en este sprint.

ARCHIVOS CREADOS:
- PROMPTS.md
- docs/BACKLOG.md (HU-01 a HU-05)
- docs/SPRINT1.md
- docs/SPRINT2.md (placeholder)
- docs/BDD.md (3 escenarios Gherkin)

PROMPT UTILIZADO:
--------------------------------------------------------------------------------
You are my development assistant (Jarvis). I am Tony Stark: I make all the
decisions. I am working on a Python project with this structure:
- backend/server.py: HTTP server with endpoints /health, /api/ask, /api/context
- backend/assistant.py: answer_question(user_id, question) function that uses RAG
- backend/cag.py: placeholder with apply_context() that just returns the base
  answer unchanged
- backend/context_store.py: ContextStore class with save() and list_for_user()
  that raise NotImplementedError
- tests/base/test_base_api.py: base tests that already pass
- tests/validation/test_cag_contract.py: validation tests I must make pass

The goal is to implement a CAG (Context-Augmented Generation) module that:
1. Saves user context (key/value) in memory
2. Retrieves that context when the user asks
3. Uses that context to modify the /api/ask response so that body["answer"]
   contains words from the context and body["context_used"] lists the keys used

The validation tests I must pass are exactly these:
- test_saves_context_for_user: POST /api/context returns 201 and {"saved": true}
- test_retrieves_context_for_user: GET /api/context?user_id=ana returns list
  with {"key": ..., "value": ...}
- test_ask_uses_context_to_influence_later_response: if context has key="audience"
  value="explicar como principiante", then /api/ask must return answer containing
  "principiante" and context_used must contain "audience"

Your task in this sprint is to ONLY generate documentation, without touching any
Python code yet:
1. Content for PROMPTS.md with this first entry
2. Content for docs/BACKLOG.md with user stories HU-01 to HU-05
3. Content for docs/SPRINT1.md
4. Content for docs/BDD.md with Gherkin scenarios for the 3 validation tests
--------------------------------------------------------------------------------

DECISIÓN HUMANA: Se aprobó la estructura de 4 sprints y el backlog antes de
implementar cualquier cosa.

CAPTURAS:
- sprint1-estado-inicial.png → frontend cargando con Panel CAG vacío

================================================================================
SPRINT 2 — IMPLEMENTACIÓN DE CONTEXTSTORE
================================================================================

QUÉ SE HIZO:
Se implementó ContextStore en backend/context_store.py reemplazando los
placeholders que lanzaban NotImplementedError. Se eligió almacenamiento en
memoria usando un diccionario Python protegido con threading.Lock() para
garantizar seguridad en el servidor multihilo. Al cierre del sprint, POST
/api/context y GET /api/context funcionaban correctamente.

ARCHIVOS MODIFICADOS:
- backend/context_store.py (implementación completa)
- docs/SPRINT2.md (actualizado)
- PROMPTS.md (Entry 2 agregada)

PROMPT UTILIZADO:
--------------------------------------------------------------------------------
You are my development assistant (Jarvis). I lead, you assist.

I have this file backend/context_store.py currently:

"""Base placeholder for student implementation."""
class ContextStore:
    def save(self, user_id, key, value):
        raise NotImplementedError("CAG context storage is not implemented yet")
    def list_for_user(self, user_id):
        raise NotImplementedError("CAG context retrieval is not implemented yet")

I must pass these two exact tests:

TEST 1 - test_saves_context_for_user:
  POST /api/context with {"user_id": "ana", "key": "preferred_style",
  "value": "explicaciones con analogias"}
  Expects: status 201, body["saved"] == True

TEST 2 - test_retrieves_context_for_user:
  First saves {"user_id": "ana", "key": "project",
  "value": "usa arquitectura monolitica moderna"}
  Then GET /api/context?user_id=ana
  Expects: status 200, body["user_id"] == "ana", body["context"] contains
  {"key": "project", "value": "usa arquitectura monolitica moderna"}

Constraints:
- In-memory storage (Python dict), no database or files
- Thread-safe using threading.Lock() because the server is ThreadingHTTPServer
- save() must return True when it saves successfully
- list_for_user() must return a list of dicts with format {"key":..., "value":...}
- If the user does not exist, list_for_user() returns an empty list
- Do not use external libraries

Give me the complete and final content of backend/context_store.py ready to
replace the current one.
--------------------------------------------------------------------------------

DECISIÓN HUMANA: Se aprobó almacenamiento en memoria con threading.Lock() en
lugar de base de datos o archivos.

CAPTURAS:
- sprint2-context-store-funcionando.png → curl mostrando {"saved": true} y
  recuperación del contexto guardado

================================================================================
SPRINT 3 — INTEGRACIÓN CAG COMPLETA
================================================================================

QUÉ SE HIZO:
Se conectó el pipeline completo del módulo CAG. Se implementó apply_context()
en cag.py para enriquecer las respuestas con los valores del contexto del usuario,
y se modificó answer_question() en assistant.py para recibir y usar ese contexto.
La decisión arquitectónica clave fue evitar importaciones circulares: server.py
obtiene el contexto y lo pasa como parámetro, manteniendo assistant.py
completamente independiente de la capa HTTP. Al cierre del sprint los 6 tests
pasaban — 3 base y 3 de validación.

ARCHIVOS MODIFICADOS:
- backend/cag.py (implementado)
- backend/assistant.py (integrado con CAG)
- backend/server.py (pasa context_items a answer_question)
- docs/SPRINT3.md (creado)
- PROMPTS.md (Entry 3 agregada)

PROMPT UTILIZADO:
--------------------------------------------------------------------------------
You are my development assistant (Jarvis). I lead and verify everything.

Project context:
- backend/context_store.py: already implemented, saves and lists context per
  user in memory
- backend/assistant.py current content:

from backend.knowledge import retrieve_snippets
def answer_question(user_id, question):
    snippets = retrieve_snippets(question)
    if not snippets:
        return {
            "user_id": user_id,
            "answer": "No encontre informacion suficiente en la base de
            conocimiento del curso.",
            "sources": [],
            "context_used": [],
        }
    source_text = " ".join(item["content"] for item in snippets)
    answer = f"Segun la base de conocimiento del curso: {source_text}"
    return {
        "user_id": user_id,
        "answer": answer,
        "sources": [item["id"] for item in snippets],
        "context_used": [],
    }

- backend/cag.py current content:
"""Base placeholder for student implementation."""
def apply_context(user_id, question, base_answer, context_items):
    return base_answer

The test I must pass is exactly this:
test_ask_uses_context_to_influence_later_response:
  1. POST /api/context {"user_id": "luis", "key": "audience",
     "value": "explicar como principiante"}
  2. POST /api/ask {"user_id": "luis", "question": "Que es CAG?"}
  3. Expects: status 200
  4. Expects: "principiante" in body["answer"].lower()
  5. Expects: "audience" in body["context_used"]

Critical constraint: do NOT create a circular import between server.py and
assistant.py. The context_store lives in server.py. Find the best architectural
solution to pass the context to answer_question.
--------------------------------------------------------------------------------

DECISIÓN HUMANA: Se aprobó la solución de pasar context_items como parámetro
desde server.py hacia answer_question() para evitar importación circular.

ARQUITECTURA RESULTANTE:
  server.py → context_store.list_for_user(user_id)
            → answer_question(user_id, question, context_items)
                 └→ apply_context(user_id, question, base_answer, context_items)

CAPTURAS:
- sprint3-sin-contexto.png → Panel CAG con "context": []
- sprint3-con-contexto.png → Panel CAG mostrando key:"audience" y
  value:"explicar como principiante"
- sprint3-respuesta-enriquecida.png → respuesta conteniendo "principiante"
  y context_used: ["audience"]

================================================================================
SPRINT 4 — DOCUMENTACIÓN FINAL Y CIERRE
================================================================================

QUÉ SE HIZO:
Se cerró el proyecto con documentación final completa. Se reescribió el README.md
con arquitectura, endpoints, decisiones técnicas y resumen Scrum. Se validó el
proyecto completo con ./test.sh obteniendo 3/3 pruebas de validación en verde.
Se creó la rama feature/cag-implementation, se hizo el Pull Request hacia main
en GitHub y se realizó el merge final.

ARCHIVOS MODIFICADOS:
- README.md (completamente reescrito)
- docs/SPRINT4.md (creado)
- PROMPTS.md (Entry 4 agregada)

PROMPT UTILIZADO:
--------------------------------------------------------------------------------
You are my development assistant (Jarvis). We are in the final sprint.

The project already has implemented:
- ContextStore in memory (context_store.py)
- apply_context that enriches responses with user context (cag.py)
- answer_question integrated with CAG (assistant.py)
- All validation tests passing

Your task is to generate the final documentation content to close the project:
1. Complete and well-structured README.md with these sections:
   - Title: RAG + CAG System - Final Project Module 3
   - Project description (what it does, what problem it solves)
   - Architecture: explain base RAG + added CAG module
   - Folder structure with description of each important file
   - Installation and execution instructions
   - Endpoint descriptions: GET /health, POST /api/ask, POST /api/context,
     GET /api/context
   - Scrum section: summary of the 4 sprints
   - Technical decisions section (why memory and not DB, how circular import
     was avoided, thread-safety)
   - References to docs/evidencias/
2. Last entry for PROMPTS.md (fourth entry, sprint 4)
3. Content of docs/SPRINT4.md with objective, completed tasks, retrospective,
   status CLOSED
--------------------------------------------------------------------------------

DECISIÓN HUMANA: Se aprobó la documentación final, se ejecutaron los comandos
git, se creó y mergeó el PR en GitHub.

CAPTURAS:
- sprint4-proyecto-funcionando.png → frontend con respuesta RAG sin contexto
- sprint4-tests-ok.png → output de ./test.sh con Ran 3 tests — OK
- sprint4-pr-github.png → Pull Request en GitHub mergeado a main

================================================================================
RESULTADOS FINALES
================================================================================

PRUEBAS:
  Base (3 tests)       → OK ✓
  Validación (3 tests) → OK ✓
  ./test.sh            → OK ✓

DECISIONES TÉCNICAS CLAVE:
  1. Almacenamiento en memoria: se usó dict Python en lugar de base de datos
     porque las pruebas crean instancias frescas del servidor — una DB
     persistente requeriría setup/teardown entre tests.

  2. Evitar importación circular: server.py obtiene el contexto y lo pasa
     como parámetro a answer_question(). assistant.py no importa nada de
     server.py.

  3. Thread-safety: threading.Lock() dentro de ContextStore serializa todas
     las lecturas y escrituras — necesario porque ThreadingHTTPServer maneja
     cada request en su propio thread.

ENTREGA:
  URL del fork: https://github.com/WdeWonka/final_project_AI_CUSTOM_wg
  Rama principal: main
  Pull Requests: 2 (develop → main, feature/cag-implementation → main)

================================================================================
FIN DEL INFORME
================================================================================
