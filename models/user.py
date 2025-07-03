from enum import Enum
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Boolean


class RoleEnum(str, Enum):
    ADMIN = 'ADMIN'
    PUBLISHER = 'PUBLISHER'
    VISITOR = 'VISITOR'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.PUBLISHER)
    is_verified = db.Column(db.Boolean, default=False)
    
    posts = db.relationship('Post', back_populates='author', lazy=True)
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')
    reactions = db.relationship('Reaction', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
