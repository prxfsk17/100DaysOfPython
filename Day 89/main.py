from datetime import datetime
from typing import List

from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, TaskForm
import os
from dotenv import load_dotenv

status_names ={
    "planned" : "'Planned'",
    "in_progress" : "'In Progress'",
    "completed" : "Completed"
}

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Task(db.Model):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(25), default="planned")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="tasks")

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    name: Mapped[str] = mapped_column(String(100))

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="user",
                                               cascade="all, delete-orphan")

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@app.route("/register", methods=["POST", "GET"])
def register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        email = reg_form.email.data
        existing_user = db.session.execute(db.select(User).where(User.email==email)).scalar()
        if existing_user:
            flash("This email address is already in use. Please try another one or sign in.", "warning")
            return redirect(url_for("register"))
        user_to_create = User(
            email=email,
            name=reg_form.name.data,
            password = generate_password_hash(reg_form.password.data, method="pbkdf2", salt_length=8)
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        return redirect(url_for("home"))
    return render_template("register.html", form=reg_form, logged_in=current_user.is_authenticated)

@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        existing_user = db.session.execute(db.select(User).where(User.email==email)).scalar()
        if existing_user:
            if check_password_hash(existing_user.password, password):
                login_user(existing_user)
                return redirect(url_for("home"))
            else:
                flash("Invalid password.", "warning")
        else:
            flash("This email doesn't exist.", "warning")
            return redirect(url_for("login"))
    return render_template("login.html", form=login_form, logged_in=current_user.is_authenticated)

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect("about")

@app.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("about"))
    planned_tasks = db.session.execute(db.select(Task).where(Task.status == "planned", Task.user_id==current_user.id)).scalars().all()
    progress_tasks = db.session.execute(db.select(Task).where(Task.status == "in_progress", Task.user_id==current_user.id)).scalars().all()
    completed_tasks = db.session.execute(db.select(Task).where(Task.status == "completed", Task.user_id==current_user.id)).scalars().all()
    task_form = TaskForm()
    return render_template("main.html",
                           planned_tasks = planned_tasks,
                           in_progress_tasks = progress_tasks,
                           completed_tasks = completed_tasks,
                           logged_in = current_user.is_authenticated,
                           task_form = task_form)


@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            name=form.title.data,
            description=form.description.data,
            status=form.status.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')

    return redirect(url_for('home'))


@app.route('/update_task/<int:task_id>/<status>')
@login_required
def update_task(task_id, status):
    task = db.get_or_404(Task, task_id)

    if task.user_id == current_user.id:
        old_status = task.status
        task.status = status
        db.session.commit()
        if status == 'completed':
            flash(f'🎉 Task "{task.name}" completed! Great job!', 'success')
        elif old_status == 'planned' and status == 'in_progress':
            flash(f'🚀 Task "{task.name}" started!', 'info')
        elif old_status == 'in_progress' and status == 'planned':
            flash(f'↩️ Task "{task.name}" moved back to planning.', 'warning')
        else:
            flash(f'Task moved to {status_names.get(status, status)}', 'success')

    return redirect(url_for('home'))

@app.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)

    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted!', 'success')

    return redirect(url_for('home'))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)