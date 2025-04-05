import os
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for


def create_app(test_config=None):

    """Create and configure the app."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #Web Pages go below.


    app.secret_key = "keyy"

    @app.route("/")
    def index():
        return render_template("login.html")
    

    @app.route("/check_login", methods = ("POST",))
    def check_login():

        try:
            connection = sqlite3.connect("CHESTRAYG6.db")
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()


            username = request.form.get("username")
            password = request.form.get("password")
            usertype = request.form.get("userType")

            if usertype == "admin":
                cur.execute("SELECT * FROM users WHERE user_name = ? AND password = ?;", (username, password))
            elif usertype == "patient":
                cur.execute("SELECT * FROM patients WHERE patient_name = ? AND patient_password = ?;", (username, password))
            else:
                return "404" #Make better

            user = cur.fetchone()

            if user and usertype == "admin":
                session["username"] = user["user_name"]
                session["userType"] = usertype
                
                connection.close()

                return render_template("dashboard.html")
            
            elif user and usertype == "patient":
                session["username"] = user["patient_name"]
                session["userType"] = usertype

                connection.close()

                return render_template("dashboard.html")


            else:
                connection.close()
                print(request.form)
                return "Invaild Login"

        except Exception as error:
            print(f"Error: {error}")
            return "404, can not reach database :C"
        


    @app.route("/dashboard")
    def dashboard():
        if "user" in session:
            return f"Welcome, {session['user']}! You are now logged in."
        return render_template("Login.html")


    return app

app = create_app()