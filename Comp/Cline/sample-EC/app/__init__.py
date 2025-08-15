from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Blueprint登録（後で実装）
    # from .routes.auth import auth_bp
    # app.register_blueprint(auth_bp)
    # ...他のBlueprintも同様に

    return app
