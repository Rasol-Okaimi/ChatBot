from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample simple chatbot logic
def get_bot_response(user_message):
    user_message = user_message.lower()
    if "hello" in user_message:
        return "Hello! How can I help you today?"
    elif "python" in user_message:
        return "Python is a popular programming language!"
    elif "bye" in user_message:
        return "Goodbye! Have a nice day!"
    else:
        return "Sorry, I don't understand that."

@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.form.get("message")
    bot_response = get_bot_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
  app.run(debug=True, port=5001)