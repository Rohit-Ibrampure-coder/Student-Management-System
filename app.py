from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from extensions import db
from models.user import User
from routes.auth import auth
from flask_login import login_required, current_user
from flask import render_template
from flask_login import current_user
from routes.student import student
from routes.attendance import attendance

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

from flask_login import current_user

@app.route("/test")
def test():
    return str(current_user.is_authenticated)

app.register_blueprint(auth)
app.register_blueprint(student)
app.register_blueprint(attendance)
if __name__ == "__main__":
    app.run(debug=True)