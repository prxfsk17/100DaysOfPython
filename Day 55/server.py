from flask import Flask
from random import randint

num=0
app = Flask(__name__)

@app.route("/")
def home():
    return ('<h1>Guess a number between 0 and 9</h1>'
            '<img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGduYW56aWp2bzV3aHhxMWR5MnRqYmd1OGRmaWs3NGxjYmxhZ3k0OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JdFEeta1hLNnO/giphy.gif" width=200>')

@app.route("/<int:number>")
def guess(number):
    if number == num:
        return ('<h1 style="color:green">You found me</h1>'
                '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMm9nOTY3NXo1ZjV4amc0YzU4Ymd4bXNyN29oYzFwdG1veHpoY2N1NCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3oz9ZE2Oo9zRC/giphy.gif" width=200>')
    elif number > num:
        return ('<h1 style="color:blue">Too high, try again!</h1>'
                '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnRjbDB3bHc4OGR4a3BnbTIyYmJ4cTU3cGMzMzNkMHEwb3hnd3B4eSZlcD12MV9naWZzX3RyZW5kaW5nJmN0PWc/8qABb3dgjun8PdNirg/giphy.gif" width=200>')
    else:
        return ('<h1 style="color:purple">Too low, try again!</h1>'
                '<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmY3aGl4amZ5cHlnaHFqMjh0amFlN21kcDdydXNybmVkZXUydG8zMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/km2mais9qzYI/giphy.gif" width=200>')

if __name__ == "__main__":
    num=randint(0, 9)
    app.run(debug=True)