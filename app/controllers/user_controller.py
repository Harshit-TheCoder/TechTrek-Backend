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
    User.add_user(data)
    return jsonify({"message": "Data added successfully"}), 201


