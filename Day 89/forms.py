from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    email = StringField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])
    name = StringField("Name", [DataRequired()])
    submit = SubmitField("Registrate")

class LoginForm(FlaskForm):
    email = StringField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")


class TaskForm(FlaskForm):
    title = StringField('Task Title',
                        validators=[DataRequired(),
                                    Length(min=2, max=20, message='Title must be between 2 and 20 characters')])

    description = StringField('Description',
                                validators=[Length(max=100, message='Description cannot exceed 100 characters')])

    status = SelectField('Status',
                         choices=[
                             ('planned', 'Planned'),
                             ('in_progress', 'In Progress'),
                             ('completed', 'Completed')
                         ],
                         default='planned')

    submit = SubmitField('Add Task')