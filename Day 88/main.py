from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean, CheckConstraint, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreateCafeForm, RegisterForm, LoginForm, CommentForm
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_KEY")
ckeditor = CKEditor(app)
#uncomment if you install new version as local files
# app.config['CKEDITOR_SERVE_LOCAL'] = True
Bootstrap5(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    name: Mapped[str] = mapped_column(String(100))

    cafes = relationship("Cafe", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Cafe(db.Model):
    __tablename__ = "cafes"
    __table_args__ = (
        CheckConstraint('wifi_rating >= 1 AND wifi_rating <= 5', name='check_wifi_rating'),
        CheckConstraint('coffee_quality >= 1 AND coffee_quality <= 5', name='check_coffee_quality'),
        CheckConstraint('quietness >= 1 AND quietness <= 5', name='check_quietness'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="cafes")

    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)

    open_time: Mapped[str] = mapped_column(String(10), nullable=False)
    close_time: Mapped[str] = mapped_column(String(10), nullable=False)

    wifi_rating: Mapped[float] = mapped_column(Integer, nullable=False)
    power_outlets: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    quietness: Mapped[float] = mapped_column(Integer, nullable=False)
    coffee_quality: Mapped[float] = mapped_column(Integer, nullable=False)

    coffee_price: Mapped[str] = mapped_column(String(50), nullable=False)

    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location_url: Mapped[str] = mapped_column(String(500), nullable=False)

    comments = relationship("Comment", back_populates="cafe")

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="comments")

    cafe_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("cafes.id"))
    cafe = relationship("Cafe", back_populates="comments")

    text: Mapped[str] = mapped_column(Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/register', methods=["GET", "POST"])
def register():
    r_form=RegisterForm()
    if r_form.validate_on_submit():
        email_data = r_form.email.data
        user = db.session.execute(db.select(User).where(User.email == email_data)).scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        new_user = User(
            email = email_data,
            name = r_form.name.data,
            password = generate_password_hash(r_form.password.data, method="pbkdf2:sha256", salt_length=8)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=r_form, logged_in=current_user.is_authenticated)

@app.route('/login', methods=["GET", "POST"])
def login():
    l_form=LoginForm()
    if l_form.validate_on_submit():
        email=l_form.email.data
        password=l_form.password.data
        try:
            user_to_login=db.session.execute(db.select(User).where(User.email==email)).scalar()
            if user_to_login is None:
                raise AttributeError()
        except AttributeError:
            flash("This email does not exist.")
            return render_template("login.html", form=l_form, logged_in=current_user.is_authenticated)
        if check_password_hash(user_to_login.password, password):
            login_user(user_to_login)
            return redirect(url_for("home"))
        flash("Password is not correct.")
    return render_template("login.html", form=l_form, logged_in=current_user.is_authenticated)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))

@app.route("/")
def home():
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()
    if current_user.is_authenticated:
        is_admin = current_user.id == 1
    else:
        is_admin = False
    return render_template("index.html", all_cafes=cafes, logged_in=current_user.is_authenticated, admin=is_admin)

@login_required
@app.route('/cafe/<int:cafe_id>', methods =["GET", "POST"])
def show_cafe(cafe_id):
    result = db.session.execute(db.select(Comment).where(Comment.cafe_id == cafe_id))
    comments = result.scalars().all()
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comm = Comment(
            text=comment_form.body.data,
            author=current_user,
            cafe=db.get_or_404(Cafe, cafe_id),
        )
        db.session.add(new_comm)
        db.session.commit()
        return redirect(url_for("show_cafe", cafe_id=cafe_id))
    else:
        cafe = db.get_or_404(Cafe, cafe_id)
        if current_user.is_authenticated:
            is_admin = current_user.id == 1
        else:
            is_admin = False

        return render_template("cafe.html", cafe=cafe, logged_in=current_user.is_authenticated,
                               admin=is_admin, form=comment_form, comments=comments)




@app.route('/add-cafe', methods=['GET', 'POST'])
@login_required
@admin_only
def add_cafe():
    form = CreateCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            author_id=current_user.id,
            name=form.name.data,
            address=form.address.data,
            open_time=form.open_time.data,
            close_time=form.close_time.data,
            wifi_rating=form.wifi_rating.data,
            power_outlets=form.has_power.data,
            quietness=form.quietness.data,
            coffee_quality=form.coffee_quality.data,
            coffee_price=form.coffee_price.data,
            image_url=form.image_url.data,
            location_url=form.location_url.data
        )

        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_cafe.html', form=form)

@app.route("/")
def get_all_posts():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
def contact():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)