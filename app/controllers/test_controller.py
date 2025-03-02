from flask import Blueprint, request, jsonify, render_template
from app.models.test import Test
from app.models.database import get_db
test_bp = Blueprint('test', __name__)

@test_bp.route('/')
def home():
    return render_template('index.html')

@test_bp.route('/add_result', methods=['POST'])
def result():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be a dictionary"}),400
    
    user_email = data["Email"]
    print(user_email)
    if not user_email:
        return jsonify({"Error": "Email is required"}), 400
    
    db = get_db()

    user = db.users.find_one({"Email": user_email}, {"_id": 1})

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user_id = str(user["_id"])

    test_data={
        "Name": data["Name"],
        "Email": user_email,
        "UserId": user_id,
        "Total Questions": data["Total Questions"],
        "Questions Attempted": data["Questions Attempted"],
        "Correct Questions": data["Correct Questions"],
        "Easy Questions Attempted": data["Easy Questions Attemped"],
        "Medium Questions Attempted": data["Medium Questions Attempted"],
        "Hard Questions Attempted": data["Hard Questions Attempted"]
    }

    Test.insert_one(test_data)

    return jsonify({"message": "Result saved successfully", "user_id": user_id}), 201



@test_bp.route('/get_leaderboard', methods=['GET'])
def leaderboard():
    users = Test.sort_by_performance()
    return users


@test_bp.route('/user_test_history', methods=['POST'])
def user_test_history():
    data = request.json
    email = data["Email"]
    history = Test.get_user_history(email)
    return history
