from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL, Email, Length, Optional
from flask_ckeditor import CKEditorField


class CreateCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired(), Length(min=2, max=250)])
    address = StringField("Address", validators=[DataRequired(), Length(min=5, max=500)])

    open_time = SelectField("Opening Time",
                               choices=[(f"{h:02d}:00", f"{h:02d}:00") for h in range(6, 12)],
                               validators=[DataRequired()])
    close_time = SelectField("Closing Time",
                               choices=[(f"{h:02d}:00", f"{h:02d}:00") for h in range(17, 24)],
                               validators=[DataRequired()])

    wifi_rating = SelectField("Wifi Quality",
                              choices=[(str(i), "★" * i) for i in range(1, 6)],
                              validators=[DataRequired()])
    has_power = BooleanField("✓ Power Outlets")
    coffee_quality = SelectField("Coffee Quality",
                                 choices=[(str(i), "★" * i) for i in range(1, 6)],
                                 validators=[DataRequired()])
    quietness = SelectField("Quietness",
                            choices=[(str(i), "★" * i) for i in range(1, 6)],
                            validators=[DataRequired()])

    coffee_price = SelectField("Coffee Price Range",
                               choices=[
                                   ("$", "$ - Cheap"),
                                   ("$$", "$$ - Moderate"),
                                   ("$$$", "$$$ - Expensive"),
                                   ("$$$$", "$$$$ - Very Expensive")
                               ],
                               validators=[DataRequired()])

    image_url = StringField("Cafe Photo URL",
                            validators=[DataRequired(), URL()],
                            render_kw={"placeholder": "https://example.com/photo.jpg"})
    location_url = StringField("Google Maps Link",
                               validators=[DataRequired(), URL()],
                               render_kw={"placeholder": "https://goo.gl/maps/..."})

    submit = SubmitField("Add Cafe", render_kw={"class": "btn btn-primary btn-lg"})

class RegisterForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    name=StringField("Name", validators=[DataRequired()])
    password=PasswordField("Password", validators=[DataRequired()])
    submit=SubmitField("Registrate")

class LoginForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=PasswordField("Password", validators=[DataRequired()])
    submit=SubmitField("Login")

class CommentForm(FlaskForm):
    body = CKEditorField("Commentaries:", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")