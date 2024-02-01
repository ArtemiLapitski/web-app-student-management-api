# import pytest
#
# from core.app import app, db, User
#
#
# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     client = app.test_client()
#
#     with app.app_context():
#         db.create_all()
#
#     yield client
#
#     with app.app_context():
#         db.session.remove()
#         db.drop_all()
#
#
# @pytest.fixture
# def session():
#     with app.app_context():
#         db.create_all()
#
#     yield db.session
#
#     with app.app_context():
#         db.session.remove()
#         db.drop_all()
#
#
# @pytest.fixture
# def user_fixture(session):
#     with app.app_context():
#         # Create a sample user for testing
#         user = User(username='test_user', email='test@example.com')
#
#         # Add the user to the session and commit
#         session.add(user)
#         session.commit()
#
#         # Refresh the user to avoid DetachedInstanceError
#         session.refresh(user)
#
#     return user
#
#
# def test_user_resource(client, session):
#     response = client.post('/users', json={'username': 'test_user', 'email': 'test@example.com'})
#     assert response.status_code == 201
#
#     response = client.get('/users/1')
#     assert response.status_code == 200
#     assert response.json == {'username': 'test_user', 'email': 'test@example.com'}
#
# def test_get_user(client, user_fixture):
#     response = client.get(f'/users/{user_fixture.id}')
#     print(response.json)
#     assert response.json == {'username': user_fixture.username, 'email': user_fixture.email}
#
# # Add more test cases as needed
#
# if __name__ == '__main__':
#     pytest.main(['-v', 'tests/test_app.py'])
from sqlalchemy import URL
from config import DB_SUPERUSER_PASSWORD, DB_SUPERUSER_USERNAME, DB_HOST, DB_PORT

superuser_url = URL.create(
    "postgresql",
    username=DB_SUPERUSER_USERNAME,
    password=DB_SUPERUSER_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

print(superuser_url)