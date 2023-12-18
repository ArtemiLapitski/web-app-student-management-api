FROM python:3.9

COPY app/database/setup.py app/database/create_tables.sql app/database/
COPY app/generate_test_data.py  app/
COPY setup_db.py /

RUN pip install sqlalchemy psycopg2-binary

CMD [ "python", "setup_db.py" ]