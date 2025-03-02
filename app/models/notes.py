from app.models.database import get_db

class Notes:

    @staticmethod
    def insert_many(data):
        db = get_db()
        db.notes.insert_many(data)

    @staticmethod
    def insert_one(data):
        db = get_db()
        db.notes.insert_one(data)

        