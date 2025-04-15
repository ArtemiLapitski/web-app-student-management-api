## Student Management API

Flask-based API service for managing students, courses, and groups.
Supports full CRUD operations using SQLAlchemy and PostgreSQL.
Includes automated testing with pytest and Docker-based database setup.


## Test Data:

On setup, the application automatically generates and inserts test data into the database:

- **200 students**, **10 groups**, and **10 courses** are randomly generated.
- Each student is randomly assigned to **1–3 courses**.
- Each group is assigned **10–30 students**.
- Some students may not belong to any group.
- Some groups may have no students assigned.


## Prerequisites:
Python 3.11

git

docker

PostgreSQL


## Installation

Clone the project using git clone command

Move to project directory

Create a virtualenv or skip this point.

Activate virtualenv.

Install the requirements:
```
pip install -r requirements.txt
```

Create .env file with your database configurations.  Use .env.example file as example.

Make sure you have docker installed. Run docker daemon.

Build docker image:
```
docker build -t students-app .
```

Run docker image to create database and data:
```
docker run --env-file .env students-app
```

To run server:

```
python main.py
```

Urls: http://127.0.0.1:5000


## Usage:

Examples of the allowed API requests are presented below.

- Get groups which contain less than or equal to amount of students.

GET: http://127.0.0.1:5000/groups?student_count_lte=15

Example response:
```
[
    "SK-11",
    "BW-86",
    "SI-60",
    "YU-31"
]
```

- Find all students related to the course with the given name.

GET: http://127.0.0.1:5000/students?course=Art

Example response:
```
[
    "Essence Lowe",
    "Shyann Fletcher",
    "Brenna Armstrong",
    "Jackson Rush",
    "Raphael Best"
]
```

- Add new student.

PUT: http://127.0.0.1:5000/students

Body of the request:
```
{"first_name": "George", "last_name": "Washington", "courses": ["Art", "Science", "Physics"]}
```

Example response (group will be null if not specified in request):
```
{
    "student_id": 201,
    "first_name": "George",
    "last_name": "Washington",
    "courses": [
        "Art",
        "Science",
        "Physics"
    ],
    "group": null
}
```

- Delete student by STUDENT_ID.

DELETE: http://127.0.0.1:5000/students/1

Example response:
```
{
    "mssg": "Student under id '1' has been deleted"
}
```

- Add student (STUDENT_ID=2) to the course (COURSE_ID=3).

PUT: http://127.0.0.1:5000/students/2/courses/3

Example response:
```
{
    "student_id": 2,
    "first_name": "Colten",
    "last_name": "Alvarez",
    "courses": [
        "Science",
        "Art",
        "English"
    ],
    "group": null
}
```

- Delete student (STUDENT_ID=2) from course (COURSE_ID=3).

DELETE: http://127.0.0.1:5000/students/2/courses/3

Example response:
```
{
    "mssg": "Course under id '3' has been deleted"
}
```
