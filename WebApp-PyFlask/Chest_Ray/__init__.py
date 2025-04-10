import os
import sqlite3
import smtplib
from datetime import date
from flask import Flask, render_template, request, session, redirect
from email.message import EmailMessage



"""

All the code below for making this thing work :D
Will add better explanation later

-Taha

"""


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
        # if "username" in session:
        #     return redirect("dashboard") 
        
        return render_template("index.html")
    
    @app.route("/login")
    def login():
        if "username" in session and session["userType"] == "patient":
            return redirect("/dashboard")
        elif "username" in session and session["userType"] == "admin" or "username" in session and session["userType"] == "director" or "username" in session and session["userType"] == "clinician":
            return redirect("/ClinicianDashboard")
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

            if usertype == "admin" or usertype == "director" or usertype == "clinician":
                cur.execute("SELECT * FROM users WHERE user_name = ? AND password = ?;", (username, password))
            elif usertype == "patient":
                cur.execute("SELECT * FROM patients WHERE patient_name = ? AND patient_password = ?;", (username, password))
            else:
                return "404" #Make better

            user = cur.fetchone()

            if user and usertype == "admin" or user and usertype == "director" or user and usertype == "clinician":
            
                UpdatedType = user["user_role"]
                print(UpdatedType)
                session["username"] = user["user_name"]
                session["userType"] = UpdatedType

    

                cur.execute("select user_id from users where user_name = ?", (username,))
                id = cur.fetchone()
                session["ID"] = id["user_id"]

                #print("DONE")  #DEBUGGING
                #print(session)

                return redirect("/ClinicianDashboard")
            
            elif user and usertype == "patient":
                session["username"] = user["patient_name"]
                session["userType"] = usertype
                #print(session["username"])
                #print(session["userType"])
                return redirect("dashboard")


            else:
                #print(request.form)
                return "Invaild Login"

        except Exception as error:
            print(f"Error: {error}")
            return "404, can not reach database :C"
        

        finally:
            connection.close()
        


    @app.route("/dashboard")
    def dashboard():
        if "username" in session:

            try:
                connection = sqlite3.connect("CHESTRAYG6.db")
                connection.row_factory = sqlite3.Row
                cur = connection.cursor()

                if "username" in session and session["userType"] == "patient":
                    username = session["username"]

                    cur.execute("select * from patients where patient_name = ?", (username,)) #bro
                    Patientrow = cur.fetchone()
                    PatientID = Patientrow["patient_id"]

                    cur.execute("select doctor_user_id from patients where patient_name = ?", (username,))
                    docID = cur.fetchone()

                    ID = docID["doctor_user_id"]
                    #for debugging
                    #print(PatientID)
                    #print(username)
                    #print(ID)

                    if docID:
                        #Get the doc info if he has one (always should anyways) but still check :/
                        cur.execute("select * from users where user_id = ?", (ID,))
                        Doctorrow = cur.fetchone()

                        cur.execute("select * from chestrayimages where patient_id = ?", (PatientID,))
                        xraysend = cur.fetchone()

                        if xraysend:

                            print(xraysend["ai_generated_diagnosis"])

                            #checks because db coding is werid
                            if xraysend:
                                boolSend = xraysend["ai_generated_diagnosis"]
                            if boolSend == 1:
                                boolSend = True
                            elif boolSend == 0:
                                boolSend = False

                            return render_template("dashboard.html", Patientrow = Patientrow, Doctorrow = Doctorrow, xraysend = xraysend, boolSend = boolSend)
                        return render_template("dashboard.html", Patientrow = Patientrow, Doctorrow = Doctorrow)
                    
                    else:
                        '''
                        Everyone HAS a doctor. This case is impossible.
                        However, if in the furture a Patient can make an account without the doctor is required,
                        this code block will be edited.
                        '''

                        Doctorrow = ""
                        return render_template("dashboard.html", Patientrow = Patientrow, Doctorrow = Doctorrow)
                

                elif "username" in session and session["userType"] == "admin" and session["PatientID"] or "username" in session and session["userType"] == "director" and session["PatientID"] or "username" in session and session["userType"] == "clinician" and session["PatientID"]:

                    """
                    Either make it so the HTTP web page for the ClinicianDashboard sends back the name of the Patient selected,
                    then make a new session["PatientID"],
                    then load all that into the dashboard again code here, to see it all.
                    """

                    username = session["PatientID"] #for now ID stores name, WILL CHANGE LATER if I have time
                    doctorID = session["ID"]

                    cur.execute("select * from patients where patient_name = ?", (username,))
                    Patientrow = cur.fetchone()
                    PatientID = Patientrow["patient_id"]

                    cur.execute("select * from users where user_id = ?", (doctorID,))
                    Doctorrow = cur.fetchone()

                    #print(doctorID)
                    #print(PatientID)

                    cur.execute("select * from chestrayimages where patient_id = ?", (PatientID,))
                    xraysend = cur.fetchone()


                    if xraysend:
                        #checks because db coding is werid
                        #print(xraysend["ai_generated_diagnosis"])

                        if xraysend:
                            boolSend = xraysend["ai_generated_diagnosis"]
                        if boolSend == 1:
                            boolSend = True
                        elif boolSend == 0:
                            boolSend = False

                        
                        if session["userType"] == "clinician":
                            clinician = "True"
                        else:
                            clinician = "False"

                        return render_template("dashboard.html", Patientrow = Patientrow, Doctorrow = Doctorrow, xraysend = xraysend, boolSend = boolSend, clinician = clinician)             
                    return render_template("dashboard.html", Patientrow = Patientrow, Doctorrow = Doctorrow)

                else:
                    return redirect("/ClinicianDashboard")

            
            except Exception as error:
                print(f"Error: {error}")

                if "username" in session and session["userType"] == "patient":
                    return "404, can not reach database :C"
                elif "username" in session and session["userType"] == "admin" or "username" in session and session["userType"] == "director" or "username" in session and session["userType"] == "clinician":
                    print("Did not select patient")
                    return redirect("/ClinicianDashboard")

            finally:
                connection.close()


        return render_template("Login.html")

    
    @app.route("/reviewed", methods = ['POST'])
    def reviewed():

        connection = sqlite3.connect("CHESTRAYG6.db")
        connection.row_factory = sqlite3.Row


        username = session["PatientID"]
        cur = connection.cursor()
        cur.execute("select * from patients where patient_name = ?", (username,))
        Patientrow = cur.fetchone()
        PatientID = Patientrow["patient_id"]


        if "username" in session and session["userType"] == "clinician" and session["PatientID"]:

            try: 

                PatientID = session["PatientID"]
                username = session["username"]


                #print(PatientID)
                #print(username)

                Diagnosis = request.form.get("Diagnosis")
                OverrideDescription = request.form.get("OverrideDescription")
                    
                cur.execute("update patients set reviewed = ? where patient_name = ?", ("Yes", PatientID,))


                print(PatientID)

                cur.execute("update chestrayimages set Description = ? where patient_id = ?", (OverrideDescription, PatientID,)) #OverrideDescription

                cur.execute("select * from chestrayimages where patient_id = ?", (PatientID,))
                xraysend = cur.fetchone()

                # print(xraysend)

                # cur.execute("select * from patients where patient_id = ?", (PatientID,))
                # emailfectch = cur.fetchone()

                # print(emailfectch)

                cur.execute("select * from users where user_name = ?", (username,))
                emailfectchdoctor = cur.fetchone()


                # emailDoc = emailfectchdoctor["email_address"]
                # email = emailfectch["email_ID"]
                # Patientaname = session["PatientID"]
                # Doctorsname = emailfectchdoctor["Full_Name"]

                # from_mail = "G6ChestRay@gmail.com"
                # password_email = "kasdM29I1Io@ds!!@)(*uNSADS"
                # smtp_server = "smtp.gmail.com"
                # smtp_port = 587

                # message = EmailMessage()
                # message["Subject"] = subject
                # message["From"] = from_mail
                # message["To"] = email
                # message.set_content(body)
                
                # messageDoc = EmailMessage()
                # messageDoc["Subject"] = subject
                # messageDoc["From"] = from_mail
                # messageDoc["To"] = emailDoc
                # messageDoc.set_content(body)

                # emailserver = smtplib.SMTP(smtp_server, smtp_port)
                # emailserver.starttls()
                # emailserver.login(from_mail, password_email)

                # emailserver.send_message(from_mail, email, message)
                # emailserver.send_message(from_mail, emailDoc, messageDoc)


                if Diagnosis == "yes":
                    if xraysend:
                        cur.execute("update chestrayimages set ai_generated_diagnosis = ? where patient_id = ?", (1, PatientID,)) #OverrideDiagnosis has

                elif Diagnosis == "no":
                    if xraysend:
                        cur.execute("update chestrayimages set ai_generated_diagnosis = ? where patient_id = ?", (0, PatientID,)) #OverrideDiagnosis has

                return redirect("/ClinicianDashboard")

            except Exception as error:
                print(f"Error: {error}")

            finally:
                connection.commit()
                connection.close()
        
        return "Did not choose diagnosis"


    @app.route("/PatientSelected", methods = ['POST'])
    def PatientSelected():
        if "username" in session and session["userType"] == "admin" or "username" in session and session["userType"] == "director" or "username" in session and session["userType"] == "clinician":
            PatientID = request.form.get("PatientID") #later can be changed to patient ID, but the way the databse works rn using name
            if PatientID:
                session["PatientID"] = PatientID 
                print(PatientID)
                return redirect("/dashboard")
            else:
                #return "You have not chosen an Patient to view from."
                return redirect("/ClinicianDashboard")


    @app.route("/createAccPatient")
    def createAccPatient():
        if "username" in session and session["userType"] == "admin"  or "username" in session and session["userType"] == "director":
            return render_template("createAccPatient.html")
        else:
            return redirect("/dashboard")
    

    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/AccountCreation", methods = ("POST",))
    def AccountCreation():

        try:


            if "username" in session and session["userType"] == "admin"  or "username" in session and session["userType"] == "director":

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
                            doctor_user_id,
                            email_ID
                            ) VALUES (?, ?, ?, ? , ?, ?, ?, ?)
                    """, (name, password, dob, gender, "", tel, Id, email)
                            )

                connection.commit()

                return redirect("/dashboard")

            return "You are not an admin!"

        except Exception as error:
            print(f"Error: {error}")
            return "404, can not reach database :C"
        
        finally:
            connection.close()




    @app.route("/ClinicianDashboard")
    def ClinicianDashboard():
        
        try:
            connection = sqlite3.connect("CHESTRAYG6.db")
            connection.row_factory = sqlite3.Row
            cur = connection.cursor()


            if "username" in session and session["userType"] == "admin":

                Id = session["ID"]
                cur.execute("select * from patients where doctor_user_id = ?", (Id,))
                rows = cur.fetchall()
                return render_template("ClinicianDashboard.html", rows = rows)


            elif "username" in session and session["userType"] == "director" or "username" in session and session["userType"] == "clinician":

                cur.execute("select * from patients")
                rows = cur.fetchall()
                return render_template("ClinicianDashboard.html", rows = rows)
            

            else:
                return redirect("/")

        except Exception as error:
            print(f"Error: {error}")
            return "404, can not reach database :C"
        

        finally:
            connection.close()





    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")


    @app.route("/xrayAI", methods = ["POST"])
    def xrayAI():
        import os

        if "xray" not in request.files:
            return redirect("/dashboard")

        import numpy as np
        import matplotlib.pyplot as plt
        import tensorflow as tf
        import cv2
        from tensorflow import keras
        from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
        import io
        from PIL import Image

        file = request.files["xray"]
        filename = file.filename #can be the ID of the file
        print(filename)
        #upload_dir = os.path.join("static", "uploads")
        #os.makedirs(upload_dir, exist_ok=True)
        path = os.path.join("Chest_Ray/static/uploads", filename)
        file.save(path)

        model = keras.models.load_model("model.keras")

        #img = Image.open(path)

        imgNp = np.array([cv2.imread(path)])

        #imgNp = np.array(imgPredict) / 255.0 #shape
        #imgNp = np.expand_dims(imgNp, axis=0)  #shape

        # imgPredict = Image.open(io.BytesIO(file_bytes)).convert("RGB") #greyscale it maybe
        # imgPredict = imgPredict.resize((250, 250))
        


        
        model.predict(imgNp)
        probabilities = tf.nn.softmax(model.predict(imgNp))
        predicted_class = np.argmax(model.predict(imgNp), axis=-1)[0]
        print(probabilities)
        print(predicted_class)

        if predicted_class == 1:
            Pneumonia = True
        else:
            Pneumonia = False
        
        print(Pneumonia)


        """
        
        COPY OF /DASHBOARD FIT FOR XRAY TO LOAD THE DETAILS AGAIN
        Why - Taha :}
        
        """


        if "username" in session:

            try:
                connection = sqlite3.connect("CHESTRAYG6.db")
                connection.row_factory = sqlite3.Row
                cur = connection.cursor()

                if "username" in session and session["userType"] == "patient":
                    username = session["username"]

                    cur.execute("select * from patients where patient_name = ?", (username,)) #bro
                    Patientrow = cur.fetchone()

                    cur.execute("select doctor_user_id from patients where patient_name = ?", (username,))
                    docID = cur.fetchone()

                    ID = docID["doctor_user_id"]
                    #for debugging
                    #print(username)
                    #print(ID)

                    if docID:
                        #Get the doc info if he has one (always should anyways) but still check :/
                        cur.execute("select * from users where user_id = ?", (ID,))
                        Doctorrow = cur.fetchone()
                        return render_template("dashboard.html", Patientrow = Patientrow, Doctorrow = Doctorrow)
                    
                    else:
                        '''
                        Everyone HAS a doctor. This case is impossible.
                        However, if in the furture a Patient can make an account without the doctor is required,
                        this code block will be edited.
                        '''

                        Doctorrow = ""
                        return render_template("dashboard.html", Patientrow = Patientrow, Doctorrow = Doctorrow, filename = filename, Pneumonia = Pneumonia)
                

                elif "username" in session and session["userType"] == "admin" and session["PatientID"] or "username" in session and session["userType"] == "director" and session["PatientID"] or "username" in session and session["userType"] == "clinician" and session["PatientID"]:

                    """
                    Either make it so the HTTP web page for the ClinicianDashboard sends back the name of the Patient selected,
                    then make a new session["PatientID"],
                    then load all that into the dashboard again code here, to see it all.
                    """

                    username = session["PatientID"] #for now ID stores name, WILL CHANGE LATER if I have time
                    doctorID = session["ID"]

                    cur.execute("select * from patients where patient_name = ?", (username,))
                    Patientrow = cur.fetchone()

                    cur.execute("select * from users where user_id = ?", (doctorID,))
                    Doctorrow = cur.fetchone()

                    cur.execute("select patient_id from patients where patient_name = ?", (username,))
                    idForPat = cur.fetchone()
                    realID = idForPat["patient_id"]

                    #save xray to db :{

                    thedate = date.today()

                    cur.execute("""
                    insert into chestrayimages (patient_id, user_id, FILE_PATH, upload_date, ai_generated_diagnosis, Description)
                    values (?, ?, ?, ?, ?, ?)
                    """, (realID, doctorID, filename, thedate, Pneumonia, ""))
                    connection.commit()


                    return render_template("dashboard.html", Patientrow = Patientrow, Doctorrow = Doctorrow, filename = filename, Pneumonia = Pneumonia)              

                else:
                    return redirect("/ClinicianDashboard")

            
            except Exception as error:
                print(f"Error: {error}")

                if "username" in session and session["userType"] == "patient":
                    return "404, can not reach database :C"
                elif "username" in session and session["userType"] == "admin" or "username" in session and session["userType"] == "director" or "username" in session and session["userType"] == "clinician":
                    print("Did not select patient")
                    return redirect("/ClinicianDashboard")

            finally:
                connection.close()


    return app

app = create_app()