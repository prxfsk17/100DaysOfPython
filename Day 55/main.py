from flask import Flask

app = Flask(__name__)

def make_bold(func):
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper

def make_emphasis(func):
    def wrapper():
        return f"<em>{func()}</em>"
    return wrapper

def make_underlined(func):
    def wrapper():
        return f"<u>{func()}</u>"
    return wrapper

@app.route("/")
def hello_world():
    return ('<h1 style="text-align:center">Hello world!</h1>'
            '<p>This is a paragraph.</p>'
            '<img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMW44ZTJtb2txYms1azhhenBteDFwOTJ2MTZxam50OXMxZ3kwcGIwOSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/W1hd3uXRIbddu/giphy.gif" width=200>')

@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello {name}. You are {number} years old."

@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def bye():
    return "Bye"

if __name__ == "__main__":
    app.run(debug=True)