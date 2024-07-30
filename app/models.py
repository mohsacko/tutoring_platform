# models.py
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# User model for authentication
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Add role field

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Updated Student model
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('student', uselist=False))
    
    classes = db.relationship('Class', secondary='student_classes', back_populates='students')

# Updated Tutor model
class Tutor(db.Model):
    __tablename__ = 'tutors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('tutor', uselist=False))

    classes = db.relationship('Class', back_populates='tutor')

# Class model
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    subject = db.Column(db.String(100), nullable=False)
    
    students = db.relationship('Student', secondary='student_classes', back_populates='classes')
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))
    tutor = db.relationship('Tutor', back_populates='classes')

# Create the association table for the many-to-many relationship
student_classes = db.Table('student_classes',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)
)
