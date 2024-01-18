from pydantic import BaseModel, field_validator, model_validator
from .schemas_validation import (student_count_validation, course_name_validation, name_validation,
                                 course_names_validation, group_validation, student_id_validation,
                                 course_id_validation, no_course_for_student_validation,
                                 course_exists_for_student_validation)
from typing import Optional


class StudentCountToValidate(BaseModel):
    student_count_lte: int

    validate_student_count = field_validator('student_count_lte')(student_count_validation)


class CourseNameToValidate(BaseModel):
    course: str

    validate_course_name = field_validator('course')(course_name_validation)


class StudentToCreate(BaseModel):
    first_name: str
    last_name: str
    courses: list
    group: Optional[str] = None

    validate_first_name = field_validator('first_name')(name_validation)
    validate_last_name = field_validator('last_name')(name_validation)
    validate_course_names = field_validator('courses')(course_names_validation)
    validate_group = field_validator('group')(group_validation)


class StudentIdToValidate(BaseModel):
    student_id: int

    validate_student_id = field_validator('student_id')(student_id_validation)


class CourseToAdd(BaseModel):
    student_id: int
    course_id: int

    validate_student_id = field_validator('student_id')(student_id_validation)
    validate_course_id = field_validator('course_id')(course_id_validation)
    validate_no_course_for_student = model_validator(mode='after')(no_course_for_student_validation)


class CourseToDelete(BaseModel):
    student_id: int
    course_id: int

    validate_student_id = field_validator('student_id')(student_id_validation)
    validate_course_id = field_validator('course_id')(course_id_validation)
    validate_course_exists_for_student = model_validator(mode='after')(course_exists_for_student_validation)


