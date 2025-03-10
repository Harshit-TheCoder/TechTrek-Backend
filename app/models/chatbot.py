from app.models.database import get_db
from flask import Flask, render_template, jsonify, request
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

genai_model = genai.GenerativeModel("gemini-1.5-flash")
chat = genai_model.start_chat()

def chatbot(question):

    response = chat.send_message(question, stream=True)
    response.resolve()
    answer=""
    for chunk in response:
        answer += chunk.text
    print(answer)
    return str(answer)

    
