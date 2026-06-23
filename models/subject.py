from extensions import db

class Subject(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    course = db.Column(
        db.String(50),
        nullable=False
    )

    semester = db.Column(
        db.String(20),
        nullable=False
    )

    subject_name = db.Column(
        db.String(100),
        nullable=False
    )

    def __repr__(self):
        return f"<Subject {self.subject_name}>"