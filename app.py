from flask import Flask
from config import Config
from extensions import db, migrate
from flask_login import LoginManager
from error_handlers import register_error_handlers
from routes.home_routes import home_bp
from routes.admin_routes import admin_bp

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to see posts."
    login_manager.login_message_category = 'info'

    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth_routes import auth_bp
    from routes.post_routes import post_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)

    register_error_handlers(app)
    return app
