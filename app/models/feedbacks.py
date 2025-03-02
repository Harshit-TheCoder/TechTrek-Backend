from app.models.database import get_db

class Feedbacks:

    @staticmethod
    def insert_many(data):
        db = get_db()
        db.exam_feedbacks.insert_many(data)

    @staticmethod
    def insert_one(data):
        db = get_db()
        db.exam_feedbacks.insert_one(data)

    