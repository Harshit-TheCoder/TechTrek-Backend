from app.models.database import get_db

class McqQuestion:
    
    @staticmethod
    def insert_many(data):
        db = get_db()
        db.mcq_questions.insert_many(data)

    @staticmethod
    def get_one():
        db = get_db()
        return list(db.mcq_questions.findOne({}, {"_id": 1}))

    @staticmethod
    def get_all():
        db = get_db()
        return list(db.mcq_questions.find({}, {"_id": 1}))
    
