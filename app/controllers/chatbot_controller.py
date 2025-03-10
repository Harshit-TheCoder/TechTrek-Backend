from flask import Blueprint, jsonify, session, request
from app.models.chatbot import chatbot

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/chatbot", methods=['POST'])
def chatbot_route():
    if request.is_json:
        data = request.get_json()
    else:  
        data = request.form  # Handle form submission

    question = data.get("question")
    return chatbot(question)