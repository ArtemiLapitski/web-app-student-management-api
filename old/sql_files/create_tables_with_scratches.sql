CREATE TABLE student_groups (
	group_id serial PRIMARY KEY,
	group_name char(5) UNIQUE NOT NULL
);

CREATE TABLE students (
	student_id serial PRIMARY KEY,
	group_id int,
	first_name varchar(50) NOT NULL,
	last_name varchar(50) NOT NULL,
	FOREIGN KEY(group_id) 
		REFERENCES student_groups(group_id)
);

CREATE TABLE courses (
	course_id serial PRIMARY KEY,
	course_name varchar(50) UNIQUE NOT NULL,
	description text
);

CREATE TABLE courses_students (
	course_id INTEGER REFERENCES courses(course_id),
	student_id INTEGER REFERENCES students(student_id),
	PRIMARY KEY(course_id,student_id)
);


drop table course_student;
drop table student_group CASCADE;
drop table student CASCADE;
drop table course;



INSERT INTO groups_model (group_name) VALUES ('EE-08');
INSERT INTO students_model (group_id, first_name, last_name) VALUES (1, 'Albert', 'Einstein');
INSERT INTO courses_model (course_name) VALUES ('math');
INSERT INTO courses_model (course_name) VALUES ('science');

INSERT INTO courses_students_model (student_id,course_id) VALUES (1,1);
INSERT INTO courses_students_model (student_id,course_id) VALUES (1,2);


SELECT * FROM public.student_group;
SELECT * FROM public.student;
SELECT * FROM public.course;
SELECT * FROM public.course_student



DROP DATABASE students

CREATE DATABASE testik
    WITH
    OWNER = artemi
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
	



DROP DATABASE test;


CREATE DATABASE students_db;

REVOKE ALL ON DATABASE students_db FROM public;

CREATE ROLE students_supervisor;

CREATE USER supervisor PASSWORD 'supervisor';

GRANT students_supervisor TO supervisor

GRANT CONNECT ON DATABASE students_db TO students_supervisor

-- REVOKE ALL ON DATABASE students_db FROM public;

-- GRANT ALL ON DATABASE students_db TO public;

-- GRANT ALL PRIVILEGES ON DATABASE students_db TO public;

DROP OWNED BY students_admin;

GRANT ALL ON ALL TABLES IN SCHEMA public TO students_admin
GRANT ALL ON SCHEMA public TO students_supervisor
