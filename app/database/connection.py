from sqlalchemy import create_engine, URL
from config import (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT, DB_SUPERUSER_USERNAME, DB_SUPERUSER_PASSWORD)
from app.database.setup import get_session


db_url = URL.create(
    "postgresql",
    username=DB_SUPERUSER_USERNAME,
    password=DB_SUPERUSER_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(db_url)

session = get_session(engine)
