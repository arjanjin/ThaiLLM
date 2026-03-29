import json
import os
import uuid
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template, request, stream_with_context

from thaillm_client import chat_stream

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

CHATS_DIR = os.path.join(os.path.dirname(__file__), "chats")
os.makedirs(CHATS_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat/stream", methods=["POST"])
def api_chat_stream():
    data = request.get_json()
    messages = data.get("messages", [])
    system_prompt = data.get("system_prompt", "").strip()

    if not messages or messages[-1].get("role") != "user":
        return jsonify({"error": "ไม่มีข้อความ"}), 400

    all_messages = []
    if system_prompt:
        all_messages.append({"role": "system", "content": system_prompt})
    all_messages.extend(messages)

    def generate():
        try:
            for raw in chat_stream(all_messages):
                if raw == "[DONE]":
                    yield f"data: {json.dumps({'done': True})}\n\n"
                    return
                try:
                    chunk = json.loads(raw)
                    content = chunk["choices"][0].get("delta", {}).get("content", "")
                    if content:
                        yield f"data: {json.dumps({'content': content})}\n\n"
                except (json.JSONDecodeError, KeyError, IndexError):
                    pass
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/api/history", methods=["GET"])
def list_history():
    items = []
    for fname in sorted(os.listdir(CHATS_DIR), reverse=True):
        if fname.endswith(".json"):
            path = os.path.join(CHATS_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                chat_data = json.load(f)
            items.append({
                "id": fname[:-5],
                "title": chat_data.get("title", "Untitled"),
                "saved_at": chat_data.get("saved_at", ""),
                "message_count": len(chat_data.get("messages", [])),
            })
    return jsonify(items)


@app.route("/api/history/save", methods=["POST"])
def save_history():
    data = request.get_json()
    messages = data.get("messages", [])
    if not messages:
        return jsonify({"error": "ไม่มีข้อความในการสนทนา"}), 400

    title = data.get("title", "").strip()
    if not title:
        first_user = next((m["content"] for m in messages if m["role"] == "user"), "Untitled")
        title = first_user[:50] + ("..." if len(first_user) > 50 else "")

    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]
    path = os.path.join(CHATS_DIR, f"{chat_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "id": chat_id,
            "title": title,
            "saved_at": datetime.now().isoformat(),
            "system_prompt": data.get("system_prompt", ""),
            "messages": messages,
        }, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "ok", "id": chat_id, "title": title})


@app.route("/api/history/<chat_id>", methods=["GET"])
def load_history(chat_id):
    if not all(c.isalnum() or c in "-_" for c in chat_id):
        return jsonify({"error": "Invalid ID"}), 400
    path = os.path.join(CHATS_DIR, f"{chat_id}.json")
    if not os.path.exists(path):
        return jsonify({"error": "ไม่พบไฟล์"}), 404
    with open(path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@app.route("/api/history/<chat_id>", methods=["DELETE"])
def delete_history(chat_id):
    if not all(c.isalnum() or c in "-_" for c in chat_id):
        return jsonify({"error": "Invalid ID"}), 400
    path = os.path.join(CHATS_DIR, f"{chat_id}.json")
    if not os.path.exists(path):
        return jsonify({"error": "ไม่พบไฟล์"}), 404
    os.remove(path)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
