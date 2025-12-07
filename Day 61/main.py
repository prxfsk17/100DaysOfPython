from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.fields.simple import SubmitField
from flask_bootstrap import Bootstrap5
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    login = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label="Log In")

app = Flask(__name__)
app.secret_key="yay"
bootstrap = Bootstrap5(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    l_form=LoginForm()
    if l_form.validate_on_submit():
        if l_form.login.data == "admin@email.com" and l_form.password.data == "12345678":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html", form=l_form)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
