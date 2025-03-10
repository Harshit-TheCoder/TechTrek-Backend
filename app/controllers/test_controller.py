from flask import Blueprint, request, jsonify, render_template
from app.models.test import Test
from app.models.users import User
from app.models.badges import Badges

from app.models.database import get_db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import date
import os

test_bp = Blueprint('test', __name__)

@test_bp.route('/')
def home():
    return render_template('index.html')

@test_bp.route('/add_result', methods=['POST'])
def result():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be a dictionary"}),400
    
    user_email = data["Email"]
    print(user_email)
    if not user_email:
        return jsonify({"Error": "Email is required"}), 400
    
    db = get_db()

    user = db.users.find_one({"Email": user_email}, {"_id": 1})

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user_id = str(user["_id"])

    test_data={
        "Name": data["Name"],
        "Email": user_email,
        "UserId": user_id,
        "TestId": data["TestId"],
        "Test Type" : "Coding Exam",
        "Duration": data["Duration"],
        "Difficulty": data["Difficulty"],
        "Total Questions": data["Total Questions"],
        "Question Ids": data["Question Ids"],
        "Questions Attempted": data["Questions Attempted"],
        "Question Unattempted" : data["Total Questions"] - data["Questions Attempted"],
        "Correct Questions": data["Correct Questions"],
        "Easy Questions Attempted": data["Easy Questions Attempted"],
        "Attempted Easy Question Ids": data["Attempted Easy Question Ids"],
        "Medium Questions Attempted": data["Medium Questions Attempted"],
        "Attempted Medium Question Ids": data["Attempted Medium Question Ids"],
        "Hard Questions Attempted": data["Hard Questions Attempted"],
        "Attempted Hard Question Ids": data["Attempted Hard Question Ids"]
    }

    Test.insert_test_data(test_data)

    subject = "🚀 TechTrek Mock Test Score Report - Your Performance Insights!"
    body = f"""\
Dear {data["Name"]},  

Congratulations on completing your TechTrek mock DSA test! 🎉  
Here's a summary of your performance:  

📌 **Test Details:**  
- **Test ID:** {data["TestId"]}  
- **Duration:** {data["Duration"]} minutes  
- **Difficulty Level:** {data["Difficulty"]} 
-- **Exam Format: Coding Exam**  

📊 **Your Performance:**  
✅ **Total Questions:** {data["Total Questions"]}  
🟢 **Attempted Questions:** {data["Questions Attempted"]}  
❌ **Unattempted Questions:** {data["Total Questions"] - data["Questions Attempted"]}  
🏆 **Correct Answers:** {data["Correct Questions"]}  

🎯 **Breakdown by Difficulty:**  
🔹 **Easy:** {data["Easy Questions Attempted"]} attempted  
🔹 **Medium:** {data["Medium Questions Attempted"]} attempted  
🔹 **Hard:** {data["Hard Questions Attempted"]} attempted  

Your dedication to improving your DSA skills is commendable! Keep practicing and sharpening your coding expertise. 🚀  

**Happy Coding!**  
**Team TechTrek**  

For feedbacks use techtrek.feedback@gmail.com
        """

    msg = MIMEMultipart()
    msg["From"] = "techtrek.results@gmail.com"
    msg["To"] = user_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("techtrek.results@gmail.com", "norp agtw jzep yhej")
        server.sendmail("techtrek.results@gmail.com", user_email, msg.as_string())
        server.quit()
        # return jsonify({"message": "Result saved successfully", "user_id": user_id}), 200
    except Exception as e:
        return jsonify({"error": f"Error occured: {str(e)}"}), 500
    

    accuracy = (float(data["Correct Questions"])/float(data["Questions Attempted"]))*100
    print(accuracy)
    
    user = User.get_user_by_email(user_email)
    print(user)
    theme = str(user["Theme"])
    print(theme)
    path = ""
    badge_name=""
    if theme == "Code of Olympus":
        if accuracy > 90:
            path = f"app/controllers/images/CodeOfOlympus/Gold.png"
            badge_name = "Zeus - King of Olympus"
        elif accuracy > 80:
            path = f"app/controllers/images/CodeOfOlympus/Silver.png"
            badge_name = "Athena - Goddess of Wisdom"
        elif accuracy > 70:
            path = f"app/controllers/images/CodeOfOlympus/Bronze.png"
            badge_name = "Hermes - Messenger of Gods"

    elif theme == "Shonen Coders":
        if accuracy > 90:
            path = f"app/controllers/images/ShonenCoders/Gold.png"
            badge_name = "Luffy - King of Pirates"
        elif accuracy > 80:
            path = f"app/controllers/images/ShonenCoders/Silver.png"
            badge_name = "Goku - Super Saiyan"
        elif accuracy > 70:
            path = f"app/controllers/images/ShonenCoders/Bronze.png"
            badge_name = "Naruto - Future Hokage"

    elif theme == "Wizarding Coders":
        if accuracy > 90:
            path = f"app/controllers/images/WizardingCoders/Gold.png"
            badge_name = "Dumbledore - Headmaster of Hogwarts"
        elif accuracy > 80:
            path = f"app/controllers/images/WizardingCoders/Silver.png"
            badge_name = "Hermione Granger - Brightest Witch of her age"
        elif accuracy > 70:
            path = f"app/controllers/images/WizardingCoders/Bronze.png"
            badge_name = "Ron Weasley - Gryffindor Prefect"

    if path != "" and badge_name != "":
        print(path)
        print(badge_name)

        achievement_data = {
            "Name": data["Name"],
            "Email": data["Email"],
            "UserId": user_id,
            "TestId": data["TestId"],
            "Test Type" : "Coding Exam",
            "Duration": data["Duration"],
            "Difficulty": data["Difficulty"],
            "Theme": theme,
            "Badge Name": badge_name
        }

        Badges.insert_one(achievement_data)
        
        subject = "🚀 Milestone Unlocked"
        email_body = f"""
    <html>
    <body>
        <h2>🎊 Congratulations, {data['Name']}!</h2>
        <p>You have earned the <b>{badge_name}</b> badge! 🏆</p>
        
        <p>🌟 <b>Badge Details:</b></p>
        <ul>
            <li>📌 <b>Theme:</b> {theme}</li>
            <li>📊 <b>Performance:</b> {accuracy:.2f}% Accuracy</li>
            <li>📅 <b>Test Date:</b> {date.today()}</li>
        </ul>
        
        <p>🎖️ Here's your badge:</p>
        <img src="cid:badge_image" alt="Badge Image" style="width: 300px; height: auto;">

        <p>Stay motivated and keep coding! 🚀</p>
        <p>Best Regards,<br>Team TechTrek</p>
    </body>
    </html>
    """

    # Attach HTML Body
        msg.attach(MIMEText(email_body, "html"))

        # Attach Image
        with open(path, "rb") as img_file:
            img = MIMEImage(img_file.read(), _subtype="png")
            img.add_header("Content-ID", "<badge_image>")
            img.add_header("Content-Disposition", "inline", filename=os.path.basename(path))
            msg.attach(img)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("techtrek.results@gmail.com", "norp agtw jzep yhej")
            server.sendmail("techtrek.results@gmail.com", user_email, msg.as_string())
            server.quit()
            return jsonify({"message": "Result saved successfully", "user_id": user_id}), 200
        except Exception as e:
            return jsonify({"error": f"Error occured: {str(e)}"}), 500
        

    return jsonify({"message": "Result saved successfully", "user_id": user_id}), 200
    



    



