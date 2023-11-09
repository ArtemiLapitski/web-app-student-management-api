from pydantic import BaseModel, field_validator
# from .schemas_validation import students_count_validation


class StudentCountToValidate(BaseModel):
    students: int

    # validate_student_count = field_validator('students')(students_count_validation)

# result = StudentCountToValidate(students='10')
# StudentCountToValidate()
