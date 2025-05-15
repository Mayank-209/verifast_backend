import os
import uuid
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  # This will load environment variables from your .env file
from app.utils.jina_embed import get_embedding  # Jina embedding helper

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "news_articles")

def create_collection_if_not_exists():
    """Create Qdrant collection if it doesn't exist (dense vector, cosine distance)"""
    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}"
    headers = {"api-key": QDRANT_API_KEY, "Content-Type": "application/json"}
    data = {
        "vectors": {
            "size": 768,  # Jina V2 base is 768-dim
            "distance": "Cosine"
        }
    }
    try:
        res = requests.put(url, headers=headers, json=data)
        print("✅ Collection checked/created:", res.json())
    except Exception as e:
        print("❌ Error creating collection:", str(e))

def upload_to_qdrant(vectors):
    """Upload list of vectors to Qdrant"""
    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points"
    headers = {"api-key": QDRANT_API_KEY, "Content-Type": "application/json"}

    try:
        res = requests.put(url, headers=headers, json={"points": vectors})
        print("✅ Uploaded to Qdrant:", res.json())
    except Exception as e:
        print("❌ Upload error:", str(e))

def ingest_articles():
    # Example hardcoded articles
    articles = [
        {
            "title": "Global Markets Surge",
            "text": "Global markets rallied today amid easing inflation concerns...",
            "url": "https://example.com/markets"
        },
        {
            "title": "New AI Breakthrough Announced",
            "text": "A major tech company revealed a new breakthrough in AI language models...",
            "url": "https://example.com/ai-news"
        },
    ]

    vectors = []

    for article in articles:
        embedding = get_embedding(article["text"])  # Call Jina to get embeddings
        if embedding:
            vectors.append({
                "id": str(uuid.uuid4()),  # Unique ID
                "vector": embedding,      # Jina's embedding
                "payload": {
                    "title": article["title"],
                    "text": article["text"],
                    "url": article["url"]
                }
            })

    create_collection_if_not_exists()  # Ensure the Qdrant collection exists
    upload_to_qdrant(vectors)         # Upload vectors to Qdrant

if __name__ == "__main__":
    ingest_articles()
