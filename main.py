from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os


from app.utils.redis_client import redis_client
from app.routes.chat import chat_bp  


load_dotenv()

def create_app():
    app = Flask(__name__)
    
    
    CORS(app)

    
    app.register_blueprint(chat_bp, url_prefix="/api/chat")

    
    try:
        redis_client.ping()
        print("✅ Redis connected")
    except Exception as e:
        print("❌ Redis connection failed:", str(e))

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
