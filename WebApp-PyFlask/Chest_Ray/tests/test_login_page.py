def test_loin_page (client):
    response = client.get("/login")

    assert form_tag() in response.text
    assert AdminuserType() in response.text
    assert PatientuserType() in response.text


def test_doctor_login_pass(client):
    response = client.post("/check_login", data ={
        "username": "abdullah_malik",
        "password": "password123",
        "userType": "admin"
    }, follow_redirects=False)

    #302 means that the page has been moved and check the name of page
    assert response.status_code == 302
    assert "ClinicianDashboard" in response.headers["Location"]

def test_patient_login_pass(client):
    response = client.post("/check_login", data ={
        "username": "Momin Naveed",
        "password": "momin123",
        "userType": "patient"
    }, follow_redirects=False)

    #302 means that the page has been moved and check the name of page
    assert response.status_code == 302
    assert "dashboard" in response.headers["Location"]


def test_doctor_login_fail(client):
    response = client.post("/check_login", data ={
        "username": "taha_inayat",
        "password": "WWRONGPASSWORD",
        "userType": "admin"
    }, follow_redirects=False)

    assert "Invaild Login" in response.text

def test_patient_login_fail(client):
    response = client.post("/check_login", data ={
        "username": "Momin WRONGG",
        "password": "momin123",
        "userType": "patient"
    }, follow_redirects=False)

    assert "Invaild Login" in response.text




def form_tag():
    return '<form id="loginForm" action = "/check_login" method="POST" onsubmit="return validateForm();">'

def AdminuserType():
    return 'id="adminFields"'

def PatientuserType():
    return 'id="patientFields"'
