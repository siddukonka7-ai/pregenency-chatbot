from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

from responses import get_response
from database import (
    init_db,
    create_user,
    get_user,
    get_user_by_id,
    update_password,
    save_chat,
    get_chat_history
)

app = Flask(__name__)
app.secret_key = "janani_care_secret_key"

# Initialize database
init_db()


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])

    return render_template(
        "index.html",
        username=session["username"],
        guardian_name=user[4],
        guardian_mobile=user[5]
    )


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        mobile = request.form.get("mobile")
        guardian_name = request.form.get("guardian_name")
        guardian_mobile = request.form.get("guardian_mobile")

        if not username or not password or not confirm_password:
            return render_template("register.html", error="All fields required")

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        if get_user(username):
            return render_template("register.html", error="User already exists")

        hashed_password = generate_password_hash(password)
        create_user(username, hashed_password, mobile, guardian_name, guardian_mobile)

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user(username)

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("home"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form.get("username")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        user = get_user(username)

        if not user:
            return render_template("forgot_password.html", error="User not found")

        if new_password != confirm_password:
            return render_template("forgot_password.html", error="Passwords do not match")

        hashed_password = generate_password_hash(new_password)
        update_password(username, hashed_password)

        return render_template("forgot_password.html", success="Password updated successfully")

    return render_template("forgot_password.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    if "user_id" not in session:
        return jsonify({"response": "Please login first"})

    data = request.get_json()
    message = data.get("message")

    response = get_response(message, session["user_id"])

    save_chat(session["user_id"], message, response)

    return jsonify({"response": response})


# ---------------- HISTORY ----------------
@app.route("/history")
def history():
    if "user_id" not in session:
        return jsonify([])

    chats = get_chat_history(session["user_id"])

    return jsonify([
        {"user": c[0], "bot": c[1]} for c in chats
    ])


# ---------------- RUN (IMPORTANT FOR RENDER) ----------------
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
