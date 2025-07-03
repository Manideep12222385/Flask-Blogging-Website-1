from flask import flash
from models.user import User, RoleEnum
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

def register_user(form):
    existing_user = User.query.filter(
        (User.username == form.username.data) |
        (User.email == form.email.data)
    ).first()

    if existing_user:
        flash('Username or email already exists.', 'error')
        return None

    user = User(
        username=form.username.data,
        email=form.email.data,
        password_hash=generate_password_hash(form.password.data),
        role=RoleEnum[form.role.data]
    )
    db.session.add(user)
    db.session.commit()
    return user

def login_user_controller(form):
    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return user

    return None
