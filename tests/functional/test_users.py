from cvreviewer import bcrypt


def test_new_user(new_user):
    assert new_user.email == 'newtestuser46@gmail.com'
    assert bcrypt.check_password_hash(new_user.password, 'FlaskIsAwesome86!')


def test_valid_login_logout(test_client, init_database):
    response = test_client.post('/login',
                                data=dict(email='newtestuser46@gmail.com',
                                passw='FlaskIsAwesome86!'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'About the author & Contacts' in response.data
    assert b'Wrong email/password!' not in response.data

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'About the author & Contacts' in response.data
