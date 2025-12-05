from flask import Flask, render_template
import requests

app = Flask(__name__)

blog_url = "https://api.npoint.io/358bc95d006f30a9c90f"
response = requests.get(blog_url)
response.raise_for_status()
all_posts = response.json()

@app.route("/")
def home():
    return render_template("index.html", posts=all_posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/blog/<int:id>")
def get_blog(id):
    blg=all_posts[id-1]
    return render_template("post.html", blog=blg)

if __name__ == "__main__":
    app.run(debug=True)