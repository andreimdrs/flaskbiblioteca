from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # type: ignore
    
    with app.app_context():
        from app.models.user import User
        from app.models.book import Book
        db.create_all()
    
    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    
    return app