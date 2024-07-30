from werkzeug.security import generate_password_hash
from app import db
from app.models import User

def update_user_passwords():
    # Fetch all users from the database
    users = User.query.all()

    for user in users:
        # Generate a new hash for each user's current password
        new_hash = generate_password_hash(user.password_hash, method='pbkdf2:sha256')

        # Update the user's password hash in the database
        user.password_hash = new_hash

    # Commit the changes to the database
    db.session.commit()

if __name__ == '__main__':
    update_user_passwords()
