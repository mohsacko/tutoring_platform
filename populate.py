import random
from app import app, db
from app.models import User, Student, Tutor, Class

def create_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create users with roles
        users = []
        for i in range(10):  # 10 users (5 students and 5 tutors)
            role = 'student' if i < 5 else 'tutor'
            user = User(email=f"user{i}@example.com", role=role)
            user.set_password("password123")
            db.session.add(user)
            users.append(user)
        db.session.commit()

        # Create students and tutors
        students = [Student(name=f"Student {i+1}", email=f"student{i+1}@example.com", user_id=users[i].id) for i in range(5)]
        tutors = [Tutor(name=f"Tutor {i+1}", email=f"tutor{i+1}@example.com", user_id=users[i+5].id) for i in range(5)]
        db.session.add_all(students + tutors)
        db.session.commit()

        # Create classes with subjects
        subjects = ["Physics", "Mathematics", "English"]
        classes = [Class(name=f"Class {i+1}", description=f"Description for class {i+1}", subject=random.choice(subjects)) for i in range(15)]
        db.session.add_all(classes)
        db.session.commit()

        # Assign students to classes
        for student in students:
            student_classes = random.sample(classes, 3)  # Each student will be in 3 classes
            for class_ in student_classes:
                class_.students.append(student)
        db.session.commit()

        # Assign classes to tutors
        for tutor in tutors:
            tutor_classes = random.sample(classes, 3)  # Each tutor will have 3 classes
            for class_ in tutor_classes:
                class_.tutor = tutor
        db.session.commit()

if __name__ == "__main__":
    create_data()
