# Enterprise-Pro-Project-P8-
from flask import Blueprint, render_template, request, redirect, session

# Create Blueprint
auth = Blueprint("auth", __name__)

# Dummy users (you can later replace with database)
users = {
    "admin": "1234",
    "user": "pass"
}

# Login route
@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "❌ Invalid username or password"

    return render_template("login.html")


# Logout route
@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")