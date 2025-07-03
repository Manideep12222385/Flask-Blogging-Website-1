from flask import Blueprint, render_template, redirect, url_for, request, flash
from forms.auth_forms import RegisterForm, LoginForm
from controllers.auth_controller import register_user, login_user_controller
from flask_login import login_required, logout_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = register_user(form)
        if user:
            flash('✅ Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
    elif request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"⚠️ {field.capitalize()}: {error}", 'danger')
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = login_user_controller(form)
        if user:
            flash('✅ Login successful!', 'success')
            return redirect(url_for('posts.show_posts'))
        else:
            flash("❌ Invalid email or password.", "danger")
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("🔒 Logged out successfully", "info")
    return redirect(url_for('auth.login'))
