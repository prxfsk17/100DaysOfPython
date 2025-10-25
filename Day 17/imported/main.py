from data import question_data, second_bank
from question_model import Question
from quiz_brain import QuizBrain

question_bank = []
for item in second_bank["results"]:
    question_bank.append(Question(item["question"], item["correct_answertr"]))

quiz = QuizBrain(question_bank)
while quiz.still_have_questions():
    quiz.next_question()

print("You've completed the quiz")
print(f"Your final score is {quiz.score}/{quiz.question_number}.")