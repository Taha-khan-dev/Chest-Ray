# def test_dashboard_redirect(client):
#     response = client.get("/dashboard")
#     assert response.status_code == 302

# def test_dashboard_session_fail(client):
#     with client.session_transaction() as session:
#         session["username"] = "Sara Malik"
#         session["userType"] = "patient"
#         pass

#     response = client.get("/dashboard")
#     assert response.status_code == 200
#     assert "dashboard" in response.headers["Location"]