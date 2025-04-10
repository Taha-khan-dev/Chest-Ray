def test_xray_fail(client):
    response = client.post("/xrayAI", data ={
        "xray": "wrongilfe.pdf",
    }, content_type="multipart/form-data", follow_redirects=False)

    assert response.status_code == 302
    assert "dashboard" in response.headers["Location"]