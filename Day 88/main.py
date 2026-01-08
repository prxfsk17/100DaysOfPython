from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/")
def get_all_posts():
    return render_template("index.html")

@app.route("/")
def register():
    return render_template("index.html")

@app.route("/")
def login():
    return render_template("index.html")

@app.route("/")
def about():
    return render_template("index.html")

@app.route("/")
def contact():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)