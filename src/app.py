from flask import Flask, request, jsonify, render_template
from chatbot.chatbot import BadAI
# TODO: Flask still will not import correctly

app = Flask(__name__)
chatbot = BadAI()

@app.route("/")
def home():
    return render_template("badai.html")

@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.json.get("user_input")
    if not user_input: return jsonify({"error": "No input provided"}), 400
    
    response = chatbot.process_input(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)