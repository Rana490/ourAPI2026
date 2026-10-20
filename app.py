
from datetime import date
from functools import wraps
import os
import secrets

from flask import Flask, jsonify, request
from itsdangerous import URLSafeTimedSerializer, BadSignature
from itsdangerous import SignatureExpired

app = Flask(__name__)

# Use environment variables for secrets.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-only-change-me"
)

serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

ACCESS_TOKEN_MINUTES = 15
REFRESH_TOKEN_DAYS = 7

# Demo credentials for this exercise.
API_USERNAME = os.environ.get("API_USERNAME", "student")
API_PASSWORD = os.environ.get("API_PASSWORD", "change-me")


# ---------------------------------
# 1. CLASSES
# ---------------------------------

class Student:
    def __init__(self, ID_S, FN, LN, DMjr, Level):
        self.ID_S = ID_S
        self.FN = FN
        self.LN = LN
        self.DMjr = DMjr
        self.Level = Level

    def to_dict(self):
        return {
            "ID_S": self.ID_S,
            "FN": self.FN,
            "LN": self.LN,
            "DMjr": self.DMjr,
            "Level": self.Level
        }


class Report:
    def __init__(self, ID_R, Title, Type, K1, K2, K3, Release_Date):
        self.ID_R = ID_R
        self.Title = Title
        self.Type = Type
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3
        self.Release_Date = Release_Date

    def to_dict(self):
        return {
            "ID_R": self.ID_R,
            "Title": self.Title,
            "Type": self.Type,
            "K1": self.K1,
            "K2": self.K2,
            "K3": self.K3,
            "Release_Date": self.Release_Date
        }


# ---------------------------------
# 2. INITIAL DATA (PYTHON LISTS)
# ---------------------------------

students = [
    Student(1, "Sara", "Ben Ali", 1, 4),
    Student(2, "Ahmed", "Trabelsi", 0, 3)
]

reports = [
    Report(
        1, "Flask API", "Project",
        "Python", "Flask", "API", "2026-10-19"
    ),
    Report(
        2, "Microbiology", "Research",
        "Bacteria", "Culture", "Laboratory", "2026-10-18"
    )
]


# ---------------------------------
# 3. TOKEN FUNCTIONS
# ---------------------------------

def create_token(token_type, max_age):
    token = serializer.dumps({
        "type": token_type,
        "nonce": secrets.token_hex(8)
    })
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "error": "Authorization token required"
            }), 401

        token = parts[1]

        try:
            payload = serializer.loads(
                token,
                max_age=(
                    ACCESS_TOKEN_MINUTES * 60
                    if token_type_is_access(token)
                    else REFRESH_TOKEN_DAYS * 24 * 60 * 60
                )
            )
        except SignatureExpired:
            return jsonify({"error": "Token expired"}), 401
        except BadSignature:
            return jsonify({"error": "Invalid token"}), 401

        if payload.get("type") != "access":
            return jsonify({
                "error": "An access token is required"
            }), 401

        return f(*args, **kwargs)

    return decorated


def token_type_is_access(token):
    # Determine token type without trusting its contents.
    try:
        payload = serializer.loads(token, max_age=None)
        return payload.get("type") == "access"
    except BadSignature:
        return True


# ---------------------------------
# 4. TOKEN ENDPOINTS
# ---------------------------------

@app.route("/auth/token", methods=["POST"])
def get_token():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    if (
        data.get("username") != API_USERNAME
        or data.get("password") != API_PASSWORD
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "access_token": create_token("access", ACCESS_TOKEN_MINUTES),
        "refresh_token": create_token("refresh", REFRESH_TOKEN_DAYS),
        "token_type": "Bearer",
        "expires_in": ACCESS_TOKEN_MINUTES * 60
    }), 200


@app.route("/auth/refresh", methods=["POST"])
def refresh_token():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data.get("refresh_token"):
        return jsonify({"error": "Refresh token required"}), 400

    try:
        payload = serializer.loads(
            data["refresh_token"],
            max_age=REFRESH_TOKEN_DAYS * 24 * 60 * 60
        )
    except SignatureExpired:
        return jsonify({"error": "Refresh token expired; log in again"}), 401
    except BadSignature:
        return jsonify({"error": "Invalid refresh token"}), 401

    if payload.get("type") != "refresh":
        return jsonify({"error": "A refresh token is required"}), 401

    return jsonify({
        "access_token": create_token("access", ACCESS_TOKEN_MINUTES),
        "token_type": "Bearer",
        "expires_in": ACCESS_TOKEN_MINUTES * 60
    }), 200


# ---------------------------------
# 5. STUDENT ENDPOINTS
# ---------------------------------

@app.route("/students", methods=["GET"])
@token_required
def get_students():
    return jsonify([s.to_dict() for s in students]), 200


