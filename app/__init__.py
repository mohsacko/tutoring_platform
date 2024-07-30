from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize the app
app = Flask(__name__)

# Set up configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:binta1@localhost/tutoring_platform'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database and migration objects
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'  # Use blueprint's route name


# Import the models
from app.models import Student, Tutor, Class, User

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register the blueprint
from app.routes import main
app.register_blueprint(main)

# Ensure your routes are imported here
from app import routes

# This is necessary if you are using Flask's built-in server
if __name__ == '__main__':
    app.run(debug=True)
