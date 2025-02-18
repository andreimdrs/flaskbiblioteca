from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.book import Book
from init import db

books_bp = Blueprint('books', __name__)

@books_bp.route('/')
def index():
    books = Book.query.all()
    return render_template('books.html', books=books)

@books_bp.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    author = request.form['author']
    
    book = Book(title=title, author=author, user_id=current_user.id) # type: ignore
    db.session.add(book)
    db.session.commit()
    
    return redirect(url_for('books.index'))