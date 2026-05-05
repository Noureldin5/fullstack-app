from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)


def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# GET /api/data — list all tasks
@app.route("/api/data", methods=["GET"])
def get_data():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tasks ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "title": r[1]} for r in rows])


# POST /api/data — add a task
@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.get_json()
    title = (data or {}).get("title", "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id", (title,))
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"id": new_id, "title": title}), 201


# DELETE /api/data/<id> — remove a task
@app.route("/api/data/<int:item_id>", methods=["DELETE"])
def delete_data(item_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (item_id,))
    deleted = cur.fetchone()
    conn.commit()
    conn.close()
    if not deleted:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"deleted": item_id})


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
