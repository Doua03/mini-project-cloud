from flask import Flask, jsonify, request, render_template, json
import psycopg2, redis, os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

r = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/tasks", methods=["GET"])
def get_tasks():
    cached = r.get("tasks")
    if cached:
        return cached, 200, {"Content-Type": "application/json"}
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tasks;")
    tasks = [{"id": row[0], "title": row[1]} for row in cur.fetchall()]
    conn.close()
    r.setex("tasks", 30, json.dumps(tasks))
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id;", (data["title"],))
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    r.delete("tasks")
    return jsonify({"id": new_id, "title": data["title"]}), 201

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()
    conn.close()
    r.delete("tasks")
    return jsonify({"message": "deleted"}), 200

@app.route("/health")
def health():
    visits = r.incr("visit_count")
    return jsonify({"status": "ok", "visits": int(visits)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)