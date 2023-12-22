Web framework: Flask restful api

Clone a project and move to it:

$ git clone https://git.foxminded.ua/foxstudent103535/task10_sql.git

$ cd task10_sql

Create a virtualenv or skip this point.
Activate virtualenv.

Install the requirements:
$ pip install -r requirements.txt

Create the file .env with virtual environments (see in .env.example)

Run docker:

docker build -t task10_sql .

docker run --env-file .env task10_sql

Run server:

$ set FLASK_APP=main.py

$ flask run

Urls: http://127.0.0.1:5000
