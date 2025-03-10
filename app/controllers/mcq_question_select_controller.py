from flask import Flask, render_template, jsonify, Blueprint, request
from app.models.mcq_question_select import McqQuestionSelector

mcqselect_bp = Blueprint('mcqselect', __name__)


mcq_distribution = {
    30: {"Easy": 7, "Medium": 3, "Hard": 2},
    45: {"Easy": 10, "Medium": 6, "Hard": 2},
    60: {"Easy": 12, "Medium": 8, "Hard": 5},
    90: {"Easy": 18, "Medium": 12, "Hard": 5},
    120: {"Easy": 25, "Medium": 17, "Hard": 8}
}

@mcqselect_bp.route('/')
def home():
    return render_template('index.html')

@mcqselect_bp.route('/prepare_mcq_question_set', methods=['POST'])
def prepare_question_set():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be a dictionary"}), 400
    
    exam_duration = data["Duration"]

    easy_share = mcq_distribution[exam_duration]["Easy"]
    medium_share = mcq_distribution[exam_duration]["Medium"]
    hard_share = mcq_distribution[exam_duration]["Hard"]

    easy_questions_list = McqQuestionSelector.select_easy_mcq_questions(easy_share)
    medium_questions_list = McqQuestionSelector.select_medium_mcq_questions(medium_share)
    hard_questions_list = McqQuestionSelector.select_hard_mcq_questions(hard_share)

    questions_list=[]
    questions_list.append(easy_questions_list)
    questions_list.append(medium_questions_list)
    questions_list.append(hard_questions_list)

    return questions_list