@test_bp.route('/add_mcq_test_result', methods=['POST'])
def mcq_result():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be a dictionary"}),400
    
    user_email = data["Email"]
    print(user_email)
    if not user_email:
        return jsonify({"Error": "Email is required"}), 400
    
    db = get_db()

    user = db.users.find_one({"Email": user_email}, {"_id": 1})

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user_id = str(user["_id"])

    test_data={
        "Name": data["Name"],
        "Email": user_email,
        "UserId": user_id,
        "TestId": data["TestId"],
        "Test Type" : "Multiple Choice Questions",
        "Duration": data["Duration"],
        "Total Questions": data["Total Questions"],
        "Question Ids": data["Question Ids"],
        "Questions Attempted": data["Questions Attempted"],
        "Question Unattempted" : data["Total Questions"] - data["Questions Attempted"],
        "Correct Questions": data["Correct Questions"],
        "Easy Questions Attempted": data["Easy Questions Attempted"],
        "Attempted Easy Question Ids": data["Attempted Easy Question Ids"],
        "Medium Questions Attempted": data["Medium Questions Attempted"],
        "Attempted Medium Question Ids": data["Attempted Medium Question Ids"],
        "Hard Questions Attempted": data["Hard Questions Attempted"],
        "Attempted Hard Question Ids": data["Attempted Hard Question Ids"]
    }

    Test.insert_test_data(test_data)

    subject = "🚀 TechTrek Mock MCQ Test Score Report - Your Performance Insights!"
    body = f"""\
Dear {data["Name"]},  

Congratulations on completing your TechTrek mock DSA test! 🎉  
Here's a summary of your performance:  

📌 **Test Details:**  
- **Test ID:** {data["TestId"]}  
- **Duration:** {data["Duration"]} minutes  
-- **Exam Format: Multiple Choice Questions**  

📊 **Your Performance:**  
✅ **Total Questions:** {data["Total Questions"]}  
🟢 **Attempted Questions:** {data["Questions Attempted"]}  
❌ **Unattempted Questions:** {data["Total Questions"] - data["Questions Attempted"]}  
🏆 **Correct Answers:** {data["Correct Questions"]}  

🎯 **Breakdown by Difficulty:**  
🔹 **Easy:** {data["Easy Questions Attempted"]} attempted  
🔹 **Medium:** {data["Medium Questions Attempted"]} attempted  
🔹 **Hard:** {data["Hard Questions Attempted"]} attempted  

Your dedication to improving your DSA skills is commendable! Keep practicing and sharpening your coding expertise. 🚀  

**Happy Coding!**  
**Team TechTrek**  

For feedbacks use techtrek.feedback@gmail.com
        """

    msg = MIMEMultipart()
    msg["From"] = "techtrek.results@gmail.com"
    msg["To"] = user_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("techtrek.results@gmail.com", "norp agtw jzep yhej")
        server.sendmail("techtrek.results@gmail.com", user_email, msg.as_string())
        server.quit()
        return jsonify({"message": "Result saved successfully", "user_id": user_id}), 200
    except Exception as e:
        return jsonify({"error": f"Error occured: {str(e)}"}), 500




@test_bp.route('/get_leaderboard', methods=['GET'])
def leaderboard():
    users = Test.sort_by_performance()
    return users


@test_bp.route('/user_test_history', methods=['POST'])
def user_test_history():
    data = request.json
    email = data["Email"]
    history = Test.get_user_history(email)
    return history
