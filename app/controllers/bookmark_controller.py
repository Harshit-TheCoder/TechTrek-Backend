from flask import Blueprint, request, jsonify, render_template
from app.models.bookmarks import Bookmarks

bookmark_bp = Blueprint('bookmark', __name__)

@bookmark_bp.route('/')
def home():
    return render_template('index.html')

@bookmark_bp.route('/add_bookmark', methods=['POST'])
def add_bookmark_question():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be a dictionary"}), 400
    
    username = data["Name"]
    useremail = data["Email"]
    userid = data["UserId"]
    questionid = data["QuestionId"]
    questionImportance = data["Importance"]

    info = {
        "Name": username,
        "Email": useremail,
        "UserId": userid,
        "QuestionId": questionid,
        "Question Importance": questionImportance
    }

    Bookmarks.insert_one(info)
    return jsonify({"message": "Question bookmarked successfully"}), 201

@bookmark_bp.route('/get_bookmark_question_id', methods=['POST'])
def get_bookmark_questions_id():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"message": "Data must be a dictionary"}), 400
    
    email = data["Email"]
    question_ids = Bookmarks.get_bookmark_questions_ids(email)
    return question_ids


