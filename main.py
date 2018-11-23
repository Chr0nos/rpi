from flask import Flask, abort
from relay import Relay
app = Flask(__name__)

DB = "states.json"

@app.route("/", methods=['GET'])
def main():
	return "Hello world"

@app.route("/set/<port>/<state>", methods=['POST'])
def set_relay_state(port, state):
	try:
		port = int(port)
		state = bool(state)
		Relay(database=DB).setEnabled(port, state)
		return "OK\n"
	except (ValueError, TypeError) as e:
		abort(400)
	except IndexError:
		abort(406)

@app.route("/get/<port>", methods=['GET'])
def get_relay_state(port):
	try:
		port = int(port)
		Relay(database=DB).update()
		return "TODO"
	except TypeError:
		abort(400)

@app.route("/reset", methods=['POST'])
def reset():
	Relay(True).setAll(False)
	return "OK\n"
