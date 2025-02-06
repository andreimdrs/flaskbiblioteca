import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models import db, User, Book

# Set up logging
logging.basicConfig(level=logging.INFO)

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
@login_required
def index():
    # Fetch the books created by the current user
    books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template('main/index.html', books=books)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html', user=current_user)

@main_bp.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form.get('description', '')

        try:
            new_book = Book(title=title, author=author, description=description, user_id=current_user.id)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!')
            return redirect(url_for('main.index'))
        except Exception as e:
            logging.error(f"Error adding book: {e}")
            flash('An error occurred while adding the book. Please try again.')

    return render_template('main/add_book.html')

@main_bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.description = request.form.get('description', '')

        try:
            db.session.commit()
            flash('Book updated successfully!')
            return redirect(url_for('main.index'))
        except Exception as e:
            logging.error(f"Error updating book: {e}")
            flash('An error occurred while updating the book. Please try again.')

    return render_template('main/edit_book.html', book=book)
