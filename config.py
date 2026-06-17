class Config:
    SECRET_KEY = "student-management-secret-key"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:system%40123@localhost/student_management"

    SQLALCHEMY_TRACK_MODIFICATIONS = False