from datetime import datetime
from app import db


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.Text)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    credits = db.Column(db.Integer)
    enrollment_limit = db.Column(db.Integer)
    status = db.Column(db.String(50))


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    max_score = db.Column(db.Integer)
    submission_format = db.Column(db.String(50))


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    score = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
