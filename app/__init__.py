from flask import Flask
from flask_pymongo import PyMongo
from config import Config

mongo = PyMongo()

def create_app():

    app = Flask(__name__)
    app.secret_key = "harshit-thecoder"
    app.config.from_object(Config)
    mongo.init_app(app)

    from app.controllers.question_controller import question_bp
    app.register_blueprint(question_bp)

    from app.controllers.mcq_question_controller import mcq_bp
    app.register_blueprint(mcq_bp)

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

    from app.controllers.cheating_controller import cheating_bp
    app.register_blueprint(cheating_bp)

    from app.controllers.codeChecker_controller import code_bp
    app.register_blueprint(code_bp)

    from app.controllers.chatbot_controller import chatbot_bp
    app.register_blueprint(chatbot_bp)

    from app.controllers.qselect_controller import qselect_bp
    app.register_blueprint(qselect_bp)

    from app.controllers.mcq_question_select_controller import mcqselect_bp
    app.register_blueprint(mcqselect_bp)

    return app