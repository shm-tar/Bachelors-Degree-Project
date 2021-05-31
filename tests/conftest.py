import pytest
from cvreviewer import create_app, bcrypt, db
from cvreviewer.models import User, ProcessedFile
from test_config import TestConfig
# python3 -m pytest


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig)

    # Flask provides a way to test your application by exposing
    # the Werkzeug test Client and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def new_user():
    hashed_passw = bcrypt.generate_password_hash('FlaskIsAwesome86!').decode('utf-8')
    user = User(email='newtestuser46@gmail.com', password=hashed_passw)
    return user


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    hashed_passw1 = bcrypt.generate_password_hash('FlaskIsAwesome86!').decode('utf-8')
    user1 = User(email='newtestuser46@gmail.com', password=hashed_passw1)

    hashed_passw2 = bcrypt.generate_password_hash('Password47').decode('utf-8')
    user2 = User(email='kennedyfamilyrecipes@gmail.com', password=hashed_passw2)

    db.session.add(user1)
    db.session.add(user2)

    first_post = ProcessedFile(title='First Anonymous CV', content="First Test Content",
                         entity_content="<p>first test</p>", user_id=1)
    second_post = ProcessedFile(title='Second Anonymous CV', content="Second Test Content",
                         entity_content="<p>Second test</p>", user_id=2)

    db.session.add(first_post)
    db.session.add(second_post)

    # Commit the changes for the users & posts
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope='module')
def new_post():
    post = ProcessedFile(title='Anonymous CV', content="Test Content",
                         entity_content="<p>test</p>", user_id=2)
    return post


@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app
