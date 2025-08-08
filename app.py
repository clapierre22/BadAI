import sys, os, traceback

from flask import Flask, request, jsonify, render_template
# from src.chatbot.chatbot import BadAI

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
chatbot = None

def init_chatbot():
    global chatbot
    try:
        from src.chatbot.chatbot import BadAI
        print("BadAI Import Success")

        chatbot = BadAI()
        print("BadAI Init Success")
        return True
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

@app.route("/")
def home():
    global chatbot
    if chatbot is None:
        init = init_chatbot()
        if not init:
            return "Error: Could not Init Chatbot"
    return render_template("badai.html")

@app.route("/process_input", methods=["POST"])
def process_input():
    global chatbot
    
    try:
        if chatbot is None:
                print("Chatbot not initialized, attempting to initialize...")
                success = init_chatbot()
                if not success:
                    return jsonify({"error": "Chatbot initialization failed"}), 500
        
        # Get request data with better error handling
        print(f"Request content type: {request.content_type}")
        print(f"Request data: {request.data}")
        print(f"Request form: {request.form}")
        
        # Try to get JSON data
        try:
            data = request.get_json()
            print(f"Parsed JSON data: {data}")
            print(f"Data type: {type(data)}")
        except Exception as json_error:
            print(f"JSON parsing failed: {json_error}")
            data = None
        
        # Fallback: try to get from form data
        if data is None:
            print("Trying form data...")
            user_input = request.form.get('user_input')
            if user_input:
                print(f"Got from form: {user_input}")
                data = {"user_input": user_input}
        
        # Fallback: try raw data
        if data is None and request.data:
            print("Trying raw data...")
            try:
                import json
                data = json.loads(request.data.decode('utf-8'))
                print(f"Parsed raw data: {data}")
            except:
                print("Raw data parsing failed")
        
        if not data:
            print("No data received in any format")
            return jsonify({"error": "No data provided"}), 400
        
        # Handle string data (in case JSON parsing gives us a string)
        if isinstance(data, str):
            print(f"Data is string: {data}")
            # Try to parse as JSON string
            try:
                import json
                data = json.loads(data)
            except:
                # Assume the string IS the user input
                user_input = data
                data = {"user_input": user_input}
        
        user_input = data.get("user_input") if isinstance(data, dict) else str(data)
        print(f"Final user input: '{user_input}'")
        
        if not user_input or not str(user_input).strip():
            print("Empty user input")
            return jsonify({"error": "No input provided"}), 400
        
        # Process input through chatbot
        print("Calling chatbot.process_input...")
        response = chatbot.process_input(str(user_input).strip())
        print(f"Chatbot response: '{response}'")
        
        return jsonify({"response": response})
        
    except Exception as e:
        error_msg = f"Error in process_input: {str(e)}"
        print(error_msg)
        print(f"Full traceback:\n{traceback.format_exc()}")
        return jsonify({"error": error_msg}), 500

if __name__ == "__main__":
    app.run(debug=True)