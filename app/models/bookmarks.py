from app.models.database import get_db

class Bookmarks:

    @staticmethod
    def insert_one(data):
        db = get_db()
        db.bookmarks.insert_one(data)

    @staticmethod
    def insert_many(data):
        db = get_db()
        db.bookmarks.insert_many(data)

    @staticmethod
    def get_bookmark_questions_ids(email):
        db = get_db()
        ids = db.bookmarks.find({"Email": email})
        return list(ids)