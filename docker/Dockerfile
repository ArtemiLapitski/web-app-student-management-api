FROM python:3.9
WORKDIR /
#COPY main.py database.py generate_test_data.py __init__.py create_tables.sql ./
COPY main.py database.py generate_test_data.py __init__.py create_tables.sql docker/

RUN pip install sqlalchemy psycopg2-binary

#CMD [ "python", "./main.py" ]
CMD [ "python", "docker/main.py" ]