def test_index(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'About the author & Contacts' in response.data


def test_alt_index(test_client):
    response = test_client.get('/index')
    assert response.status_code == 200
    assert b'About the author & Contacts' in response.data


def test_uploadcv(test_client):
    response = test_client.get('/upload_cv')
    assert response.status_code == 302


def test_favicon(test_client):
    response = test_client.get('/favicon.ico')
    assert response.status_code == 200
