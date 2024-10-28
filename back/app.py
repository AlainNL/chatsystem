from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)


def require_valid_chat_history(f):
    """Decorator for check if history is valid between call function"""
    @wraps(f) # Retains original function metadata
    def validate_and_proceed(*args, **kwargs):
        # Collect JSON data sending by front-end
        data = request.get_json()

        # Validate history (user/agent)
        if not validate_history(data['history']):
            return jsonify({"error": "Incorrect chat history"}), 400

        return f(*args, **kwargs) # Calls the original function if the history is valid
    return validate_and_proceed


# Route for manage the messages
@app.route('/chat', methods=['POST', 'GET'])
@require_valid_chat_history
def chat():
    if request.method == 'POST':
        try:
            # generate static response of agent
            agent_reply = generate_agent_reply()

            # return agent response
            return jsonify({"agent_reply": agent_reply})

        except KeyError:
            return jsonify({"error": "Bad Request"}), 400

    elif request.method == 'GET':
        return jsonify({"status": "Server run"}), 200

if __name__ == '__main__':
    # Create WSGI server with Gevent for running multiple concurrent calls
    http_server = WSGIServer(("127.0.0.1", 5000), app)
    http_server.serve_forever()
    app.run(debug=True)

# conditions to validate chat history
def validate_history(history):

    # check if history is a list
    if not isinstance(history, list):
        return False

    # if history is empty, done
    if len(history) == 0:
        return True

    # expect alternating entre 'user' / 'agent'
    expected_sender = 'user'

    for message in history:

        # Check that each message is a dictionary with 'sender' and 'message'.
        if not isinstance(message, dict) or 'sender' not in message or 'message' not in message:
            return False

        # Check if key sender is correct
        if message['sender'] not in ['user', 'agent']:
            return False

        # Check if message comes from the expected sender
        if message['sender'] != expected_sender:
            return False

        # Alternate the expected sender
        expected_sender = 'agent' if expected_sender == 'user' else 'user'

    return True

# Generate static agent response
def generate_agent_reply():
    return "How can I help you ?"