@app.route("/students/<int:student_id>", methods=["GET"])
@token_required
def get_student(student_id):
    student = next(
        (s for s in students if s.ID_S == student_id),
        None
    )

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student.to_dict()), 200


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    required = ["FN", "LN", "DMjr", "Level"]
    missing = [key for key in required if key not in data]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    if (
        not isinstance(data["FN"], str) or not data["FN"].strip()
        or not isinstance(data["LN"], str) or not data["LN"].strip()
    ):
        return jsonify({"error": "FN and LN must be non-empty strings"}), 400

    if type(data["DMjr"]) is not int or data["DMjr"] not in (0, 1):
        return jsonify({"error": "DMjr must be 0 or 1"}), 400

    if type(data["Level"]) is not int or data["Level"] not in (1, 2, 3, 4):
        return jsonify({"error": "Level must be 1, 2, 3, or 4"}), 400

    new_id = max((s.ID_S for s in students), default=0) + 1

    student = Student(
        new_id,
        data["FN"].strip(),
        data["LN"].strip(),
        data["DMjr"],
        data["Level"]
    )

    students.append(student)

    return jsonify(student.to_dict()), 201


# ---------------------------------
# 6. REPORT ENDPOINTS
# ---------------------------------

@app.route("/reports", methods=["GET"])
def get_reports():
    return jsonify([r.to_dict() for r in reports]), 200


@app.route("/reports/<int:report_id>", methods=["GET"])
def get_report(report_id):
    report = next(
        (r for r in reports if r.ID_R == report_id),
        None
    )

    if report is None:
        return jsonify({"error": "Report not found"}), 404

    return jsonify(report.to_dict()), 200


@app.route("/reports", methods=["POST"])
def add_report():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    required = ["Title", "Type", "K1", "K2", "K3", "Release_Date"]
    missing = [key for key in required if key not in data]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    if any(
        not isinstance(data[key], str) or not data[key].strip()
        for key in required
    ):
        return jsonify({
            "error": "All report fields must be non-empty strings"
        }), 400

    try:
        date.fromisoformat(data["Release_Date"])
    except ValueError:
        return jsonify({
            "error": "Release_Date must use YYYY-MM-DD"
        }), 400

    new_id = max((r.ID_R for r in reports), default=0) + 1

    report = Report(
        new_id,
        data["Title"].strip(),
        data["Type"].strip(),
        data["K1"].strip(),
        data["K2"].strip(),
        data["K3"].strip(),
        data["Release_Date"]
    )

    reports.append(report)

    return jsonify(report.to_dict()), 201


# ---------------------------------
# 7. OPTIONAL PUT AND DELETE
# ---------------------------------

@app.route("/students/<int:student_id>", methods=["PUT"])
@token_required
def update_student(student_id):
    student = next(
        (s for s in students if s.ID_S == student_id),
        None
    )

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    if "FN" in data:
        if not isinstance(data["FN"], str) or not data["FN"].strip():
            return jsonify({"error": "Invalid FN"}), 400
        student.FN = data["FN"].strip()

    if "LN" in data:
        if not isinstance(data["LN"], str) or not data["LN"].strip():
            return jsonify({"error": "Invalid LN"}), 400
        student.LN = data["LN"].strip()

    if "DMjr" in data:
        if type(data["DMjr"]) is not int or data["DMjr"] not in (0, 1):
            return jsonify({"error": "DMjr must be 0 or 1"}), 400
        student.DMjr = data["DMjr"]

    if "Level" in data:
        if type(data["Level"]) is not int or data["Level"] not in (1, 2, 3, 4):
            return jsonify({"error": "Level must be 1, 2, 3, or 4"}), 400
        student.Level = data["Level"]

    return jsonify(student.to_dict()), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
@token_required
def delete_student(student_id):
    student = next(
        (s for s in students if s.ID_S == student_id),
        None
    )

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    students.remove(student)
    return "", 204


@app.route("/reports/<int:report_id>", methods=["PUT"])
def update_report(report_id):
    report = next(
        (r for r in reports if r.ID_R == report_id),
        None
    )

    if report is None:
        return jsonify({"error": "Report not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    fields = ["Title", "Type", "K1", "K2", "K3", "Release_Date"]

    for key in fields:
        if key in data:
            if not isinstance(data[key], str) or not data[key].strip():
                return jsonify({"error": f"Invalid {key}"}), 400

    if "Release_Date" in data:
        try:
            date.fromisoformat(data["Release_Date"])
        except ValueError:
            return jsonify({"error": "Invalid Release_Date"}), 400

    for key in fields:
        if key in data:
            setattr(report, key, data[key].strip())

    return jsonify(report.to_dict()), 200


@app.route("/reports/<int:report_id>", methods=["DELETE"])
def delete_report(report_id):
    report = next(
        (r for r in reports if r.ID_R == report_id),
        None
    )

    if report is None:
        return jsonify({"error": "Report not found"}), 404

    reports.remove(report)
    return "", 204


# ---------------------------------
# 8. ERROR HANDLING
# ---------------------------------

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(error):
    app.logger.error("Internal server error: %s", error)
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
