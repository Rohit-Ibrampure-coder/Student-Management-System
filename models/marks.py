from extensions import db
from models.subject import Subject

class Marks(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    student_name = db.Column(
        db.String(100),
        nullable=False
    )

    subject = db.Column(
        db.String(100),
        nullable=False
    )

    obtained_marks = db.Column(
        db.Integer,
        nullable=False
    )

    total_marks = db.Column(
        db.Integer,
        nullable=False
    )