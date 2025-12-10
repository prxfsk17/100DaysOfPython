import datetime

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, NumberRange
import requests

class EditForm(FlaskForm):
    rating = StringField(label="Your rating out of 10", validators=[DataRequired()])
    review = StringField(label="Review", validators=[DataRequired()])
    ranking = StringField(label="Ranking", validators=[DataRequired()])
    submit = SubmitField(label="Update")

class AddForm(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired()])
    year = IntegerField(
        'Year',
        validators=[
            DataRequired(message="Year is required."),
            NumberRange(min=1900, max=datetime.date.today().year,
                        message="Please enter a valid year between 1900 and the current year.")
        ]
    )
    description = StringField(label="Description", validators=[DataRequired()])
    rating = FloatField(label="Rating", validators=[DataRequired(), NumberRange(
                min=0.0,
                max=10.0,
                message='Value must be between 0 and 10.'
            )])
    ranking = IntegerField(label="Ranking", validators=[DataRequired()])
    review = StringField(label="Review", validators=[DataRequired()])
    url = StringField(label="URL to image of film", validators=[DataRequired()])
    submit = SubmitField(label="Add new film")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_movies=db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    edit_form = EditForm()
    if edit_form.validate_on_submit():
        movie_id = request.args.get("id")
        movie = db.get_or_404(Movie, movie_id)
        movie.review=edit_form.review.data
        movie.rating=edit_form.rating.data
        movie.ranking = edit_form.ranking.data
        db.session.commit()
        return redirect(url_for('home'))
    movie_id=request.args.get("id")
    movie=db.get_or_404(Movie, movie_id)
    return render_template("edit.html", form=edit_form, movie=movie)

@app.route("/delete", methods=["GET"])
def delete():
    movie_id=request.args.get("id")
    movie=db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        new_movie=Movie(title=add_form.title.data,
                        year=add_form.year.data,
                        description=add_form.description.data,
                        rating=add_form.rating.data,
                        ranking=add_form.ranking.data,
                        review=add_form.review.data,
                        url=add_form.url.data)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=add_form)

if __name__ == '__main__':
    app.run(debug=True)
