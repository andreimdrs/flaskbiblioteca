from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.book import Book
from app.init import db

books_bp = Blueprint('books', __name__)

@books_bp.route('/')
def index():
    books = Book.query.all()
    return render_template('book.html', books=books)

@books_bp.route('/add', methods=['GET', 'POST'])

@login_required
def add():
    if not current_user.is_admin:
        flash('Apenas administradores podem adicionar livros')
        return redirect(url_for('books.index'))
        
    title = request.form['title']
    author = request.form['author']
    
    book = Book(title=title, author=author, user_id=current_user.id) # type: ignore
    db.session.add(book)
    db.session.commit()
    
    flash('Livro adicionado com sucesso!')
    return redirect(url_for('books.index'))
