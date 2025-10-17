student_scores = [123, 43, 432, 412, 23, 66, 143, 165, 264, 286, 322, 222]
total_exam_score = sum(student_scores)
print(total_exam_score)
sum = 0
for score in student_scores:
    sum += score
print(sum)

print(max(student_scores))
max = student_scores[0]
for score in student_scores:
    if score > max:
        max = score
print(max)