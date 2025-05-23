

# 🧠 Verifast Backend - RAG Chatbot API

This is the backend for the Verifast RAG-powered chatbot, built using Flask. It integrates:
- Jina Embeddings API (text embeddings)
- Qdrant Cloud (vector DB)
- Gemini API (LLM response generation)
- Redis Cloud (caching + session memory)

---

## 🚀 Features

- Embedding generation and indexing of news articles
- Contextual Q&A over indexed news using RAG
- Session-based history with Redis
- Modular Flask codebase for scalability

---

## ⚙️ Setup Instructions

```bash
# Clone the backend repo
git clone https://github.com/yourname/verifast_backend.git
cd verifast_backend

# Create a virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
### Add environment variables
```
REDIS_URL=your_redis_url
QDRANT_API_KEY=your_qdrant_key
QDRANT_URL=https://your-qdrant-url
GEMINI_API_KEY=your_gemini_key
PORT=8000
```
### Run the app
```bash
python -m main
```
## 🧪 API Endpoints
```
POST /api/chat/message
```
- Accepts a user message
- Returns a response from the LLM based on vector-retrieved context

```
GET /api/history/<sessionId>
```
- Gets the chat history of previous conversations.

```
DELETE /api/clear/<sessionId>
```
- Deletes a conversation from the redis database
## 📌 Notes
- All context is fetched from Qdrant before querying the Gemini model.
- Redis is used to store session context for smoother user interaction.
