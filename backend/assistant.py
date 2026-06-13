from backend.knowledge import retrieve_snippets
from backend.cag import apply_context


def answer_question(user_id, question, context_items=None):
    if context_items is None:
        context_items = []

    snippets = retrieve_snippets(question)

    if not snippets:
        base_answer = "No encontre informacion suficiente en la base de conocimiento del curso."
        result = apply_context(user_id, question, base_answer, context_items)
        return {
            "user_id": user_id,
            "answer": result["answer"],
            "sources": [],
            "context_used": result["context_used"],
        }

    source_text = " ".join(item["content"] for item in snippets)
    base_answer = f"Segun la base de conocimiento del curso: {source_text}"
    result = apply_context(user_id, question, base_answer, context_items)

    return {
        "user_id": user_id,
        "answer": result["answer"],
        "sources": [item["id"] for item in snippets],
        "context_used": result["context_used"],
    }
