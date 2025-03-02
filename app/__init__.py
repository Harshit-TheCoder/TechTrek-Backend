from flask import Flask
from flask_pymongo import PyMongo
from config import Config

mongo = PyMongo()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    mongo.init_app(app)

    from app.controllers.question_controller import question_bp
    app.register_blueprint(question_bp)

    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    from app.controllers.test_controller import test_bp
    app.register_blueprint(test_bp)

    from app.controllers.bookmark_controller import bookmark_bp
    app.register_blueprint(bookmark_bp)

    from app.controllers.notes_controller import notes_bp
    app.register_blueprint(notes_bp)

    from app.controllers.feedback_controller import feedback_bp
    app.register_blueprint(feedback_bp)

    return app