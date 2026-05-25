"""
api.py  —  Flask REST API for Student Management System
Data stored in data.json (no MySQL needed)
Run with:  python api.py
Base URL:  http://localhost:5000
"""

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# ════════════════════════════════════════════════════════════════════
# JSON DB HELPERS
# ════════════════════════════════════════════════════════════════════

def load():
    """Load all data from JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save(data):
    """Save all data back to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def err(msg, code=400):
    return jsonify({"success": False, "message": msg}), code

def ok(data=None, msg="Success", code=200):
    res = {"success": True, "message": msg}
    if data is not None:
        res["data"] = data
    return jsonify(res), code


# ════════════════════════════════════════════════════════════════════
# AUTH
# ════════════════════════════════════════════════════════════════════

@app.route("/api/login", methods=["POST"])
def login():
    """POST /api/login  body: {username, password}"""
    body = request.get_json() or {}
    u = body.get("username", "")
    p = body.get("password", "")
    db = load()
    match = any(a["username"] == u and a["password"] == p for a in db["admin"])
    if match:
        return ok(msg="Login successful")
    return err("Invalid credentials", 401)


# ════════════════════════════════════════════════════════════════════
# STUDENTS
# ════════════════════════════════════════════════════════════════════

@app.route("/api/students", methods=["GET"])
def get_students():
    """GET /api/students"""
    db = load()
    return ok(db["students"])


@app.route("/api/students/<int:sid>", methods=["GET"])
def get_student(sid):
    """GET /api/students/<id>"""
    db = load()
    s = next((x for x in db["students"] if x["student_id"] == sid), None)
    if s:
        return ok(s)
    return err("Student not found", 404)


@app.route("/api/students", methods=["POST"])
def add_student():
    """POST /api/students  body: {student_id, student_name, age, department}"""
    body = request.get_json() or {}
    db   = load()
    sid  = body.get("student_id")
    if any(x["student_id"] == sid for x in db["students"]):
        return err(f"Student ID {sid} already exists")
    db["students"].append({
        "student_id":   sid,
        "student_name": body.get("student_name", ""),
        "age":          body.get("age", 0),
        "department":   body.get("department", "")
    })
    save(db)
    return ok(msg="Student added successfully"), 201


@app.route("/api/students/<int:sid>", methods=["PUT"])
def update_student(sid):
    """PUT /api/students/<id>  body: {student_name, age, department}"""
    body = request.get_json() or {}
    db   = load()
    for s in db["students"]:
        if s["student_id"] == sid:
            s["student_name"] = body.get("student_name", s["student_name"])
            s["age"]          = body.get("age", s["age"])
            s["department"]   = body.get("department", s["department"])
            save(db)
            return ok(msg="Student updated")
    return err("Student not found", 404)


@app.route("/api/students/<int:sid>", methods=["DELETE"])
def delete_student(sid):
    """DELETE /api/students/<id>"""
    db  = load()
    old = len(db["students"])
    db["students"] = [x for x in db["students"] if x["student_id"] != sid]
    if len(db["students"]) < old:
        # also remove related marks and attendance
        db["marks"]      = [x for x in db["marks"]      if x["student_id"] != sid]
        db["attendance"] = [x for x in db["attendance"] if x["student_id"] != sid]
        save(db)
        return ok(msg="Student deleted")
    return err("Student not found", 404)


# ════════════════════════════════════════════════════════════════════
# ATTENDANCE
# ════════════════════════════════════════════════════════════════════

@app.route("/api/attendance", methods=["GET"])
def get_attendance():
    """GET /api/attendance"""
    db = load()
    return ok(db["attendance"][-200:])  # last 200


@app.route("/api/attendance", methods=["POST"])
def mark_attendance():
    """POST /api/attendance  body: {student_id, attendance_date, status}"""
    body = request.get_json() or {}
    db   = load()
    db["attendance"].append({
        "id":              len(db["attendance"]) + 1,
        "student_id":      body.get("student_id"),
        "attendance_date": body.get("attendance_date"),
        "status":          body.get("status", "present").lower()
    })
    save(db)
    return ok(msg="Attendance marked"), 201


@app.route("/api/attendance/class-summary", methods=["GET"])
def attendance_class_summary():
    """GET /api/attendance/class-summary"""
    db      = load()
    total   = len(db["attendance"])
    present = sum(1 for x in db["attendance"] if x["status"] == "present")
    return ok({"total": total, "present": present, "absent": total - present})


@app.route("/api/attendance/report/<int:sid>", methods=["GET"])
def attendance_report(sid):
    """GET /api/attendance/report/<id>"""
    db      = load()
    records = [x for x in db["attendance"] if x["student_id"] == sid]
    total   = len(records)
    present = sum(1 for x in records if x["status"] == "present")
    absent  = total - present
    pct     = round(present / total * 100, 2) if total > 0 else 0
    return ok({
        "student_id":    sid,
        "total_classes": total,
        "present":       present,
        "absent":        absent,
        "percentage":    pct
    })


# ════════════════════════════════════════════════════════════════════
# MARKS
# ════════════════════════════════════════════════════════════════════

@app.route("/api/marks/<int:sid>", methods=["GET"])
def get_marks(sid):
    """GET /api/marks/<id>"""
    db = load()
    m  = next((x for x in db["marks"] if x["student_id"] == sid), None)
    if m:
        return ok(m)
    return err("No marks found", 404)


