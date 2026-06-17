from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from extensions import db
# from models.user import User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

@app.route("/")
def home():
    return "Student Management System"

if __name__ == "__main__":
    app.run(debug=True)