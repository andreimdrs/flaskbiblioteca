from models import db, User
from app import create_app  # Import the create_app function

app = create_app()  # Create an instance of the app

def create_admin_user():
    admin_username = 'root'
    admin_password = 'root'
    
    with app.app_context():  # Set up the application context
        # Check if the user already exists
        if User.query.filter_by(username=admin_username).first() is None:
            new_admin = User()  # Create a new User instance
            new_admin.username = admin_username  # Set the username
            new_admin.set_password(admin_password)
            new_admin.role = 'admin'  # Set the role to admin
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

if __name__ == "__main__":
    create_admin_user()