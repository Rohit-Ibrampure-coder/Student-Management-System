from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.subject import Subject

subject = Blueprint(
    "subject",
    __name__
)


@subject.route(
    "/add-subject",
    methods=["GET", "POST"]
)
@login_required
def add_subject():

    if current_user.role != "Admin":
        return "Access Denied"

    if request.method == "POST":

        course = request.form.get("course")
        semester = request.form.get("semester")
        subject_name = request.form.get("subject_name")

        existing_subject = Subject.query.filter_by(
            course=course,
            semester=semester,
            subject_name=subject_name
        ).first()

        if existing_subject:
            return "Subject already exists!"

        new_subject = Subject(
            course=course,
            semester=semester,
            subject_name=subject_name
        )

        db.session.add(new_subject)
        db.session.commit()

        flash(
            "Subject Added Successfully!",
            "success"
        )

        return redirect(
            url_for("subject.subjects")
        )

    return render_template(
        "add_subject.html"
    )


@subject.route("/subjects")
@login_required
def subjects():

    if current_user.role != "Admin":
        return "Access Denied"

    all_subjects = Subject.query.all()

    return render_template(
        "subjects.html",
        subjects=all_subjects
    )


@subject.route(
    "/edit-subject/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_subject(id):

    if current_user.role != "Admin":
        return "Access Denied"

    subject_data = Subject.query.get_or_404(id)

    if request.method == "POST":

        subject_data.course = request.form.get("course")
        subject_data.semester = request.form.get("semester")
        subject_data.subject_name = request.form.get("subject_name")

        db.session.commit()

        flash(
            "Subject Updated Successfully!",
            "success"
        )

        return redirect(
            url_for("subject.subjects")
        )

    return render_template(
        "edit_subject.html",
        subject=subject_data
    )


@subject.route("/delete-subject/<int:id>")
@login_required
def delete_subject(id):

    if current_user.role != "Admin":
        return "Access Denied"

    subject_data = Subject.query.get_or_404(id)

    db.session.delete(subject_data)

    db.session.commit()

    flash(
            "Subject Delete Successfully!",
            "success"
        )
    
    return redirect(
        url_for("subject.subjects")
    )