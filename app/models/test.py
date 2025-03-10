from app.models.database import get_db
from app.models.users import User

class Test:

    @staticmethod
    def insert_test_data(data):
        db = get_db()
        db.test_details.insert_one(data)

    @staticmethod
    def insert_one(data):
        db = get_db()
        db.user_test_details.insert_one(data)

    @staticmethod
    def insert_many(data):
        db = get_db()
        db.user_test_details.insert_many(data)

    @staticmethod
    def sort_by_performance():
        db = get_db()
        pipeline = [
            {"$sort": {"_id": -1}},  # Sort by latest entry (MongoDB ObjectId is time-based)
            {"$group": {
                "_id": "$UserId",  # Group by UserId
                "latest_record": {"$first": "$$ROOT"}  # Take the latest entry
            }},
            {"$replaceRoot": {"newRoot": "$latest_record"}}  # Flatten the structure
        ]
        latest_results = list(db.user_test_details.aggregate(pipeline))

        sorted_results = sorted(latest_results, key=lambda x: (
            x["Questions Attempted"], 
            x["Hard Questions Attempted"], 
            x["Medium Questions Attempted"], 
            x["Easy Questions Attempted"]
        ), reverse=True)

        return sorted_results
    
    @staticmethod
    def get_user_history(email):
        db = get_db()
        user_history = list(db.user_test_details.find({"Email": email}))
        return user_history


    