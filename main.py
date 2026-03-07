import os
from flask import Flask, jsonify

app = Flask(__name__)

PORT = int(os.environ.get("APP_PORT", 3333))


@app.route("/")
def index():
    return jsonify({"service": "commit-test", "status": "running"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
