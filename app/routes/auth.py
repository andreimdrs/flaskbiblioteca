from flask import Blueprint, request, redirect, url_for, flash, render_template
from app.models.user import User

from flask_login import login_user, logout_user
from app.models.user import User
from app.init import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            if user.is_admin:
                flash('Login de administrador realizado com sucesso')
            else:
                flash('Login realizado com sucesso')
            return redirect(url_for('books.index'))
        flash('Credenciais inválidas')
    return render_template('login.html')

@auth_bp.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('auth.create_admin'))

        user = User(username=username, is_admin=True)  # Set is_admin to True
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Admin user created successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('create_admin.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form.get('is_admin', False)

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=username, is_admin=is_admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')




@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('books.index'))
