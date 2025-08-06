from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory user storage
users = {
    1: {"name": "John Doe", "email": "john@example.com"},
    2: {"name": "Jane Smith", "email": "jane@example.com"}
}

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

# GET user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# POST create new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid data"}), 400

    user_id = max(users.keys()) + 1 if users else 1
    users[user_id] = {"name": data["name"], "email": data["email"]}
    return jsonify({"message": "User created", "user_id": user_id}), 201

# PUT update user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    users[user_id].update(data)
    return jsonify({"message": "User updated", "user": users[user_id]}), 200

# DELETE user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
