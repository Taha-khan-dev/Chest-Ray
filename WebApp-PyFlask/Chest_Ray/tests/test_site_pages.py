def test_index(client):
    response = client.get("/")
    assert response.status_code == 200

def test_loin_page(client):
    response = client.get("/login")
    assert response.status_code == 200

# def test_dashboard(client):
#     response = client.get("/dashboard")
#     assert response.status_code == 302
