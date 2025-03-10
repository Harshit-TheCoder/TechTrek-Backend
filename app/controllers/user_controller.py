from flask import Blueprint, request, jsonify, render_template
from app.models.users import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def home():
    return render_template('index.html')

@user_bp.route('/add_user', methods=['POST'])
def add_data():
    data = request.json
    if not isinstance(data, list):
        return jsonify({"error":"Data must be a list"}), 400
    
    try:

        response = User.register_user(data)
        if isinstance(response, tuple):
            return response
        
        return jsonify({"message": "Data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@user_bp.route('/login_user', methods=['POST'])
def verify_data():
    data = request.json
    if not data:
        return jsonify({"error": "No input data provided"}), 400  # Handle missing data

    try:
        response = User.login_user(data)
        if response:  # Ensure response is valid
            return response
        return jsonify({"error": "Unexpected error occurred"}), 500  # Fallback error response
    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400  # Handle missing keys
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@user_bp.route('/send_otp', methods=['POST'])
def send_mail():
    data = request.json
    email = data.get("Email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    return User.sendMail(email)






