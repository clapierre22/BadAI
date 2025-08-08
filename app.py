from flask import Flask, request, jsonify, render_template
from src.chatbot.chatbot import BadAI

app = Flask(__name__)
chatbot = BadAI()

@app.route("/")
def home():
    return render_template("badai.html")

@app.route("/process_input", methods=["POST"])
def process_input():
    try:
        data = request.json.get("user_input")
        if not data: return jsonify({"error": "No input provided"}), 400

        user_input = data.get("user_input")
        if not user_input or not isinstance(user_input, str): return jsonify({"error": "Invalid input"}), 400
        
        response = chatbot.process_input(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)