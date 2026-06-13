def apply_context(user_id, question, base_answer, context_items):
    if not context_items:
        return {"answer": base_answer, "context_used": []}

    values = " ".join(item["value"] for item in context_items)
    keys = [item["key"] for item in context_items]
    enriched_answer = f"{base_answer} [Contexto del usuario: {values}]"
    return {"answer": enriched_answer, "context_used": keys}
