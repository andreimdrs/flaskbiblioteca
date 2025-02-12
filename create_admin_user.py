from models import db, User
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    # Create an admin user
    admin_user = User(username='admin', password='admin_password', role='admin') # type: ignore
    db.session.add(admin_user)
    db.session.commit()
    print("Admin user created.")
