FROM python:3.9

COPY app/database/setup.py app/database/db.py app/database/models.py app/database/create_tables.sql app/database/
COPY app/generate_data.py  app/
COPY setup_db.py config.py /

RUN pip install sqlalchemy psycopg2-binary python-dotenv flask_sqlalchemy

CMD [ "python", "setup_db.py" ]
