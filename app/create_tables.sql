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
