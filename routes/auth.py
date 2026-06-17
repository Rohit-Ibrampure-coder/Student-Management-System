from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash
from models.user import User
from extensions import db
from models.user import User
from flask_login import login_user
from werkzeug.security import check_password_hash
from flask import redirect, url_for
from flask_login import logout_user

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return "Passwords do not match!"

        # Check existing email
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered!"

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return "User Registered Successfully!"

    return render_template("signup.html")

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("dashboard"))

        return "Invalid Email or Password!"

    return render_template("login.html")

@auth.route("/logout")
def logout():

    logout_user()

    return redirect(url_for("auth.login"))