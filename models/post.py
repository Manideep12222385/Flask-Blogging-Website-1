from datetime import datetime
from extensions import db
from models.user import User 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship("User", back_populates="posts")  

    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


    media_url = db.Column(db.String(255))

    reactions = db.relationship('Reaction', back_populates='post', lazy='dynamic', cascade='all, delete-orphan')



    def publish(self):
        self.is_published = True
        db.session.commit()

    def unpublish(self):
        self.is_published = False
        db.session.commit()

    def __repr__(self):
        return f'<Post {self.title}>'