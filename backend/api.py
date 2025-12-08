import traceback
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import os
import sys

# -----------------------------
# PATH SETUP
# -----------------------------
BACKEND_DIR = Path(__file__).resolve().parent        # /backend
BASE_DIR = BACKEND_DIR.parent                       # project root
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"

# Fix Python import paths
sys.path.insert(0, str(BASE_DIR))

from backend.transcriber import Transcriber
from backend.summarizer import Summarizer
from backend.chatbot import LectureChatbot

# -----------------------------
# CONSTANTS
# -----------------------------
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB in bytes
ALLOWED_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.webm'}

# -----------------------------
# FLASK APP
# -----------------------------
app = Flask(
    __name__,
    static_folder=str(STATIC_DIR),
    static_url_path="/static"
)
CORS(app)

transcriber = Transcriber()
summarizer = Summarizer()
chatbot = LectureChatbot()

# -----------------------------
# FRONTEND ROUTES
# -----------------------------
@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/gaku_logo.png")
def serve_logo():
    return send_from_directory(FRONTEND_DIR, "gaku_logo.png")

@app.route("/gaku_background.png")
def serve_bg():
    return send_from_directory(FRONTEND_DIR, "gaku_background.png")

# -----------------------------
# API: TRANSCRIBE (IMPROVED)
# -----------------------------
@app.route("/transcribe", methods=["POST"])
def transcribe_api():
    try:
        if "file" not in request.files:
            return jsonify({"status": "error", "error": "No file uploaded"}), 400

        file = request.files["file"]
        
        # Validate file has a name
        if not file.filename:
            return jsonify({"status": "error", "error": "No file selected"}), 400
        
        # Validate file extension
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()
        
        if ext not in ALLOWED_EXTENSIONS:
            return jsonify({
                "status": "error", 
                "error": f"Invalid file type. Allowed types: MP3, WAV, M4A, WEBM"
            }), 400
        
        # Validate file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset pointer to beginning
        
        if file_size > MAX_FILE_SIZE:
            size_mb = file_size / (1024 * 1024)
            return jsonify({
                "status": "error",
                "error": f"File too large ({size_mb:.1f}MB). Maximum size is 200MB"
            }), 400
        
        if file_size == 0:
            return jsonify({
                "status": "error",
                "error": "File is empty"
            }), 400

        temp_path = BASE_DIR / f"temp_upload{ext}"
        
        # Use try-finally for proper cleanup
        try:
            file.save(temp_path)
            print(f"✅ File saved: {temp_path} ({file_size / (1024*1024):.1f}MB)")
            
            result = transcriber.transcribe_audio(str(temp_path))
            return jsonify(result)
            
        finally:
            # Always try to clean up temp file
            try:
                if temp_path.exists():
                    temp_path.unlink()
                    print(f"🗑️ Cleaned up temp file: {temp_path}")
            except Exception as cleanup_error:
                print(f"⚠️ Warning: Could not delete temp file: {cleanup_error}")

    except Exception as e:
        print("\n🔥 BACKEND CRASH 🔥")
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500


# -----------------------------
# API: SET CONTEXT
# -----------------------------
@app.route("/set_context", methods=["POST"])
def context_api():
    data = request.get_json()
    transcript = data.get("transcript", "")
    
    if not transcript.strip():
        return jsonify({"status": "error", "error": "Empty transcript"}), 400
    
    chatbot.set_lecture_context(transcript)
    return jsonify({"status": "success"})


# -----------------------------
# API: SUMMARY (ENHANCED)
# -----------------------------
@app.route("/summary", methods=["POST"])
def summary_api():
    data = request.get_json()
    text = data.get("text", "")
    
    if not text.strip():
        return jsonify({"status": "error", "error": "No text provided"}), 400
    
    return jsonify(summarizer.generate_summary(text))


# -----------------------------
# API: CHAT
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    question = data.get("question", "")
    
    if not question.strip():
        return jsonify({"status": "error", "error": "No question provided"}), 400
    
    return jsonify(chatbot.ask_question(question))


# -----------------------------
# API: QUIZ
# -----------------------------
@app.route("/quiz", methods=["POST"])
def quiz_api():
    data = request.get_json()
    num_questions = data.get("num_questions", 5)
    
    # Validate num_questions
    if not isinstance(num_questions, int) or num_questions < 1 or num_questions > 20:
        num_questions = 5
    
    return jsonify(chatbot.get_quiz_questions(num_questions))


# -----------------------------
# API: EXPLAIN
# -----------------------------
@app.route("/explain", methods=["POST"])
def explain_api():
    data = request.get_json()
    concept = data.get("concept", "")
    
    if not concept.strip():
        return jsonify({"status": "error", "error": "No concept provided"}), 400
    
    return jsonify(chatbot.explain_concept(concept))


# -----------------------------
# API: FLASHCARDS (NEW)
# -----------------------------
@app.route("/flashcards", methods=["POST"])
def flashcards_api():
    data = request.get_json()
    num_cards = data.get("num_questions", 10)
    
    # Validate num_cards
    if not isinstance(num_cards, int) or num_cards < 1 or num_cards > 30:
        num_cards = 10
    
    transcript = chatbot.lecture_context
    
    if not transcript:
        return jsonify({
            "status": "error",
            "flashcards": None,
            "error": "No lecture context set. Please transcribe a lecture first."
        })
    
    return jsonify(summarizer.generate_flashcards(transcript, num_cards))


# -----------------------------
# ERROR HANDLERS
# -----------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"status": "error", "error": "Internal server error"}), 500


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 GAKU LECTURE SUMMARIZER")
    print("=" * 60)
    print("📍 Running at: http://127.0.0.1:5000")
    print("📁 Frontend:  ", FRONTEND_DIR)
    print("📁 Static:    ", STATIC_DIR)
    print("=" * 60)
    app.run(debug=True, port=5000, host='127.0.0.1')