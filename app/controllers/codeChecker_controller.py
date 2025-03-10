from flask import Blueprint, jsonify, session, request
from app.models.code_checker import code_checker

code_bp = Blueprint("code", __name__)

@code_bp.route("/code_checker", methods=['POST'])
def code_checking_route():
    if request.is_json:
        data = request.get_json()
    else:  
        data = request.form  # Handle form submission

    question = data.get("question")
    code = data.get("code")
    language = data.get("language")

    return code_checker(question, code, language)