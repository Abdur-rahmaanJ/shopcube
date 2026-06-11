def test_index(client):
    response = client.get('/vendor/')
    assert response.status_code == 200
