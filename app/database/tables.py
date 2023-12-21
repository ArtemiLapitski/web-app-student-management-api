from sqlalchemy import MetaData, create_engine, URL
from sqlalchemy.orm import sessionmaker
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT


user_db_url = URL.create(
    "postgresql",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(user_db_url)
#
#
# Session = sessionmaker(engine)
# session = Session()
#
#
# metadata_obj = MetaData()
# metadata_obj.reflect(bind=engine)
#
#
# course_table = metadata_obj.tables["course"]
# student_table = metadata_obj.tables["student"]
# student_group_table = metadata_obj.tables["student_group"]
# course_student_table = metadata_obj.tables["course_student"]