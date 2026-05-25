🎓 Student Management System (SMS)
A full-stack desktop application for managing students, attendance, and marks — built with a Python Flask REST API backend and a Tkinter GUI frontend. All data is stored in a local data.json file (no database setup required).

📁 Project Structure
student-management-system/
├── api.py          # Flask REST API (backend)
├── dashboard.py    # Tkinter GUI (frontend)
├── data.json       # JSON file database
└── migrate.py      # One-time MySQL → data.json migration script

🚀 Quick Start
1. Install Dependencies
bashpip install flask requests matplotlib
2. Start the API Server
bashpython api.py
The API will start at http://localhost:5000.
3. Launch the Dashboard
Open a new terminal and run:
bashpython dashboard.py
4. Login
FieldValueUsernameadminPasswordadmin123

🗂️ File-by-File Explanation

data.json — The Database
This file acts as the entire database. It has four top-level keys:
json{
  "admin":      [...],   // Admin login credentials
  "students":   [...],   // Student records
  "attendance": [...],   // Attendance entries
  "marks":      [...]    // Subject-wise marks per student
}
Student record example:
json{
  "student_id": 101,
  "student_name": "AYUSH",
  "age": 19,
  "department": "CSE"
}
Marks record example (5 subjects, max 100 each = 500 total):
json{
  "student_id": 101,
  "PPS": 23,
  "AEP": 23,
  "ESE": 26,
  "ODVC": 23,
  "BEE": 25
}

api.py — Flask REST API
The backend server. It reads/writes data.json on every request using two helper functions:
pythondef load():   # reads data.json → returns dict
def save():   # writes dict back to data.json
Auth
MethodEndpointDescriptionPOST/api/loginValidate admin credentials
Students
MethodEndpointDescriptionGET/api/studentsList all studentsGET/api/students/<id>Get one student by IDPOST/api/studentsAdd a new studentPUT/api/students/<id>Update student detailsDELETE/api/students/<id>Delete student + related marks/attendance
Attendance
MethodEndpointDescriptionGET/api/attendanceGet last 200 attendance recordsPOST/api/attendanceMark attendance for a studentGET/api/attendance/class-summaryTotal present/absent countGET/api/attendance/report/<id>Per-student attendance % report
Marks
MethodEndpointDescriptionGET/api/marks/<id>Get marks for a studentPOST/api/marksAdd marks (first time only)PUT/api/marks/<id>Update existing marksGET/api/marks/result/<id>Get total, percentage, and grade
Grading scale:
PercentageGrade≥ 90%A+≥ 75%A≥ 60%B≥ 40%C< 40%FAIL
Analytics
MethodEndpointDescriptionGET/api/analytics/class-dashboardClass stats: avg, highest, lowest, top 5, subject avgsGET/api/analytics/student/<id>Full profile: student info + marks + attendance
Health Check
MethodEndpointDescriptionGET/api/healthAPI status check

dashboard.py — Tkinter GUI
The frontend desktop app. It communicates with the API using four helper functions:
pythonapi_get(path)           # HTTP GET
api_post(path, body)    # HTTP POST
api_put(path, body)     # HTTP PUT
api_delete(path)        # HTTP DELETE
Application Flow
LoginWindow  →  (credentials verified via API)  →  Dashboard
LoginWindow

Centered 480×560 window with dark theme
Sends POST /api/login on submit (or pressing Enter)
On success: destroys login window and opens the main Dashboard

Dashboard
A 1300×800 window with:

Sidebar — navigation menu with 9 sections, highlighted active item, logout button
Top bar — current page title, today's date, live API status indicator (pings every 15 seconds)
Content area — dynamically swaps content based on selected nav item

Dashboard Sections
SectionWhat it does📊 DashboardStat cards (students, avg marks, attendance %) + bar chart + pie chart + recent students table➕ Add StudentForm to add a new student record👥 View StudentsFull paginated table of all students🔍 SearchLook up a student by ID, shows their full profile✏️ Update StudentEdit name, age, or department for an existing student🗑️ Delete StudentRemove a student and all their related records📅 AttendanceMark present/absent, view attendance records📝 Marks & ResultsAdd/update subject marks, generate result card with grade📈 AnalyticsSubject bar chart per student, attendance pie chart, class-wide dashboard
Charts (Matplotlib embedded in Tkinter)

Subject bar chart — colour-coded bars (one per subject) showing marks out of 100
Attendance pie chart — donut-style chart showing Present vs Absent %
Class subject average bar chart — average marks per subject across all students

UI Theme
The entire app uses a consistent dark design system:
RoleColourBackground#0f0e17Panel#1a1826Card#221f35Accent (orange)#e85d04Accent (purple)#7b2ff7Accent (cyan)#00b4d8Success (green)#06d6a0Danger (red)#ef233c

migrate.py — MySQL Migration (Optional)
If you were previously using a MySQL database, run this script once to export everything into data.json:
bashpip install mysql-connector-python
python migrate.py
Edit the connection details at the top of the file before running:
pythonconn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="student_management"
)
It migrates the admin, students, attendance, and marks tables. After running, restart api.py and dashboard.py — they will use the new data.json automatically.

🔄 How Everything Connects
dashboard.py  ──HTTP──▶  api.py  ──read/write──▶  data.json
    (GUI)                (REST API)                (JSON DB)

User interacts with dashboard.py
Dashboard calls api.py endpoints via HTTP
api.py loads data.json, performs the operation, saves back
Response is returned to the dashboard and displayed


📦 Dependencies
PackageUsed byPurposeflaskapi.pyREST API frameworkrequestsdashboard.pyHTTP calls to the APImatplotlibdashboard.pyEmbedded charts in the GUItkinterdashboard.pyDesktop GUI (built into Python)mysql-connector-pythonmigrate.pyMySQL migration (optional)

📌 Notes

data.json must be in the same directory as api.py
Run api.py before launching dashboard.py
The API runs on http://localhost:5000 by default
All data is stored locally — no internet connection required
