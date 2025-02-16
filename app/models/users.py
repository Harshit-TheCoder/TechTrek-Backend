from app.models.database import get_db

class User:

    @staticmethod
    def add_user(user_data):
        db = get_db()
        return db.users.insert_one(user_data)
    
    @staticmethod
    def get_user_by_email(email):
        db = get_db()
        return db.users.find_one({"email": email})
    
    @staticmethod
    def get_all_users():
        db = get_db()
        return list(db.users.find({}, {"_id": 0}))
    
    @staticmethod
    def delete_user(email):
        db = get_db()
        return db.users.delete_one({"email": email})
    
    