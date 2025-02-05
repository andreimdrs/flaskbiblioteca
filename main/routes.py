from flask import Blueprint, render_template
from flask_login import current_user, login_required

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html', user=current_user)