import os
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename

import colorgram

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_APP")
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
Bootstrap5(app)

class UploadForm(FlaskForm):
    file = FileField('Image File', validators=
    [FileRequired("There was no file selected!"),
     FileAllowed(["jpg", "png", "jpeg", "gif"], message="Images only!")
     ])
    submit = SubmitField("Upload")

def get_common_color(file):

    colors = colorgram.extract(file, 6)
    for color in colors:
        print(f"RGB: {color.rgb}, Proportion: {color.proportion:.4f}")
    return colors[0]

@app.route("/", methods=['GET', 'POST'])
def home():

    form = UploadForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            f.save(file_path)
            flash("Successful", "success")
        except:
            flash("Not successful", "warning")
            return redirect(url_for("home"))
        else:
            color=get_common_color(file_path)
            return render_template("home.html", form=form, color=color)

    return render_template("home.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)