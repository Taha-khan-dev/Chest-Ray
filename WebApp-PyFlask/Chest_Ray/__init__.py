import os
import sqlite3
from flask import Flask, render_template, request, session, redirect


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
        if "user" in session:
            return redirect("dashboard") 
        
        return redirect("login")
    
    @app.route("/login")
    def login():
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

                return redirect("dashboard")
            
            elif user and usertype == "patient":
                session["username"] = user["patient_name"]
                session["userType"] = usertype

                connection.close()

                return redirect("dashboard")


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
            return f"Welcome, {session['username']}! You are now logged in."
        return render_template("Login.html")


    @app.route("/createAccPatient")
    def createAccPatient():
        return render_template("createAccPatient.html")
    

    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/AccountCreation", methods = ("POST",))
    def AccountCreation():

        try:
            connection = sqlite3.connect("CHESTRAYG6.db")
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()

            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            email = request.form.get("email")
            tel = request.form.get("tel")
            password = request.form.get("password")
            dob = request.form.get("DOB")
            gender = request.form.get("gender")

            name = first_name + " " + last_name

            #medical_history should be added into account settings

            cur.execute("""
                insert into patients (
                        patient_name,
                        patient_password,
                        DOB,
                        gender,
                        medical_history,
                        phone_number
                        ) VALUES (?, ?, ?, ? , ?, ?)
                """, (name, password, dob, gender, "", tel)
                        )

            connection.commit()
            connection.close()

            return redirect("/dashboard")

        except Exception as error:
            print(f"Error: {error}")
            return "404, can not reach database :C"


    return app

app = create_app()