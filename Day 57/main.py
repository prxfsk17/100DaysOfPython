from flask import Flask, render_template
import requests
from post import Post

app = Flask(__name__)

blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
response = requests.get(blog_url)
response.raise_for_status()
all_posts = response.json()
list_of_blogs = [Post(post["title"], post["subtitle"], post["body"], post["id"]) for post in all_posts]

@app.route('/')
def home():
    return render_template("index.html", posts=list_of_blogs)

@app.route('/blog/<int:blog_id>')
def get_blog(blog_id):
    _blog=list_of_blogs[0]
    for bl in list_of_blogs:
        if bl.id == blog_id:
            _blog=bl
            break
    return render_template("post.html", blog=_blog)

if __name__ == "__main__":
    app.run(debug=True)
