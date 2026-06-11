def test_index(client):
    response = client.get('/purchase/')
    assert response.status_code == 200
