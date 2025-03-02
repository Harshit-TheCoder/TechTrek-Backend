from app.models.database import get_db
import bcrypt
from flask import jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

class User:

    SENDER_EMAIL = "techtrek.helpline@gmail.com"
    SENDER_PASSWORD = "socc jqel uzeh nddl"



    @staticmethod
    def hashPassword(password):
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hash_password.decode('utf-8')
    
    @staticmethod
    def verify_password(stored_password, entered_password):
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8'))
    
    @staticmethod
    def register_user(user_data):
        db = get_db()
        if isinstance(user_data, list):
            users_to_insert = []
            for user in user_data:
                if User.get_user_by_email(user["Email"]):
                    return jsonify({"message": f"User with email {user['Email']} already exists"}), 400
                 
                user["Password"] = User.hashPassword(user["Password"])
                users_to_insert.append(user)

            if users_to_insert:
                return db.users.insert_many(users_to_insert) 
            else:
                return jsonify({"error": "No valid users to insert"}), 400 
        

        else:
            if User.get_user_by_email(user_data["Email"]):  # Check if user exists
                return jsonify({"error": "User already exists"}), 400
            user_data["Password"] = User.hashPassword(user_data["Password"])
            return db.users.insert_one(user_data) 
        
    @staticmethod
    def login_user(user_data):
        db = get_db()

        user = User.get_user_by_email(user_data["Email"])
        if not user:
            return jsonify({"error": "User does not exist"}), 404
        
        if user:
            if User.verify_password(user["Password"], user_data.get("Password", "")):
                return jsonify({"message": "User successfully logged in"}), 200
            else:
                return jsonify({"message": "Incorrect Password"}), 500
        else:
            return jsonify({"message" : "User does not exists"}), 401

    @staticmethod
    def sendMail(email):
          
        RECIEVER_EMAIL = email
        otp = str(random.randint(100000, 999999))
        subject = "🔐 Your TechTrek OTP for Login Verification"
        body = f"""\
Dear User,

We received a request to log into your TechTrek account. Please use the following One-Time Password (OTP) to complete your verification:

🔢 Your OTP: {otp}

This OTP is valid for 10 minutes. Do not share this code with anyone for security reasons.
If you did not request this, please ignore this email or contact our support team immediately.

Happy Coding! 🚀  
**Team TechTrek**
        """

        msg = MIMEMultipart()
        msg["From"] = User.SENDER_EMAIL
        msg["To"] = RECIEVER_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(User.SENDER_EMAIL, User.SENDER_PASSWORD)
            server.sendmail(User.SENDER_EMAIL, email, msg.as_string())
            server.quit()
            return jsonify({"message": "OTP sent successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to send OTP: {str(e)}"}), 500 

    
    @staticmethod
    def get_user_by_email(email):
        db = get_db()
        return db.users.find_one({"Email": email})
    
    @staticmethod
    def get_all_users():
        db = get_db()
        return list(db.users.find({}, {"_id": 0}))
    
    @staticmethod
    def delete_user(email):
        db = get_db()
        return db.users.delete_one({"email": email})
    
    