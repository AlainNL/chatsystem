from flask import Flask, request, jsonify

app = Flask(__name__)

#Route for manage the messages
@app.route('/chat', methods=['POST'])
def chat():
    try:
        #collect JSON data send by front-end
        data = request.get_json()

        #validate history (user/agent)
        if not validate_history(data['history']):
            return jsonify({"error": "Incorrect chat history"}), 400

        #generate static response of agent
        agent_reply = generate_agent_reply()


#Function to validate chat message history
def validate_history(history_message):
    for i in range(len(history_message) - 1)
