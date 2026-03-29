from flask import Flask, render_template, request, jsonify, session
from thaillm_client import chat
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "ข้อความว่างเปล่า"}), 400

    # Get conversation history from session
    if "messages" not in session:
        session["messages"] = []

    session["messages"].append({"role": "user", "content": user_message})

    try:
        result = chat(session["messages"])
        reply = result["choices"][0]["message"]["content"]
        session["messages"].append({"role": "assistant", "content": reply})
        session.modified = True
        return jsonify({"reply": reply})
    except Exception as e:
        session["messages"].pop()
        return jsonify({"error": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def clear_chat():
    session["messages"] = []
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
