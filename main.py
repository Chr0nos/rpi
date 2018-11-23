from flask import Flask
from relay import Relay
app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():
    return "Hello world"

