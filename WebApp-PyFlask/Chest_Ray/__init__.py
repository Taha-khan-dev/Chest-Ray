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


    app.secret_key = "keyy" #dont change later on otherwise sessions will be reset



    @app.route("/")
    def index():
        if "username" in session:
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
    

                cur.execute("select user_id from users where user_name = ?", (username,))
                id = cur.fetchone()
                session["ID"] = id["user_id"]

                #print("DONE")  #DEBUGGING
                print(session)

                return redirect("dashboard")
            
            elif user and usertype == "patient":
                session["username"] = user["patient_name"]
                session["userType"] = usertype

                return redirect("dashboard")


            else:
                print(request.form)
                return "Invaild Login"

        except Exception as error:
            print(f"Error: {error}")
            return "404, can not reach database :C"
        

        finally:
            connection.close()
        


    @app.route("/dashboard")
    def dashboard():
        if "username" in session:
            return f"Welcome, {session["username"]}! You are now logged in."
        return render_template("Login.html")


    @app.route("/createAccPatient")
    def createAccPatient():
        if "username" in session and session["userType"] == "admin":
            return render_template("createAccPatient.html")
        else:
            return redirect("dashboard")
    

    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/AccountCreation", methods = ("POST",))
    def AccountCreation():

        try:


            if "username" in session and session["userType"] == "admin":

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
                Id = session["ID"]

                name = first_name + " " + last_name

                #medical_history should be added into account settings

                cur.execute("""
                    insert into patients (
                            patient_name,
                            patient_password,
                            DOB,
                            gender,
                            medical_history,
                            phone_number,
                            doctor_user_id
                            ) VALUES (?, ?, ?, ? , ?, ?, ?)
                    """, (name, password, dob, gender, "", tel, Id)
                            )

                connection.commit()

                return redirect("/dashboard")

            return "You are not an admin!"

        except Exception as error:
            print(f"Error: {error}")
            return "404, can not reach database :C"
        
        finally:
            connection.close()




    @app.route("/ClinicianDashbaord")
    def ClinicianDashbaord():
        
        try:


            connection = sqlite3.connect("CHESTRAYG6.db")
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()


            if "username" in session and session["userType"] == "admin":

                Id = session["ID"]

                cur.execute("select * from patients where doctor_user_id = ?", (Id))
                rows = cur.fetchall()
                render_template("ClinicianDashbaord.html", rows = rows)


            elif "username" in session and session["userType"] == "director":

                cur.execute("select * from patients")
                rows = cur.fetchall()

        except Exception as error:
            print(f"Error: {error}")
            return "404, can not reach database :C"

        

        finally:
            connection.close()



    return app

app = create_app()