@app.route("/api/marks", methods=["POST"])
def add_marks():
    """POST /api/marks  body: {student_id, PPS, AEP, ESE, ODVC, BEE}"""
    body = request.get_json() or {}
    db   = load()
    sid  = body.get("student_id")
    if any(x["student_id"] == sid for x in db["marks"]):
        return err(f"Marks for student {sid} already exist. Use PUT to update.")
    db["marks"].append({
        "student_id": sid,
        "PPS":  body.get("PPS",  0),
        "AEP":  body.get("AEP",  0),
        "ESE":  body.get("ESE",  0),
        "ODVC": body.get("ODVC", 0),
        "BEE":  body.get("BEE",  0),
    })
    save(db)
    return ok(msg="Marks added"), 201


@app.route("/api/marks/<int:sid>", methods=["PUT"])
def update_marks(sid):
    """PUT /api/marks/<id>  body: {PPS, AEP, ESE, ODVC, BEE}"""
    body = request.get_json() or {}
    db   = load()
    for m in db["marks"]:
        if m["student_id"] == sid:
            m["PPS"]  = body.get("PPS",  m["PPS"])
            m["AEP"]  = body.get("AEP",  m["AEP"])
            m["ESE"]  = body.get("ESE",  m["ESE"])
            m["ODVC"] = body.get("ODVC", m["ODVC"])
            m["BEE"]  = body.get("BEE",  m["BEE"])
            save(db)
            return ok(msg="Marks updated")
    return err("No marks record found", 404)


@app.route("/api/marks/result/<int:sid>", methods=["GET"])
def get_result(sid):
    """GET /api/marks/result/<id>?max_marks=500"""
    max_marks = int(request.args.get("max_marks", 500))
    db = load()
    m  = next((x for x in db["marks"] if x["student_id"] == sid), None)
    if not m:
        return err("No marks found", 404)
    total = m["PPS"] + m["AEP"] + m["ESE"] + m["ODVC"] + m["BEE"]
    pct   = round(total / max_marks * 100, 2)
    if pct >= 90:   grade = "A+"
    elif pct >= 75: grade = "A"
    elif pct >= 60: grade = "B"
    elif pct >= 40: grade = "C"
    else:           grade = "FAIL"
    return ok({
        "student_id": sid,
        "marks":      m,
        "total":      total,
        "max_marks":  max_marks,
        "percentage": pct,
        "grade":      grade
    })


# ════════════════════════════════════════════════════════════════════
# ANALYTICS
# ════════════════════════════════════════════════════════════════════

@app.route("/api/analytics/class-dashboard", methods=["GET"])
def class_dashboard():
    """GET /api/analytics/class-dashboard"""
    db = load()

    total_students = len(db["students"])

    totals = [m["PPS"]+m["AEP"]+m["ESE"]+m["ODVC"]+m["BEE"] for m in db["marks"]]
    avg_marks     = round(sum(totals) / len(totals), 1) if totals else 0
    highest_marks = max(totals) if totals else 0
    lowest_marks  = min(totals) if totals else 0

    # subject averages
    subjects = ["PPS","AEP","ESE","ODVC","BEE"]
    subject_avgs = {}
    for s in subjects:
        vals = [m[s] for m in db["marks"]]
        subject_avgs[s] = round(sum(vals)/len(vals), 1) if vals else 0

    # top 5
    mark_totals = sorted(
        [{"student_id": m["student_id"],
          "name": next((st["student_name"] for st in db["students"] if st["student_id"] == m["student_id"]), "Unknown"),
          "total": m["PPS"]+m["AEP"]+m["ESE"]+m["ODVC"]+m["BEE"]}
         for m in db["marks"]],
        key=lambda x: x["total"], reverse=True
    )[:5]

    return ok({
        "total_students": total_students,
        "avg_marks":      avg_marks,
        "highest_marks":  highest_marks,
        "lowest_marks":   lowest_marks,
        "top5_students":  mark_totals,
        "subject_avgs":   subject_avgs
    })


@app.route("/api/analytics/student/<int:sid>", methods=["GET"])
def student_analytics(sid):
    """GET /api/analytics/student/<id>"""
    db = load()

    student = next((x for x in db["students"] if x["student_id"] == sid), None)
    if not student:
        return err("Student not found", 404)

    marks = next((x for x in db["marks"] if x["student_id"] == sid), None)

    records = [x for x in db["attendance"] if x["student_id"] == sid]
    total   = len(records)
    present = sum(1 for x in records if x["status"] == "present")
    att_pct = round(present / total * 100, 2) if total > 0 else 0

    result = None
    if marks:
        total_marks = marks["PPS"]+marks["AEP"]+marks["ESE"]+marks["ODVC"]+marks["BEE"]
        pct         = round(total_marks / 500 * 100, 2)
        if pct >= 90:   grade = "A+"
        elif pct >= 75: grade = "A"
        elif pct >= 60: grade = "B"
        elif pct >= 40: grade = "C"
        else:           grade = "FAIL"
        result = {"total": total_marks, "percentage": pct, "grade": grade}

    return ok({
        "student":    student,
        "marks":      marks,
        "result":     result,
        "attendance": {
            "total":      total,
            "present":    present,
            "absent":     total - present,
            "percentage": att_pct
        }
    })


# ════════════════════════════════════════════════════════════════════
# HEALTH
# ════════════════════════════════════════════════════════════════════

@app.route("/api/health", methods=["GET"])
def health():
    return ok({"status": "API running", "storage": "data.json"})


# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🚀  Student Management API (JSON mode) starting...")
    print("📁  Data file : data.json")
    print("📍  Base URL  : http://localhost:5000\n")
    app.run(debug=True, port=5000, host="127.0.0.1")