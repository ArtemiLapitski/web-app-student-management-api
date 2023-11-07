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


drop table courses_students_model;
drop table groups_model CASCADE;
drop table students_model CASCADE;
drop table courses_model;



INSERT INTO groups_model (group_name) VALUES ('EE-08');
INSERT INTO students_model (group_id, first_name, last_name) VALUES (1, 'Albert', 'Einstein');
INSERT INTO courses_model (course_name) VALUES ('math');
INSERT INTO courses_model (course_name) VALUES ('science');

INSERT INTO courses_students_model (student_id,course_id) VALUES (1,1);
INSERT INTO courses_students_model (student_id,course_id) VALUES (1,2);


SELECT * FROM public.student_groups;
SELECT * FROM public.students;
SELECT * FROM public.courses;
SELECT * FROM public.courses_students
