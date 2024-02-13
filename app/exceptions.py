class StudentIdNotFound(Exception):
    def __init__(self, student_id):
        super().__init__(f"Student under id '{student_id}' does not exist.")
        # self.driver = driver
