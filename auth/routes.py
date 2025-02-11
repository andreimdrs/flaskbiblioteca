from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user, login_user
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        current_password = request.form['current_password']

        # Verify current password
        if current_user.check_password(current_password):
            current_user.username = new_username
            if new_password:
                current_user.set_password(new_password)
            db.session.commit()
            flash('User information updated successfully!')
            return redirect(url_for('main.index'))
        else:
            flash('Current password is incorrect.')

    return render_template('auth/settings.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user')  # Default role to 'user'
        
        if User.query.filter_by(username=username).first():
            flash('Usuário já existe')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, role=role)  # Assign role to new user
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
