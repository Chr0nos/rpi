from flask import Flask, abort
from relay import Relay
app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():
    return "Hello world"

@app("/set/<port>/<state>", methods=['POST'])
def set_relay_state(port, state):
    try:
        port = int(port)
        state = bool(state)
        r = Relay()
        r.setEnabled(port, state)
        return "OK"
    except ValueError:
        abort(400)
    except IndexError:
        abort(406)

@app("/get/<port>", methods=['GET'])
def get_relay_state(port):
    try:
        port = int(port)
        return "TODO"
