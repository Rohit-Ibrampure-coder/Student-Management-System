from flask import Blueprint, render_template, request
from models.student import Student
from extensions import db
from flask import render_template
from sqlalchemy import or_
from flask import redirect, url_for, flash
from flask_login import current_user
from flask_login import login_required

student = Blueprint(
    "student",
    __name__
)

@student.route(
    "/add-student",
    methods=["GET", "POST"]
)
@login_required
def add_student():
    if current_user.role != "Admin":
        return "Access Denied"
    
    if request.method == "POST":

        roll_no = request.form.get("roll_no")
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        course = request.form.get("course")
        year = request.form.get("year")
        semester = request.form.get("semester")
        address = request.form.get("address")

        if not phone.isdigit():
            return "Phone number must contain only digits!"

        if len(phone) != 10:
            return "Phone number must be exactly 10 digits!"
        
        existing_roll = Student.query.filter_by(
            roll_no=roll_no
        ).first()

        if existing_roll:
            return "Roll Number already exists!"
        
        existing_email = Student.query.filter_by(
            email=email
        ).first()

        if existing_email:
            return "Email already exists!"

        new_student = Student(
            roll_no=roll_no,
            name=name,
            email=email,
            phone=phone,
            course=course,
            year=year,
            semester = semester,
            address=address
        )

        db.session.add(new_student)
        db.session.commit()

        flash(
            "Student Saved Successfully!",
            "success"
        )

        return redirect(
            url_for("student.students")
        )

    return render_template("add_student.html")

@student.route("/students")
def students():

    search = request.args.get("search")

    if search:

        all_students = Student.query.filter(

            or_(
                Student.name.contains(search),
                Student.roll_no.contains(search),
                Student.email.contains(search)
            )

        ).all()

    else:

        all_students = Student.query.all()

    return render_template(
        "students.html",
        students=all_students,
        search=search
    )

@student.route(
    "/edit-student/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_student(id):

    student = Student.query.get_or_404(id)
    
    if current_user.role != "Admin":
        return "Access Denied"

    if request.method == "POST":

        student.roll_no = request.form.get("roll_no")
        student.name = request.form.get("name")
        student.email = request.form.get("email")
        student.phone = request.form.get("phone")
        student.course = request.form.get("course")
        student.year = request.form.get("year")
        student.semester = request.form.get("semester")
        student.address = request.form.get("address")

        phone = request.form.get("phone")

        if not phone.isdigit():
            return "Phone number must contain only digits!"

        if len(phone) != 10:
            return "Phone number must be exactly 10 digits!"

        db.session.commit()

        flash(
            "Student Updated Successfully!",
            "success"
        )

        return redirect(
            url_for("student.students")
        )

    return render_template(
        "edit_student.html",
        student=student
    )

@student.route("/delete-student/<int:id>")
@login_required
def delete_student(id):

    student = Student.query.get_or_404(id)

    if current_user.role != "Admin":
        return "Access Denied"

    db.session.delete(student)

    db.session.commit()
    flash(
            "Student Delete Successfully!",
            "success"
        )
    return redirect(url_for("student.students"))
