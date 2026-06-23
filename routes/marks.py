from flask import Blueprint, render_template, request
from models.student import Student
from models.marks import Marks
from models.subject import Subject
from flask import redirect, url_for,flash
from extensions import db
from flask_login import current_user, login_required

marks = Blueprint(
    "marks",
    __name__
)

@marks.route(
    "/marks",
    methods=["GET", "POST"]
)
@login_required
def marks_page():

    if current_user.role != "Admin" and current_user.role != "Teacher":
        return "Access Denied"

    if request.method == "POST":

        student_id = request.form.get("student_id")

        subject = request.form.get("subject")

        obtained_marks = int(
            request.form.get("obtained_marks")
        )

        total_marks = int(
            request.form.get("total_marks")
        )

        if obtained_marks > total_marks:

            return "Obtained marks cannot be greater than total marks!"

        existing_marks = Marks.query.filter_by(
            student_id=student_id,
            subject=subject
        ).first()

        if existing_marks:

            return "Marks already entered for this subject!"

        student = Student.query.get(
            student_id
        )

        new_marks = Marks(
            student_id=student.id,
            student_name=student.name,
            subject=subject,
            obtained_marks=obtained_marks,
            total_marks=total_marks
        )

        db.session.add(new_marks)

        db.session.commit()

        flash(
            "Marks Saved Successfully!",
            "success"
        )

        return redirect(
            url_for("marks.marks_page")
        )

    students = Student.query.all()

    subjects = Subject.query.order_by(
        Subject.semester
    ).all()

    dashboard_link = "/teacher-dashboard"

    if current_user.role == "Admin":
        dashboard_link = "/admin-dashboard"

    return render_template(
        "add_marks.html",
        students=students,
        subjects=subjects,
        dashboard_link=dashboard_link
    )

@marks.route("/marks-records")
@login_required
def marks_records():

    search = request.args.get("search")

    if search:

        all_marks = Marks.query.filter(
            Marks.student_name.contains(search)
        ).all()

    else:

        all_marks = Marks.query.all()

    return render_template(
        "marks_records.html",
        marks=all_marks,
        search=search
    )

@marks.route("/report-card/<int:student_id>")
@login_required
def report_card(student_id):
    
    if current_user.role != "Admin" and current_user.role != "Teacher":
        return "Access Denied"

    student = Student.query.get_or_404(student_id)

    marks_data = Marks.query.filter_by(
        student_id=student_id
    ).all()

    total_obtained = 0
    total_possible = 0

    for mark in marks_data:

        total_obtained += mark.obtained_marks
        total_possible += mark.total_marks

    if total_possible > 0:

        percentage = (
            total_obtained / total_possible
        ) * 100

    else:

        percentage = 0

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    return render_template(
        "report_card.html",
        student=student,
        marks_data=marks_data,
        total_obtained=total_obtained,
        total_possible=total_possible,
        percentage=round(percentage, 2),
        grade=grade
    )

@marks.route(
    "/edit-marks/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_marks(id):
    
    mark = Marks.query.get_or_404(id)

    if current_user.role != "Admin" and current_user.role != "Teacher":
        return "Access Denied"

    if request.method == "POST":

        obtained_marks = int(
            request.form.get("obtained_marks")
        )

        total_marks = int(
            request.form.get("total_marks")
        )

        if obtained_marks > total_marks:
            return "Obtained marks cannot be greater than total marks!"

        mark.obtained_marks = obtained_marks
        mark.total_marks = total_marks

        db.session.commit()

        flash(
            "Marks Updated Successfully!",
            "success"
        )

        return redirect(
            url_for("marks.marks_records")
        )

    return render_template(
        "edit_marks.html",
        mark=mark
    )

@marks.route("/delete-marks/<int:id>")
@login_required
def delete_marks(id):
    
    mark = Marks.query.get_or_404(id)

    if current_user.role != "Admin" and current_user.role != "Teacher":
        return "Access Denied"

    db.session.delete(mark)

    db.session.commit()

    return redirect(
        url_for("marks.marks_records")
    )

@marks.route("/topper-list")
@login_required
def topper_list():
    
    if current_user.role != "Admin" and current_user.role != "Teacher":
        return "Access Denied"

    students = Student.query.all()

    topper_data = []

    for student in students:

        marks_data = Marks.query.filter_by(
            student_id=student.id
        ).all()

        total_obtained = 0
        total_possible = 0

        for mark in marks_data:

            total_obtained += mark.obtained_marks
            total_possible += mark.total_marks

        if total_possible > 0:

            percentage = (
                total_obtained / total_possible
            ) * 100

        else:

            percentage = 0

        topper_data.append({

            "name": student.name,
            "roll_no": student.roll_no,
            "percentage": round(
                percentage,
                2
            )

        })

    topper_data.sort(
        key=lambda x: x["percentage"],
        reverse=True
    )

    return render_template(
        "topper_list.html",
        topper_data=topper_data
    )

@marks.route("/marks-dashboard")
@login_required
def marks_dashboard():

    if current_user.role != "Admin" and current_user.role != "Teacher":
        return "Access Denied"

    total_students = Student.query.count()

    total_marks_records = Marks.query.count()

    students = Student.query.all()

    topper_name = "N/A"
    highest_percentage = 0

    total_percentage = 0
    student_count = 0

    for student in students:

        marks_data = Marks.query.filter_by(
            student_id=student.id
        ).all()

        total_obtained = 0
        total_possible = 0

        for mark in marks_data:

            total_obtained += mark.obtained_marks
            total_possible += mark.total_marks

        if total_possible > 0:

            percentage = (
                total_obtained / total_possible
            ) * 100

            total_percentage += percentage

            student_count += 1

            if percentage > highest_percentage:

                highest_percentage = percentage

                topper_name = student.name

    if student_count > 0:

        average_percentage = round(
            total_percentage / student_count,
            2
        )

    else:

        average_percentage = 0

    dashboard_link = "/teacher-dashboard"

    if current_user.role == "Admin":
        dashboard_link = "/admin-dashboard"

    return render_template(
        "marks_dashboard.html",
        total_students=total_students,
        total_marks_records=total_marks_records,
        average_percentage=average_percentage,
        topper_name=topper_name,
        highest_percentage=round(
        highest_percentage,
        2
    ),
    dashboard_link=dashboard_link
)


@marks.route("/my-marks")
@login_required
def my_marks():

    if current_user.role not in [
        "Admin",
        "Student"
    ]:
        return "Access Denied"

    student = Student.query.filter_by(
        email=current_user.email
    ).first()

    if not student:
        return "Student record not found!"

    marks_data = Marks.query.filter_by(
        student_id=student.id
    ).all()

    return render_template(
        "my_marks.html",
        student=student,
        marks_data=marks_data
    )

@marks.route("/my-report-card")
@login_required
def my_report_card():

    if current_user.role not in [
        "Admin",
        "Student"
    ]:
        return "Access Denied"

    student = Student.query.filter_by(
        email=current_user.email
    ).first()

    if not student:
        return "Student record not found!"

    marks_data = Marks.query.filter_by(
        student_id=student.id
    ).all()

    total_obtained = 0
    total_maximum = 0

    for mark in marks_data:

        total_obtained += mark.obtained_marks
        total_maximum += mark.total_marks

    if total_maximum > 0:

        percentage = (
            total_obtained / total_maximum
        ) * 100

    else:

        percentage = 0

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    return render_template(
        "my_report_card.html",
        student=student,
        marks_data=marks_data,
        total_obtained=total_obtained,
        total_maximum=total_maximum,
        percentage=round(percentage, 2),
        grade=grade
    )