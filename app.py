from flask import Flask, render_template
from flask_login import (
    LoginManager,
    login_required,
    current_user
)

from config import Config
from extensions import db

from models.user import User

from routes.auth import auth
from routes.student import student
from routes.attendance import attendance
from routes.marks import marks

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@app.route("/")
def home():

    return "Student Management System"


@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        user=current_user
    )


@app.route("/admin-dashboard")
@login_required
def admin_dashboard():

    return render_template(
        "admin_dashboard.html",
        user=current_user
    )


@app.route("/teacher-dashboard")
@login_required
def teacher_dashboard():

    return render_template(
        "teacher_dashboard.html",
        user=current_user
    )


@app.route("/student-dashboard")
@login_required
def student_dashboard():

    return render_template(
        "student_dashboard.html",
        user=current_user
    )


@app.route("/test")
def test():

    return str(
        current_user.is_authenticated
    )


# @app.route("/debug-user")
# @login_required
# def debug_user():

#     return f"""
#     Name: {current_user.name}<br>
#     Email: {current_user.email}<br>
#     Role: {current_user.role}
#     """


app.register_blueprint(auth)
app.register_blueprint(student)
app.register_blueprint(attendance)
app.register_blueprint(marks)


if __name__ == "__main__":

    app.run(debug=True)