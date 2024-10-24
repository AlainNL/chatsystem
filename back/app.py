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

        #return agent response
        return jsonify({"agent_reply": agent_reply})

    except KeyError:
        return jsonify({"error": "Bad Request"}), 400

    if __name__ == '__main__':
        app.run(debug=True)

#validate chat history
def validate_history(history):

    #check if history is a list
    if not isinstance(history, list):
        return False

    #if history is empty, done
    if len(history) == 0:
        return True

    #expect alternating entre 'user' / 'agent'
    expected_sender = 'user'

    for message in history:

        # Check that each message is a dictionary with 'sender' and 'message'.
        if not isinstance(message, dict) or 'sender' not in message or 'message' not in message:
            return False

        #check if sender is correct
        if message['sender'] not in ['user', 'agent']:
            return False

        #check if message comes from the expected sender
        if message['sender'] != expected_sender:
            return False

        #Alternate the expected sender
        expected_sender = 'agent' if expected_sender == 'user' else 'user'

    return True

#generate agent response
def generate_agent_reply():
    return "How can I help you?"
