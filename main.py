import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)

PORT = int(os.environ.get("APP_PORT", 3333))


def get_db_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", 5432),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            value VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    return jsonify({"service": "commit-test", "status": "running"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/add")
def add_entry():
    name = request.args.get("name")
    value = request.args.get("value")
    if not name or not value:
        return jsonify({"error": "Both 'name' and 'value' query params are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO entries (name, value) VALUES (%s, %s) RETURNING id", (name, value))
    entry_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Entry added", "id": entry_id})


@app.route("/entries")
def get_entries():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, value, created_at FROM entries ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    entries = [{"id": r[0], "name": r[1], "value": r[2], "created_at": r[3].isoformat()} for r in rows]
    return jsonify({"entries": entries})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=PORT)
