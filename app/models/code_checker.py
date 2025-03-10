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

def code_checker(question, code, language):
    user_question = f'''
    I am sending you the question along with the solution code. Please analyze it and return a JSON object with the following fields:
    
    - "syntax_errors": Describe any syntax errors found, or "No syntax errors".
    - "logical_errors": Describe any logical mistakes, or "No logical errors".
    - "runtime_errors": Describe potential runtime issues, or "No runtime errors".
    - "correctness": Indicate if the solution is correct, e.g., "The solution is correct" or "The solution has issues".
    - "failing_test_cases": List test cases that may fail if applicable.
    - "corrected_code": Provide an improved version of the code if errors exist.
    
    **IMPORTANT**: Your response **must be in valid JSON format**. Do not include additional text outside the JSON block.

    Question: {question}
    Code: {code}
    Language: {language}
    '''

    response = chat.send_message(user_question)

    try:
        # Ensure the response is in valid JSON format
        response_text = response.text.strip()

        # Look for JSON block in case AI adds extra text
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1

        if json_start == -1 or json_end == 0:
            return jsonify({"error": "AI response is not valid JSON. Please refine your prompt."})

        response_json = json.loads(response_text[json_start:json_end])

    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response. AI did not return valid JSON."})

    return jsonify(response_json)
