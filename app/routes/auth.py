from flask import Blueprint, request, redirect, url_for, flash, render_template
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

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = 'is_admin' in request.form  # Check if admin checkbox was checked

        if User.query.filter_by(username=username).first():
            flash('Usuário já existe')
            return redirect(url_for('auth.register'))

        user = User(username=username, is_admin=is_admin) # type: ignore
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('Registro realizado com sucesso!')
        return redirect(url_for('books.index'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('books.index'))
