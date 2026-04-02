from flask import Blueprint, request, redirect, session
import hashlib

from db import get_db_connection
from templates import render

bp = Blueprint("auth", __name__)


# VULN: SQL Injection in Login
@bp.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        md5_pass = hashlib.md5(password.encode()).hexdigest()

        # VULNERABLE: direct string concatenation in SQL
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{md5_pass}'"
        try:
            db = get_db_connection()
            user = db.execute(query).fetchone()
            if user:
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["role"] = user["role"]
                return redirect("/profile")
            else:
                error = "Invalid credentials"
        except Exception as e:
            error = f"Error: {e}"  # VULNERABLE: shows SQL errors

    return render(
        "Login",
        f"""
        <p class='danger'>{error}</p>
        <form method='POST'>
            <input name='username' placeholder='Username'>
            <input name='password' type='password' placeholder='Password'>
            <button type='submit'>Login</button>
        </form>
        """,
    )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@bp.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        email = request.form.get("email", "")
        # VULNERABLE: MD5 hash + no salt
        md5_pass = hashlib.md5(password.encode()).hexdigest()
        try:
            db = get_db_connection()
            db.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, md5_pass, email),
            )
            db.commit()
            msg = "User created. <a href='/login'>Login</a>"
        except Exception as e:
            msg = f"Error: {e}"

    return render(
        "Register",
        f"""
        <p>{msg}</p>
        <form method='POST'>
            <input name='username' placeholder='Username'>
            <input name='email' placeholder='Email'>
            <input name='password' type='password' placeholder='Password'>
            <button type='submit'>Register</button>
        </form>
        """,
    )


# VULN: IDOR — access other users profiles
@bp.route("/profile")
@bp.route("/profile/<int:user_id>")
def profile(user_id=None):
    if user_id is None:
        if "user_id" not in session:
            return redirect("/login")
        user_id = session["user_id"]

    # VULNERABLE: does not check if the current user has permission
    db = get_db_connection()
    user = db.execute("SELECT * FROM users WHERE id = %s", (user_id,)).fetchone()

    if user:
        return render(
            f"Account Overview: {user['username']}",
            f"""
            <div class='card'>
                <p><b>Account ID:</b> {user['id']}</p>
                <p><b>Client Name:</b> {user['username']}</p>
                <p><b>Contact Email:</b> {user['email']}</p>
                <p><b>Account Type:</b> {user['role']}</p>
                <p><b>Private Notes:</b> {user['secret_note']}</p>
            </div>
            """,
        )
    return "User not found", 404
