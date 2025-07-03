import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from models.user import User

app = create_app()

with app.app_context():
    admin = User.query.filter_by(email='admin@example.com').first()
    if admin:
        admin.role = 'admin'
        db.session.commit()
        print(f"{admin.username} is now an Admin.")
    else:
        print("Admin user not found.")
