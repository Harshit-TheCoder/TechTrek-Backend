from flask import Flask, render_template, jsonify, Blueprint, request
from app.models.question_select import QuestionSelector
from app.models.test import Test

qselect_bp = Blueprint('qselect', __name__)

difficulty_distribution = {
    "Easy": {"Easy": 0.7, "Medium": 0.2, "Hard": 0.1},
    "Medium": {"Easy": 0.2, "Medium": 0.7, "Hard": 0.1},
    "Hard": {"Easy": 0.1, "Medium": 0.2, "Hard": 0.7},
}
questions_per_duration = {
    60: 6, 
    90: 9, 
    120: 12
}

@qselect_bp.route('/')
def home():
    return render_template('index.html')

@qselect_bp.route('/prepare_question_set', methods=['POST'])
def prepare_question_set():
    test_details_data = {
        "Duration": 0,
        "Difficulty": 0,
        "Number of Questions": 0,
        "Number of Easy Questions": 0,
        "Easy Question Ids": [],
        "Number of Medium Questions": 0,
        "Medium Question Ids": [],
        "Number of Hard Questions": 0,
        "Hard Question Ids": [],
    }

    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be a dictionary"}), 400
    
    exam_difficulty = data["Difficulty"]
    exam_duration = data["Duration"]

    test_details_data["Duration"] = exam_duration
    test_details_data["Difficulty"] = exam_difficulty

    number_of_questions = questions_per_duration[exam_duration]
    easy_share = difficulty_distribution[exam_difficulty]["Easy"]
    medium_share = difficulty_distribution[exam_difficulty]["Medium"]
    hard_share = difficulty_distribution[exam_difficulty]["Hard"]

    test_details_data["Number of Easy Questions"] = round(number_of_questions*easy_share)
    test_details_data["Number of Medium Questions"] = round(number_of_questions*medium_share)
    test_details_data["Number of Hard Questions"] = round(number_of_questions*hard_share)
    test_details_data["Number of Questions"] = test_details_data["Number of Easy Questions"]+test_details_data["Number of Medium Questions"]+test_details_data["Number of Hard Questions"]

    easy_questions_list = QuestionSelector.select_easy_questions(round(number_of_questions*easy_share))
    medium_questions_list = QuestionSelector.select_medium_questions(round(number_of_questions*medium_share))
    hard_questions_list = QuestionSelector.select_hard_questions(round(number_of_questions*hard_share))


    easy_question_ids = [str(question["_id"]) for question in easy_questions_list]
    medium_question_ids = [str(question["_id"]) for question in medium_questions_list]
    hard_question_ids = [str(question["_id"]) for question in hard_questions_list]

    test_details_data["Easy Question Ids"] = easy_question_ids
    test_details_data["Medium Question Ids"] = medium_question_ids
    test_details_data["Hard Question Ids"] = hard_question_ids

    Test.insert_test_data(test_details_data)

    questions_list=[]
    questions_list.append(easy_questions_list)
    questions_list.append(medium_questions_list)
    questions_list.append(hard_questions_list)

    return questions_list