from flask import Blueprint, request, jsonify, render_template
from app.models.feedbacks import Feedbacks

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/')
def home():
    return render_template('index.html')

@feedback_bp.route('/add_feedback', methods=['POST'])
def add_feedback():
    data = request.json

    if not isinstance(data, dict):
        return jsonify({"error": "Data must be a dictionary"}), 400
    
    username = data["Name"]
    useremail = data["Email"]
    userid = data["UserId"]
    testnumber = data["Test Number"]
    feedback = data["Feedback"]

    info = {
        "Name": username,
        "Email": useremail,
        "UserId": userid,
        "Test Number": testnumber,
        "Feedback": feedback
    }

    Feedbacks.insert_one(info)
    return jsonify({"message": "Feedback Submitted successfully"}), 201