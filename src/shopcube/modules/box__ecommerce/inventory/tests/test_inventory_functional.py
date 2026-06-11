def test_index(client):
    response = client.get('/inventory/')
    assert response.status_code == 200
