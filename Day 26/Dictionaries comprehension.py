# new_dict = {new_key:new_value for (key,value) in dict.items() if test}
# import random
#
# names = ["Alex", "Beth", "Caroline", "Freddie"]
# students_scores = {student:random.randint(1,100) for student in names}
# print(students_scores)
#
# passed_students = {student:score for (student, score) in students_scores.items() if score > 59}
# print(passed_students)
#
student_dict = {
    "student": ["Alex", "Beth", "Caroline", "Freddie"],
    "score": [56, 76, 98, 33]
}
# for (key, value) in student_dict.items():
#     print(value)

import pandas
student_data_frame = pandas.DataFrame(student_dict)
print(student_data_frame)
# for (key, value) in student_data_frame.items():
#     print(value)
for (index, row) in student_data_frame.iterrows():
    print(row.score)