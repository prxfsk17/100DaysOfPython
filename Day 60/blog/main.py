from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
import smtplib

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/358bc95d006f30a9c90f").json()
app = Flask(__name__)
load_dotenv()
sender=os.getenv("SENDER")
password=os.getenv("PASSWORD_SMTP")

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        error = None
        try:
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            message = request.form["message"]
            with smtplib.SMTP("smtp.gmail.com", port=587) as conn:
                conn.starttls()
                conn.login(user=sender, password=password)

                conn.sendmail(from_addr=sender, to_addrs=email,
                              msg=f"Subject: Message sent successfully!\n\nName: {name},\nEmail: {email},\nPhone: {phone},\nMessage: {message} .")
            return render_template("contact.html", text="Message sent successfully!")
        except KeyError:
            return render_template("contact.html", error=error)
    else:
        return render_template("contact.html", text="Contact Me")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
