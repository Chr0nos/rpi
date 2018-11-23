from flask import Flask, abort, render_template, request
from relay import Relay
app = Flask(__name__, template_folder="./templates/")

DB = "states.json"

@app.route("/", methods=['GET'])
def main():
	r = Relay(database=DB, ro=True)
	switches = [
		{'name': 'Eclairage', 'state': r.states[0], 'index': 0},
		{'name': 'Co2', 'state': r.states[1], 'index': 1},
		{'name': 'Brassage', 'state': r.states[2], 'index': 2},
		{'name': 'Unused', 'state': r.states[3], 'index': 3}
	]
	return render_template("index.html", switches=switches)

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

@app.route("/set", methods=['POST'])
def set_state():
	try:
		idx = int(request.form['index'])
		state = bool(request.form['state'])
	except ValueError:
		abort(400)

	r = Relay(database=DB)
	r.setEnabled(idx, state)
	return "OK\n"
