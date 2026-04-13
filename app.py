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
    error = None

    if request.method == "POST":
        print("POST WORKING")
        
        
        file = request.files.get("file")

        if file and file.filename != "":
            try:
                df = pd.read_csv(file)

                # DEBUG (optional)
                print(df.head())

                # Check columns exist
                if "people_count" not in df.columns or "noise_level" not in df.columns:
                    return "Error: CSV must contain 'people_count' and 'noise_level' columns"

                # Calculate values
                people = df["people_count"].mean()
                noise = df["noise_level"].mean()

                # Prediction
                result = model.predict([[people, noise]])
                prediction = int(result[0])

            except Exception as e:
                error = str(e)
        else:
            error = "No file selected"

    return render_template("dashboard.html", prediction=prediction, error=error)



# LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# RUN APP
if __name__ == "__main__":
    app.run(debug=True)