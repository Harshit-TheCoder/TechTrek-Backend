from flask import Blueprint, request, jsonify, render_template
from app.models.mcq_question import McqQuestion

mcq_bp = Blueprint('mcq', __name__)

@mcq_bp.route('/')
def home():
    return render_template('index.html')

@mcq_bp.route('/add_mcqs', methods=['POST'])
def add_data():
    data = request.json
    if not isinstance(data, list):  # Ensure data is a list of dictionaries
        return jsonify({"error": "Data must be a list"}), 400
    McqQuestion.insert_many(data)
    return jsonify({"message": "Data added successfully"}), 201
