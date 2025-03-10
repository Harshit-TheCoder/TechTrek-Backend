from app.models.database import get_db

class Badges:
    
    @staticmethod
    def insert_many(data):
        db = get_db()
        db.badges.insert_many(data)

    @staticmethod
    def insert_one(data):
        db = get_db()
        db.badges.insert_one(data)