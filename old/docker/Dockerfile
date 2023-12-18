FROM python:3.9

COPY docker/database.py docker/generate_test_data.py docker/__init__.py docker/create_tables.sql docker/
COPY docker/setup.py /
RUN pip install sqlalchemy psycopg2-binary

#CMD [ "python", "./main.py" ]
CMD [ "python", "setup.py" ]