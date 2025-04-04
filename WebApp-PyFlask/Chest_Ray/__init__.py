import os
import sqlite3
from flask import Flask, render_template, request, session


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
        return render_template("Login.html")
    

    @app.route("/check_login", methods = ("POST",))
    def check_login():

        try:

            connection = sqlite3.connect("CHESTRAYG6.db")
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()

            username = request.form.get("username")
            password = request.form.get("password")

            cur.execute("SELECT * FROM users WHERE user_name = ? AND password = ?;", (username, password))
            user = cur.fetchone()

            connection.close()

            if user:
                session["user"] = user["user_name"]
                session["user"] = user["user_role"]
                
                return render_template("index.html")
            
            else:
                return request.form

        except:
            return "404, can not reach database :C"
        







    @app.route("/dashboard")
    def dashboard():
        if "user" in session:
            return f"Welcome, {session['user']}! You are now logged in."
        return render_template("Login.html")


    return app

app = create_app()