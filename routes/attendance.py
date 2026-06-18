from flask import Blueprint, render_template, request
from models.student import Student
from models.attendance import Attendance
from extensions import db
from datetime import datetime
from flask_login import current_user, login_required

attendance = Blueprint(
    "attendance",
    __name__
)

@attendance.route(
    "/attendance",
    methods=["GET", "POST"]
)
@login_required
def attendance_page():

    if current_user.role != "Admin" and current_user.role != "Teacher":
        return "Access Denied"

    if request.method == "POST":

        student_id = request.form.get("student_id")

        attendance_date = datetime.strptime(
            request.form.get("date"),
            "%Y-%m-%d"
        ).date()

        status = request.form.get("status")

        student = Student.query.get(student_id)

        existing_attendance = Attendance.query.filter_by(
            student_id=student_id,
            date=attendance_date
        ).first()

        if existing_attendance:
            return "Attendance already marked for this student on this date!"
        
        new_attendance = Attendance(
            student_id=student.id,
            student_name=student.name,
            date=attendance_date,
            status=status
        )

        db.session.add(new_attendance)
        db.session.commit()

        return "Attendance Saved Successfully!"

    students = Student.query.all()

    return render_template(
        "attendance.html",
        students=students
    )

@attendance.route("/attendance-records")
@login_required
def attendance_records():
    if current_user.role != "Admin" and current_user.role != "Teacher":
        return "Access Denied"
    
    search = request.args.get("search")

    if search:

        records = Attendance.query.filter(
            Attendance.student_name.contains(search)
        ).all()

    else:

        records = Attendance.query.all()

    return render_template(
        "attendance_records.html",
        records=records,
        search=search
    )

@attendance.route("/attendance-summary")
@login_required
def attendance_summary():

    if current_user.role != "Admin" and current_user.role != "Teacher":
        return "Access Denied"

    students = Student.query.all()

    summary_data = []

    for student in students:

        total_classes = Attendance.query.filter_by(
            student_id=student.id
        ).count()

        present_count = Attendance.query.filter_by(
            student_id=student.id,
            status="Present"
        ).count()

        absent_count = Attendance.query.filter_by(
            student_id=student.id,
            status="Absent"
        ).count()

        if total_classes > 0:

            percentage = (
                present_count / total_classes
            ) * 100

        else:

            percentage = 0

        summary_data.append({

            "name": student.name,

            "roll_no": student.roll_no,

            "total": total_classes,

            "present": present_count,

            "absent": absent_count,

            "percentage": round(
                percentage,
                2
            )

        })

    return render_template(
        "attendance_summary.html",
        summary_data=summary_data
    )