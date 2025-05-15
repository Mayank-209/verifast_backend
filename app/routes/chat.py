from flask import Blueprint, request, jsonify
import uuid

from app.utils.redis_client import save_message, get_session_history, clear_session
from app.services.rag_pipeline import generate_response  # You'll define this next

chat_bp = Blueprint("chat", __name__)

# POST /api/chat/message
@chat_bp.route("/message", methods=["POST"])
def handle_message():
    data = request.get_json()
    user_message = data.get("message")
    session_id = data.get("session_id") or str(uuid.uuid4())  # new session if none provided

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Save user message to Redis
    save_message(session_id, "user", user_message)

    # Generate response using RAG pipeline
    try:
        bot_response = generate_response(user_message)
    except Exception as e:
        bot_response = "Sorry, I had trouble processing that."
        print("RAG Error:", str(e))

    # Save bot response to Redis
    save_message(session_id, "bot", bot_response)

    # Fetch full chat history
    history = get_session_history(session_id)

    return jsonify({
        "session_id": session_id,
        "response": bot_response,
        "history": history
    })

# GET /api/chat/history/<session_id>
@chat_bp.route("/history/<session_id>", methods=["GET"])
def get_history(session_id):
    history = get_session_history(session_id)
    return jsonify({
        "session_id": session_id,
        "history": history
    })

# DELETE /api/chat/clear/<session_id>
@chat_bp.route("/clear/<session_id>", methods=["DELETE"])
def clear(session_id):
    clear_session(session_id)
    return jsonify({
        "message": f"Session {session_id} cleared."
    })
