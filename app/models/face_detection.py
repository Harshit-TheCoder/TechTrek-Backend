import cv2
import dlib
import numpy as np
from flask import session

# Load Dlib face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("app/models/shape_predictor_68_face_landmarks.dat")  # Ensure this file exists

def get_eye_region(landmarks, eye_points):
    """Extracts eye region from landmarks."""
    return np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in eye_points], np.int32)

def get_pupil_position(gray, eye_region):
    """Finds the pupil position."""
    mask = np.zeros_like(gray)
    cv2.fillPoly(mask, [eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)
    
    _, thresh = cv2.threshold(eye, 50, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
        else:
            cx = eye_region[:, 0].mean().astype(int)
        return cx
    return eye_region[:, 0].mean().astype(int)

def detect_cheating():
    """Detect cheating behavior and count warnings."""
    cap = cv2.VideoCapture(0)
    warnings = session.get("warnings", 0)  # Retrieve warning count from session

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 1)

        if len(faces) >= 2:
            cap.release()
            cv2.destroyAllWindows()
            session["warnings"] = 0
            return {"message": "Multiple faces detected. Camera stopped.", "warnings": warnings}

        cheating_detected = False

        for face in faces:
            landmarks = predictor(gray, face)

            left_eye_region = get_eye_region(landmarks, range(36, 42))
            right_eye_region = get_eye_region(landmarks, range(42, 48))

            left_pupil_x = get_pupil_position(gray, left_eye_region)
            right_pupil_x = get_pupil_position(gray, right_eye_region)

            left_eye_width = left_eye_region[:, 0].max() - left_eye_region[:, 0].min()
            right_eye_width = right_eye_region[:, 0].max() - right_eye_region[:, 0].min()

            left_relative_x = (left_pupil_x - left_eye_region[:, 0].min()) / left_eye_width
            right_relative_x = (right_pupil_x - right_eye_region[:, 0].min()) / right_eye_width

            if left_relative_x < 0.35 and right_relative_x < 0.35:
                text = "Looking Left (Cheating)"
                cheating_detected = True
            elif left_relative_x > 0.65 and right_relative_x > 0.65:
                text = "Looking Right (Cheating)"
                cheating_detected = True
            else:
                text = "Looking Straight (No Cheating)"

            color = (0, 0, 255) if cheating_detected else (0, 255, 0)
            cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        if cheating_detected:
            warnings += 1
            session["warnings"] = warnings  # Store warnings in session

            if warnings >= 50:
                cap.release()
                cv2.destroyAllWindows()
                session["warnings"] = 0
                return {"message": "Camera stopped after 8 warnings", "warnings": warnings}

        cv2.imshow("Exam Monitoring", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return {"message": "Cheating detection running", "warnings": warnings}
