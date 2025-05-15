import feedparser
from datetime import datetime
import uuid
from app.utils.jina_embed import get_embedding
from app.utils.qdrant_client import upload_to_qdrant

def rss_ingest(rss_url: str, collection_name: str):
    """
    Fetches articles from RSS feed, embeds them, and uploads to Qdrant.
    
    Args:
        rss_url (str): URL of the RSS feed.
        collection_name (str): Qdrant collection name.
    """
    feed = feedparser.parse(rss_url)
    if feed.bozo:
        print(f"Error parsing RSS feed: {feed.bozo_exception}")
        return
    
    articles = []
    for entry in feed.entries[0:50]:
        title = entry.get("title", "")
        link = entry.get("link", "")
        published = entry.get("published", "")
        summary = entry.get("summary", "") or entry.get("description", "")

        text = f"{title}\n\n{summary}"
        embedding = get_embedding(text)
        if not embedding:
            print(f"Failed to get embedding for article: {title}")
            continue
        
        try:
            published_date = datetime(*entry.published_parsed[:6]).isoformat()
        except Exception:
            published_date = published
        
        doc = {
            "id": str(uuid.uuid5(uuid.NAMESPACE_URL, link)),  # valid UUID from URL
            "text": text,
            "title": title,
            "link": link,
            "published": published_date,
            "embedding": embedding,
        }
        articles.append(doc)

    if not articles:
        print("No articles to upload.")
        return
    
    result = upload_to_qdrant( articles)
    print(f"Uploaded {len(articles)} articles to Qdrant collection '{collection_name}': {result}")

if __name__ == "__main__":
    RSS_FEED_URL = "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en"
    COLLECTION_NAME = "news_articles"
    rss_ingest(RSS_FEED_URL, COLLECTION_NAME)
