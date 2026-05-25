"""
migrate.py
Run this ONCE to copy all your MySQL data into data.json
Usage: python migrate.py
"""

import mysql.connector
import json
import os

# ── MySQL connection ─────────────────────────────────────────────────
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="namanpuri",
    database="student_management"
)
cur = conn.cursor(dictionary=True)

data = {
    "admin":      [],
    "students":   [],
    "attendance": [],
    "marks":      []
}

# ── Admin ────────────────────────────────────────────────────────────
try:
    cur.execute("SELECT * FROM admin")
    data["admin"] = cur.fetchall()
    print(f"✅ Admin      : {len(data['admin'])} records")
except Exception as e:
    print(f"⚠️  Admin table: {e}")
    data["admin"] = [{"username": "admin", "password": "admin123"}]

# ── Students ─────────────────────────────────────────────────────────
try:
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    data["students"] = [
        {
            "student_id":   r["student_id"],
            "student_name": r["student_name"],
            "age":          r["age"],
            "department":   r["department"]
        } for r in rows
    ]
    print(f"✅ Students   : {len(data['students'])} records")
except Exception as e:
    print(f"⚠️  Students   : {e}")

# ── Attendance ───────────────────────────────────────────────────────
try:
    cur.execute("SELECT * FROM attendance")
    rows = cur.fetchall()
    data["attendance"] = [
        {
            "id":              i + 1,
            "student_id":      r["student_id"],
            "attendance_date": str(r["attendance_date"]),
            "status":          r["status"].lower()
        } for i, r in enumerate(rows)
    ]
    print(f"✅ Attendance  : {len(data['attendance'])} records")
except Exception as e:
    print(f"⚠️  Attendance  : {e}")

# ── Marks ────────────────────────────────────────────────────────────
try:
    cur.execute("SELECT * FROM marks")
    rows = cur.fetchall()
    data["marks"] = [
        {
            "student_id": r["student_id"],
            "PPS":        r.get("PPS",  r.get("subject1", 0)),
            "AEP":        r.get("AEP",  r.get("subject2", 0)),
            "ESE":        r.get("ESE",  r.get("subject3", 0)),
            "ODVC":       r.get("ODVC", r.get("subject4", 0)),
            "BEE":        r.get("BEE",  r.get("subject5", 0)),
        } for r in rows
    ]
    print(f"✅ Marks       : {len(data['marks'])} records")
except Exception as e:
    print(f"⚠️  Marks       : {e}")

cur.close()
conn.close()

# ── Save to data.json ────────────────────────────────────────────────
out = os.path.join(os.path.dirname(__file__), "data.json")
with open(out, "w") as f:
    json.dump(data, f, indent=2)

print(f"\n🎉 Done! All data saved to data.json")
print(f"   Now restart api.py and dashboard.py")