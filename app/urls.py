from app.views import Groups, Students, StudentsCourses
# from app.views import Groups

def add_urls(api):
    api.add_resource(Groups, '/groups')
    api.add_resource(Students, '/students', '/students/<student_id>')
    api.add_resource(StudentsCourses, '/students/<student_id>/courses/<course_id>')

