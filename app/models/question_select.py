from app.models.database import get_db

class QuestionSelector:

    @staticmethod
    def select_hard_questions(num_hard):
        db = get_db()
        question_list = list(db.questions.aggregate([{"$match": {"Difficulty": "Hard"}}, {"$sample": {"size": num_hard}}]))
        return question_list
    
    @staticmethod
    def select_medium_questions(num_medium):
        db = get_db()
        question_list = list(db.questions.aggregate([{"$match": {"Difficulty": "Medium"}}, {"$sample": {"size": num_medium}}]))
        return question_list
    
    @staticmethod
    def select_easy_questions(num_easy):
        db = get_db()
        question_list = list(db.questions.aggregate([{"$match": {"Difficulty": "Easy"}}, {"$sample": {"size": num_easy}}]))
        return question_list