from extensions import db

class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    roll_no = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(15)
    )

    course = db.Column(
        db.String(50)
    )

    year = db.Column(
        db.String(20)
    )

    semester = db.Column(
        db.String(20)
    )
    
    address = db.Column(
        db.Text
    )

    def __repr__(self):
        return f"<Student {self.name}>"