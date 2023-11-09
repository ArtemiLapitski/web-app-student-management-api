from app import GroupsPerStudentCount


def add_urls(api):
    api.add_resource(GroupsPerStudentCount, '/groups')
