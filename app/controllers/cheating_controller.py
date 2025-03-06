from flask import Blueprint, jsonify, session
from app.models.face_detection import detect_cheating

cheating_bp = Blueprint("cheating", __name__)

@cheating_bp.route("/detect_cheating", methods=["GET"])
def detect_cheating_route():
    """Starts face detection and returns warning count."""
    if session.get("warnings", 0) >= 5:
        return jsonify({"message": "Exam session ended due to repeated cheating", "warnings": session["warnings"]})
    
    result = detect_cheating()
    return jsonify(result)
