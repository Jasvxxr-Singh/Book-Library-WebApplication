import pytest
from flask import session

def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code

    response = client.post(
        '/authentication/register',
        data={'user_name': 'jaden', 'password': 'jadenisCute420'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):

    response = client.post(
        '/authentication/register',
        data={'user_name': username, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    # response = auth.login()
    # assert response.headers['Location'] == 'http://localhost/authentication/login'

    # Check that a session has been created for the logged-in user.
    # with client:
    #     client.get('/')
    #     assert session['user_name'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200

def test_get_books(client):
    response = client.get('browsing/books/1')
    assert response.status_code == 200


def test_login_required_to_comment(client):
    response = client.get('browsing/books/1/reviews')
    assert response.headers['Location'] == 'http://localhost/authentication/login'

@pytest.mark.parametrize(('review', 'messages'), (
        ('This shit dogwater', (b'Your comment must not contain profanity')),
        ('ass', b'Your comment must not contain profanity'),
))
def test_review_with_invalid_test(client, auth, review, messages):
    auth.login()
    response = client.post('http://localhost/browsing/books/1/reviews', data={"review": review})

    for message in messages:
        assert message in response.data