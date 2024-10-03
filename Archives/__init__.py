from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialiser la base de données
    db.init_app(app)

    # Importer les routes
    from .routes import main
    app.register_blueprint(main)

    return app

