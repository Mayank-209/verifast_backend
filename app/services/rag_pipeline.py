import os
from app.utils.jina_embed import get_embedding  # You’ll create this
from app.utils.qdrant_client import query_qdrant  # You’ll create this
from app.utils.gemini import query_gemini  # You’ll create this

def generate_response(user_query: str, top_k: int = 5) -> str:
    # Step 1: Embed the query using Jina Embeddings API
    query_embedding = get_embedding(user_query)
    if not query_embedding:
        return "Failed to embed the query."

    # Step 2: Search Qdrant for top-k similar documents
    documents = query_qdrant(query_embedding, top_k=top_k)
    if not documents:
        return "I couldn't find any relevant information."

    # Step 3: Build context string
    context = "\n\n".join(doc['text'] for doc in documents)

    # Step 4: Send prompt to Gemini
    prompt = f"""Use the following context to answer the question:\n\n{context}\n\nQuestion: {user_query}"""

    answer = query_gemini(prompt)
    return answer or "Gemini could not generate a response."
