from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from utils.roles import role_required
from models.user import User
from extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/users')
@login_required
@role_required('ADMIN')
def list_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>/role', methods=['POST'])
@login_required
@role_required('ADMIN')
def change_role(user_id):
    new_role = request.form.get('role')
    user = User.query.get_or_404(user_id)
    
    if new_role not in ['ADMIN', 'PUBLISHER', 'VISITOR']:
        flash('Invalid role selected.', 'danger')
    else:
        user.role = new_role
        db.session.commit()
        flash(f"Role updated to {new_role} for {user.username}.", "success")

    return redirect(url_for('admin.list_users'))
