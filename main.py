from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/WebsiteQuestions"
mongo = PyMongo(app)

@app.route('/add', methods = ['POST'])
def add_data():
    data = request.json
    mongo.db.questions.insert_many(data)
    return jsonify({"message" : "Data added successfully1"}), 201

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)