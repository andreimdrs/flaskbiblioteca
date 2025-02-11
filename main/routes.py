from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from flask_login import current_user, login_required
from models import Book, db, User

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/register_book', methods=['GET', 'POST'])
@login_required
def register_book():
    if current_user.role != 'admin':
        flash('Acesso negado. Apenas administradores podem registrar livros.')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')

        
        new_book = Book(title=title, author=author, isbn=isbn)  # Create a new book instance
        db.session.add(new_book)  # Add the book to the session
        db.session.commit()  # Commit the session to save the book

        flash('Livro registrado com sucesso!')
        return redirect(url_for('main.index'))
    
    return render_template('main/register_book.html')  # Create this template for book registration

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password and new_password != confirm_password:
            flash('As senhas não coincidem.')
            return redirect(url_for('main.profile'))

        if new_username:
            if User.query.filter_by(username=new_username).first():
                flash('Nome de usuário já existe. Escolha outro.')
                return redirect(url_for('main.profile'))
            current_user.username = new_username

        
        if new_password:
            current_user.set_password(new_password)

        db.session.commit()
        flash('Informações atualizadas com sucesso!')
        return redirect(url_for('main.profile'))

    return render_template('main/profile.html', user=current_user)
