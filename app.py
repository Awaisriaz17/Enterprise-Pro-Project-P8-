from flask import Flask, render_template, request, redirect, session
import pandas as pd
import pickle
print("APP RUNNING NEW CODE")
app = Flask(__name__)
app.secret_key = "secret123"

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Login data
users = {"admin": "1234"}


# LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/dashboard")   # ✅ IMPORTANT
        else:
            return "Invalid Login"

    return render_template("login.html")



# DASHBOARD PAGE
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    prediction = None

    if request.method == "POST":
        file = request.files["file"]

        if file:
            df = pd.read_csv(file)

            people = df["people_count"].mean()
            noise = df["noise_level"].mean()

            result = model.predict([[people, noise]])
            prediction = int(result[0])

    return render_template("dashboard.html", prediction=prediction)


# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# RUN APP
if __name__ == "__main__":
    app.run(debug=True)