import os

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from pyexpat.errors import messages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['UPLOAD_FOLDER'] = './static/files'

#authentification
login_manager = LoginManager()
login_manager.init_app(app)
load_dotenv()
app.secret_key = os.getenv("SECRET")

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        new_user=User(
            email=request.form.get("email"),
            password=generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8),
            name=request.form.get("name")
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("secrets"))
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    # check_password_hash
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")
        try:
            user_to_login=db.session.execute(db.select(User).where(User.email==email)).scalar()
            if user_to_login is None:
                raise AttributeError()
        except AttributeError:
            flash("This email does not exist.")
            return render_template("login.html", logged_in=current_user.is_authenticated)
        if check_password_hash(user_to_login.password, password):
            login_user(user_to_login)
            return redirect(url_for("secrets"))
        flash("Password is not correct.")
    return render_template("login.html", logged_in=current_user.is_authenticated)

@login_required
@app.route('/secrets')
def secrets():
    return render_template("secrets.html", name=current_user.name, logged_in=current_user.is_authenticated)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_required
@app.route('/download')
def download():
    return send_from_directory(
        app.config['UPLOAD_FOLDER'], "cheat_sheet.pdf", as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
