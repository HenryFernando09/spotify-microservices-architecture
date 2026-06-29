from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

app = Flask(__name__)
register_counter = Counter("auth_register_total", "Total de registros")
login_counter = Counter("auth_login_total", "Total de logins")

def init_db():
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return jsonify({
        "service": "Auth Service",
        "status": "running"
    })

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "message": "Username and password are required"
        }), 400

    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({
            "message": "User already exists"
        }), 409

    hashed_password = generate_password_hash(password)

    cursor.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    (username, hashed_password)
    )

    conn.commit()
    conn.close()

    register_counter.inc()

    return jsonify({
        "message": "User registered successfully",
        "user": username
    }), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[2], password):

        login_counter.inc()

        return jsonify({
            "message": "Login successful",
            "user": username
        }), 200

    return jsonify({
        "message": "Invalid credentials"
    }), 401

@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()

    conn.close()

    usernames = []

    for user in users:
        usernames.append({
            "username": user[0]
        })

    return jsonify({
        "users": usernames
    })

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

