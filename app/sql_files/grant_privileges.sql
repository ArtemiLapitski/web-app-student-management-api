CREATE ROLE students_admin;

GRANT students_admin TO supervisor;

GRANT ALL ON SCHEMA public TO students_admin