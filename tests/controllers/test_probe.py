def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200

    response = client.post("/ping")
    assert response.status_code == 405
