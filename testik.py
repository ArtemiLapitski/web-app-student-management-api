from app.database.models import Base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from config import (DB_HOST, DB_NAME, DB_PORT, DB_SUPERUSER_USERNAME, DB_SUPERUSER_PASSWORD)
from application import add_course

TEST_DB_URL = f'postgresql://{DB_SUPERUSER_USERNAME}:{DB_SUPERUSER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(TEST_DB_URL)
if not database_exists(TEST_DB_URL):
    create_database(engine.url)
Base.metadata.create_all(bind=engine)


connection = engine.connect()
transaction = connection.begin()
test_session = Session(bind=connection)

add_course("math")

test_session.rollback()
connection.close()
