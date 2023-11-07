from pytest import fixture
from app import database, get_session

@fixture(autouse=True)
def mock_database(mocker):
    mocker.patch.object(database, 'DATABASE_URL', 'sqlite:///:memory:')
    test_db = database.connect_db()
    test_db.create_tables(MODELS)
    return test_db
