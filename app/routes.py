from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Student, Tutor, Class, User
from app.forms import LoginForm, RegistrationForm, ClassRegistrationForm
from flask import Blueprint
from collections import defaultdict

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            # Redirect based on user role
            if user.role == 'tutor':
                return redirect(url_for('main.tutor_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Create and save the User
        user = User(email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()  # Commit first to get the user ID
        
        # Create and save the Student or Tutor
        if form.role.data == 'tutor':
            new_user = Tutor(name=form.name.data, email=form.email.data, user_id=user.id)
        else:
            new_user = Student(name=form.name.data, email=form.email.data, user_id=user.id)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

@main.route('/get_classes/<subject>', methods=['GET'])
@login_required
def get_classes(subject):
    if current_user.role == 'student':
        student = current_user.student
        enrolled_classes = Class.query.filter(Class.students.any(id=student.id), Class.subject == subject).all()
        
        classes_data = [{
            'id': cls.id,
            'name': cls.name,
            'description': cls.description,
            'tutor': {
                'id': cls.tutor.id,
                'name': cls.tutor.name,
                'email': cls.tutor.email
            }
        } for cls in enrolled_classes]
        
        return jsonify(classes=classes_data)
    else:
        return jsonify(success=False, message="Unauthorized"), 403

@main.route('/get_tutor/<int:tutor_id>', methods=['GET'])
@login_required
def get_tutor(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)
    tutor_data = {
        'name': tutor.name,
        'email': tutor.email
    }
    return jsonify(tutor_data)

@main.route('/drop_class/<int:class_id>', methods=['POST'])
@login_required
def drop_class(class_id):
    if current_user.role == 'student':
        student = current_user.student
        cls = Class.query.get(class_id)

        # Log the class being dropped
        print(f"Attempting to drop class: {class_id}")

        # Log the student's enrolled classes
        enrolled_class_ids = [c.id for c in student.classes]
        print(f"Student enrolled classes: {enrolled_class_ids}")

        if cls is None:
            print("Class not found")
            return jsonify(success=False, message="Class not found"), 404
        if cls not in student.classes:
            print("Class not enrolled")
            return jsonify(success=False, message="Class not enrolled"), 400

        student.classes.remove(cls)
        db.session.commit()
        print("Class dropped successfully")
        return jsonify(success=True), 200
    return jsonify(success=False, message="Unauthorized"), 403


@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'tutor':
        return redirect(url_for('main.tutor_dashboard'))

    if current_user.role == 'student':
        student = current_user.student
        classes = student.classes

        grouped_classes = defaultdict(list)
        for cls in classes:
            grouped_classes[cls.subject].append(cls)

        return render_template('dashboard.html', grouped_classes=grouped_classes, student=student)
    
    flash('You do not have access to this page.', 'danger')
    return redirect(url_for('main.index'))


@main.route('/courses')
@login_required
def courses():
    subjects = current_user.interests
    return render_template('courses.html', subjects=subjects)

@main.route('/find_classes')
@login_required
def find_classes():
    # Get the current student's registered classes
    registered_class_ids = [cls.id for cls in current_user.student.classes]

    # Fetch all classes from the database, excluding those the student is registered for
    all_classes = Class.query.filter(~Class.id.in_(registered_class_ids)).all()
    
    # Group classes by subject
    subjects = {}
    for cls in all_classes:
        subject = cls.subject
        if subject not in subjects:
            subjects[subject] = []
        subjects[subject].append({
            'id': cls.id,
            'name': cls.name,
            'description': cls.description,
            'tutor': cls.tutor
        })
    
    # Convert to list of dictionaries for the template
    grouped_subjects = [{'subject': subject, 'classes': classes} for subject, classes in subjects.items()]

    return render_template('find_classes.html', subjects=grouped_subjects)

@main.route('/register_class', methods=['POST'])
@login_required
def register_class():
    class_id = request.form.get('class_id')
    cls = Class.query.get(class_id)

    if cls and cls not in current_user.student.classes:
        current_user.student.classes.append(cls)
        db.session.commit()
        return jsonify(success=True, message='Successfully registered for the class.')
    else:
        return jsonify(success=False, message='Class not found or you are already registered for this class.')

@main.route('/tutor_dashboard')
@login_required
def tutor_dashboard():
    if current_user.role != 'tutor':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('main.index'))

    tutor = current_user.tutor
    classes = tutor.classes
    class_details = defaultdict(dict)

    for cls in classes:
        class_details[cls.name]['description'] = cls.description
        class_details[cls.name]['students'] = cls.students

    return render_template('tutor_dashboard.html', tutor=tutor, class_details=class_details)



