import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY: str = os.environ.get('SECRET_KEY')

DATABASE_URL: str = os.environ.get('DATABASE_URL')

# DATABASE_URL = "sqlite+pysqlite:///:memory:"


COURSES = ['Physical Education', 'Science', 'Art', 'Mathematics', 'English', 'Music', 'Chemistry', 'Algebra', 'Physics',
           'Geography']

NAMES = ['Luca', 'Sasha', 'Amaya', 'Chace', 'Amiah', 'Essence', 'Shyann', 'Jackson', 'Jamar', 'Emanuel', 'Kristin',
         'Brenna', 'Gaige', 'Brianna', 'Quinn', 'Colten', 'Raphael', 'Keyon', 'Kennedi', 'Mackenzie']

SURNAMES = ['Schaefer', 'Sharp', 'Newton', 'Armstrong', 'Reynolds', 'Hamilton', 'Romero', 'Rush', 'Alvarez',
            'Williamson', 'Fletcher', 'Cannon', 'Blackwell', 'Mora', 'Ford', 'Lowe', 'Hutchinson', 'Pineda', 'Chaney',
            'Best']

LOWER_BOUND_STUDENTS_PER_GROUP = 10

UPPER_BOUND_STUDENTS_PER_GROUP = 30

GROUP_SIZES = list(range(LOWER_BOUND_STUDENTS_PER_GROUP, UPPER_BOUND_STUDENTS_PER_GROUP + 1))

LOWER_BOUND_COURSES_PER_STUDENT = 1

UPPER_BOUND_COURSES_PER_STUDENT = 3

COURSES_AMOUNT_PER_STUDENT = list(range(LOWER_BOUND_COURSES_PER_STUDENT, UPPER_BOUND_COURSES_PER_STUDENT + 1))

#
# import random
# import string
#
#
# def generate_groups() -> list:
#
#     list_of_groups = []
#
#     for i in range(10):
#         characters = string.ascii_uppercase
#         digits = string.digits
#         char1 = random.choice(characters)
#         char2 = random.choice(characters)
#         digit1 = random.choice(digits)
#         digit2 = random.choice(digits)
#         group_name = "".join([char1, char2, "-", digit1, digit2])
#         list_of_groups.append(group_name)
#
#     return list_of_groups
#
#
# def generate_full_names(first_names: list, surnames:list) -> list:
#     list_of_full_names = []
#     for i in range(200):
#         name = random.choice(first_names)
#         surname = random.choice(surnames)
#         fullname = " ".join([name, surname])
#         list_of_full_names.append(fullname)
#     return list_of_full_names
#
#
# # def assign_students_to_groups(students: list, groups: list, lower_bound: int, upper_bound: int):
# #     groups_dict = {group: [] for group in groups}
#
#
# students = generate_full_names(NAMES, SURNAMES)
#
# groups = generate_groups()
#
# groups_dict = {group: [] for group in groups}
#
#
# group_sizes = list(range(LOWER_BOUND_STUDENTS_PER_GROUP, UPPER_BOUND_STUDENTS_PER_GROUP+1))
#
# for group in groups:
#     group_size = random.choice(group_sizes)
#     if len(students) >= group_size:
#         for i in range(group_size):
#             student = random.choice(students)
#             groups_dict[group].append(student)
#             students.remove(student)
#
#
# total_num = []
#
# for key, value in groups_dict.items():
#     print(key, len(value))
#     total_num.append(len(value))
#
# print(sum(total_num))
#
#
#

#
# lst = [1, 2]
# lst.pop(1)
# print(lst)