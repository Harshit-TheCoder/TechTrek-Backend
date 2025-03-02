from flask import Blueprint, request, jsonify, render_template
from app.models.notes import Notes

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/')
def home():
    return render_template('index.html')

@notes_bp.route('/add_notes', methods=['POST'])
def add_notes():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be a dictionary"}), 400
    
    username = data["Name"]
    useremail = data["Email"]
    userid = data["UserId"]
    questionid = data["QuestionId"]
    questionNotes = data["Notes"]

    info = {
        "Name": username,
        "Email": useremail,
        "UserId": userid,
        "QuestionId": questionid,
        "Question Notes": questionNotes
    }

    Notes.insert_one(info)
    return jsonify({"message": "Notes added successfully"}), 201



