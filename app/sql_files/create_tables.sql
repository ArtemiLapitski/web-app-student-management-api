CREATE TABLE student_group (
	group_id serial PRIMARY KEY,
	group_name char(5) UNIQUE NOT NULL
);

CREATE TABLE student (
	student_id serial PRIMARY KEY,
	group_id int,
	first_name varchar(50) NOT NULL,
	last_name varchar(50) NOT NULL,
	FOREIGN KEY(group_id) 
		REFERENCES student_group(group_id)
);

CREATE TABLE course (
	course_id serial PRIMARY KEY,
	course_name varchar(50) UNIQUE NOT NULL,
	description text
);

CREATE TABLE course_student (
	course_id INTEGER REFERENCES course(course_id),
	student_id INTEGER REFERENCES student(student_id) ON DELETE CASCADE,
	PRIMARY KEY(course_id,student_id)
);
