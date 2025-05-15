import os
from app.utils.jina_embed import get_embedding  
from app.utils.qdrant_client import query_qdrant 
from app.utils.gemini import query_gemini 

def generate_response(user_query: str, top_k: int = 5) -> str:
    
    query_embedding = get_embedding(user_query)
    if not query_embedding:
        return "Failed to embed the query."

    
    documents = query_qdrant(query_embedding, top_k=top_k)
    if not documents:
        return "I couldn't find any relevant information."

    
    context = "\n\n".join(doc['text'] for doc in documents)

    
    prompt = f"""Use the following context to answer the question:\n\n{context}\n\nQuestion: {user_query}"""

    answer = query_gemini(prompt)
    return answer or "Gemini could not generate a response."
