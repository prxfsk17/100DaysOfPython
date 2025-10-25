class QuizBrain:
    def __init__(self, questions):
        self.question_number = 0
        self.questions_list = questions
        self.score = 0

    def still_have_questions(self):
        return self.question_number<len(self.questions_list)

    def next_question(self):
        answer = input(f"Q. {self.question_number+1}: {self.questions_list[self.question_number].text} (True/False)?: ")
        self.question_number += 1
        self.check_answer(answer, self.questions_list[self.question_number-1].answer)

    def check_answer(self, answer, correct):
        if answer.lower() == correct.lower():
            print("You got it right!")
            self.score += 1
        else:
            print("That's wrong!")
            print(f"The correct answer is {correct}.")
        print(f"Your current score is {self.score}/{self.question_number}")
        print("\n")

