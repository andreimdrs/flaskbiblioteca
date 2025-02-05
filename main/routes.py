from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models import db, User, Book

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def index():
    return render_template('main/index.html')

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

        new_book = Book(title=title, author=author, description=description, user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()

        flash('Book added successfully!')
        return redirect(url_for('main.index'))

    return render_template('main/add_book.html')
