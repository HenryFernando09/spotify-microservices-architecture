from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

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

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()

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
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
