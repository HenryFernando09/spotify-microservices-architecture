from flask import Flask, request, jsonify

app = Flask(__name__)

users = []

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

    for user in users:
        if user["username"] == username:
            return jsonify({
                "message": "User already exists"
            }), 409

    users.append({
        "username": username,
        "password": password
    })

    return jsonify({
        "message": "User registered successfully",
        "user": username
    }), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    for user in users:
        if user["username"] == username and user["password"] == password:
            return jsonify({
                "message": "Login successful",
                "user": username
            }), 200

    return jsonify({
        "message": "Invalid credentials"
    }), 401

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({
        "users": users
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    