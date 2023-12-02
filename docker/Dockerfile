FROM python:3.9

COPY main.py create_tables.sql ./

RUN pip install sqlalchemy psycopg2-binary

CMD [ "python", "./main.py" ]
