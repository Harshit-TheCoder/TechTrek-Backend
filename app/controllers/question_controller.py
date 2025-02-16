from flask import Blueprint, request, jsonify, render_template
from app.models.question import Question

question_bp = Blueprint('question', __name__)

@question_bp.route('/')
def home():
    return render_template('index.html')

@question_bp.route('/add', methods=['POST'])
def add_data():
    data = request.json
    if not isinstance(data, list):  # Ensure data is a list of dictionaries
        return jsonify({"error": "Data must be a list"}), 400
    Question.insert_many(data)
    return jsonify({"message": "Data added successfully"}), 201

@question_bp.route('/questions', methods=['GET'])
def get_questions():
    return jsonify(Question.get_all()), 200