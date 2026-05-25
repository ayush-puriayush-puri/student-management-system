import tkinter as tk
from tkinter import ttk, messagebox, font
import requests
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')
from datetime import datetime

# ─── API CLIENT ──────────────────────────────────────────────────────
API_BASE = "http://localhost:5000/api"

def api_get(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=8)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def api_post(path, body):
    try:
        r = requests.post(f"{API_BASE}{path}", json=body, timeout=8)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def api_put(path, body):
    try:
        r = requests.put(f"{API_BASE}{path}", json=body, timeout=8)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def api_delete(path):
    try:
        r = requests.delete(f"{API_BASE}{path}", timeout=8)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

# ─── COLORS ─────────────────────────────────────────────────────────
BG        = "#0f0e17"
PANEL     = "#1a1826"
CARD      = "#221f35"
ACCENT1   = "#e85d04"   # orange
ACCENT2   = "#7b2ff7"   # purple
ACCENT3   = "#00b4d8"   # cyan
GREEN     = "#06d6a0"
RED       = "#ef233c"
TEXT      = "#fffffe"
SUBTEXT   = "#a7a9be"
BORDER    = "#2e2b45"

# ─── FONTS ──────────────────────────────────────────────────────────
FONT_H1   = ("Segoe UI", 22, "bold")
FONT_H2   = ("Segoe UI", 14, "bold")
FONT_H3   = ("Segoe UI", 11, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL= ("Segoe UI", 9)
FONT_MONO = ("Consolas", 10)

# ─── HELPERS ────────────────────────────────────────────────────────
def styled_btn(parent, text, command, color=ACCENT1, width=18):
    b = tk.Button(parent, text=text, command=command,
                  bg=color, fg=TEXT, font=FONT_H3,
                  relief="flat", bd=0, cursor="hand2",
                  activebackground=color, activeforeground=TEXT,
                  padx=10, pady=6, width=width)
    b.bind("<Enter>", lambda e: b.config(bg=_lighten(color)))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def _lighten(hex_color):
    r = min(255, int(hex_color[1:3], 16) + 30)
    g = min(255, int(hex_color[3:5], 16) + 30)
    b = min(255, int(hex_color[5:7], 16) + 30)
    return f"#{r:02x}{g:02x}{b:02x}"

def card_frame(parent, **kwargs):
    return tk.Frame(parent, bg=CARD, bd=0,
                    highlightbackground=BORDER,
                    highlightthickness=1, **kwargs)

def label(parent, text, font_=FONT_BODY, color=TEXT, bg=CARD, **kw):
    return tk.Label(parent, text=text, font=font_, fg=color, bg=bg, **kw)

def entry_field(parent, width=22, show=None):
    e = tk.Entry(parent, font=FONT_BODY, bg="#2e2b45", fg=TEXT,
                 insertbackground=TEXT, relief="flat", bd=6,
                 highlightbackground=BORDER, highlightthickness=1,
                 width=width)
    if show:
        e.config(show=show)
    return e

# ════════════════════════════════════════════════════════════════════
# LOGIN WINDOW
# ════════════════════════════════════════════════════════════════════
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("480x560")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._center()
        self._build()

    def _center(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 480) // 2
        y = (self.root.winfo_screenheight() - 560) // 2
        self.root.geometry(f"480x560+{x}+{y}")

    def _build(self):
        # gradient top bar
        bar = tk.Frame(self.root, bg=ACCENT2, height=6)
        bar.pack(fill="x")

        wrap = tk.Frame(self.root, bg=BG)
        wrap.pack(expand=True)

        # icon
        icon = tk.Label(wrap, text="🎓", font=("Segoe UI Emoji", 52),
                        bg=BG, fg=TEXT)
        icon.pack(pady=(30, 0))

        tk.Label(wrap, text="Student Management", font=("Segoe UI", 20, "bold"),
                 bg=BG, fg=TEXT).pack()
        tk.Label(wrap, text="Sign in to continue", font=FONT_BODY,
                 bg=BG, fg=SUBTEXT).pack(pady=(4, 30))

        box = card_frame(wrap, padx=40, pady=30)
        box.pack(padx=40, fill="x")

        # username
        tk.Label(box, text="USERNAME", font=("Segoe UI", 8, "bold"),
                 fg=SUBTEXT, bg=CARD).pack(anchor="w")
        self.usr_var = tk.StringVar()
        usr_e = entry_field(box, width=28)
        usr_e.config(textvariable=self.usr_var)
        usr_e.pack(fill="x", pady=(4, 14))

        # password
        tk.Label(box, text="PASSWORD", font=("Segoe UI", 8, "bold"),
                 fg=SUBTEXT, bg=CARD).pack(anchor="w")
        self.pwd_var = tk.StringVar()
        pwd_e = entry_field(box, width=28, show="●")
        pwd_e.config(textvariable=self.pwd_var)
        pwd_e.pack(fill="x", pady=(4, 22))
        pwd_e.bind("<Return>", lambda e: self._login())

        self.msg_var = tk.StringVar()
        tk.Label(box, textvariable=self.msg_var, font=FONT_SMALL,
                 fg=RED, bg=CARD).pack()

        styled_btn(box, "  LOGIN  →", self._login,
                   color=ACCENT2, width=28).pack(pady=(8, 0), fill="x")

    def _login(self):
        u = self.usr_var.get().strip()
        p = self.pwd_var.get().strip()
        if not u or not p:
            self.msg_var.set("Please enter both fields.")
            return
        self.msg_var.set("Connecting to API...")
        self.root.update()
        res = api_post("/login", {"username": u, "password": p})
        if res.get("success"):
            self.root.destroy()
            main_root = tk.Tk()
            Dashboard(main_root)
            main_root.mainloop()
        elif "error" in res:
            self.msg_var.set(f"API Error: {res['error']}")
        else:
            self.msg_var.set("Invalid username or password.")

# ════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ════════════════════════════════════════════════════════════════════
class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("SMS — Dashboard")
        self.root.geometry("1300x800")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self._center()
        self._build_layout()
        self._show_section("dashboard")

    def _center(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 1300) // 2
        y = max(0, (self.root.winfo_screenheight() - 800) // 2)
        self.root.geometry(f"1300x800+{x}+{y}")

    # ── LAYOUT ─────────────────────────────────────────────────────
    def _build_layout(self):
        # top accent bar
        tk.Frame(self.root, bg=ACCENT2, height=4).pack(fill="x")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        # sidebar
        self.sidebar = tk.Frame(body, bg=PANEL, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        # main area
        self.main_area = tk.Frame(body, bg=BG)
        self.main_area.pack(side="left", fill="both", expand=True)
        self._build_topbar()

        self.content = tk.Frame(self.main_area, bg=BG)
        self.content.pack(fill="both", expand=True, padx=20, pady=10)

    def _build_sidebar(self):
        # logo area
        logo_f = tk.Frame(self.sidebar, bg=PANEL, pady=20)
        logo_f.pack(fill="x")
        tk.Label(logo_f, text="🎓", font=("Segoe UI Emoji", 28),
                 bg=PANEL, fg=TEXT).pack()
        tk.Label(logo_f, text="SMS", font=("Segoe UI", 16, "bold"),
                 bg=PANEL, fg=TEXT).pack()
        tk.Label(logo_f, text="Student Management", font=("Segoe UI", 8),
                 bg=PANEL, fg=SUBTEXT).pack()

        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=15)

        nav_items = [
            ("📊", "Dashboard",     "dashboard"),
            ("➕", "Add Student",   "add_student"),
            ("👥", "View Students", "view_students"),
            ("🔍", "Search",        "search_student"),
            ("✏️",  "Update Student","update_student"),
            ("🗑️",  "Delete Student","delete_student"),
            ("📅", "Attendance",    "attendance"),
            ("📝", "Marks",         "marks"),
            ("📈", "Analytics",     "analytics"),
        ]

        self.nav_buttons = {}
        nav_frame = tk.Frame(self.sidebar, bg=PANEL)
        nav_frame.pack(fill="x", pady=10)

        for icon, label_text, key in nav_items:
            f = tk.Frame(nav_frame, bg=PANEL, cursor="hand2")
            f.pack(fill="x", padx=8, pady=2)

            inner = tk.Frame(f, bg=PANEL, padx=12, pady=10)
            inner.pack(fill="x")

            ic = tk.Label(inner, text=icon, font=("Segoe UI Emoji", 13),
                          bg=PANEL, fg=TEXT)
            ic.pack(side="left")
            lb = tk.Label(inner, text=f"  {label_text}", font=FONT_BODY,
                          bg=PANEL, fg=TEXT)
            lb.pack(side="left")

            self.nav_buttons[key] = (f, inner, ic, lb)

            for w in (f, inner, ic, lb):
                w.bind("<Button-1>", lambda e, k=key: self._show_section(k))
                w.bind("<Enter>",    lambda e, fi=inner: fi.config(bg="#2a2745"))
                w.bind("<Leave>",    lambda e, fi=inner, k=key: fi.config(
                    bg=ACCENT2 if self._active == k else PANEL))

        # logout
        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=15, pady=10)
        styled_btn(self.sidebar, "  Logout", self._logout,
                   color="#3a3355", width=20).pack(padx=15, pady=10, fill="x")

    def _build_topbar(self):
        tb = tk.Frame(self.main_area, bg=PANEL, height=56)
        tb.pack(fill="x")
        tb.pack_propagate(False)

        self.page_title = tk.Label(tb, text="Dashboard", font=FONT_H2,
                                   fg=TEXT, bg=PANEL)
        self.page_title.pack(side="left", padx=24)

        now = datetime.now().strftime("%A, %d %B %Y")
        tk.Label(tb, text=now, font=FONT_SMALL, fg=SUBTEXT, bg=PANEL
                 ).pack(side="right", padx=24)

        # API status indicator
        self._api_status_label = tk.Label(tb, text="⬤ API", font=FONT_SMALL,
                                          fg=SUBTEXT, bg=PANEL)
        self._api_status_label.pack(side="right", padx=10)
        self._check_api_status()

    def _check_api_status(self):
        """Ping /api/health and update the status dot."""
        def ping():
            try:
                r = __import__("requests").get(f"{API_BASE}/health", timeout=3)
                ok = r.json().get("success", False)
            except:
                ok = False
            color = GREEN if ok else RED
            text  = "⬤ API Online" if ok else "⬤ API Offline"
            self._api_status_label.config(fg=color, text=text)
            # re-check every 15 seconds
            self.root.after(15000, self._check_api_status)
        import threading
        threading.Thread(target=ping, daemon=True).start()

    def _set_active_nav(self, key):
        self._active = key
        for k, (f, inner, ic, lb) in self.nav_buttons.items():
            if k == key:
                inner.config(bg=ACCENT2)
                for w in (ic, lb): w.config(bg=ACCENT2)
            else:
                inner.config(bg=PANEL)
                for w in (ic, lb): w.config(bg=PANEL)

    def _show_section(self, key):
        self._active = key
        self._set_active_nav(key)
        for w in self.content.winfo_children():
            w.destroy()
        titles = {
            "dashboard": "Dashboard", "add_student": "Add Student",
            "view_students": "All Students", "search_student": "Search Student",
            "update_student": "Update Student", "delete_student": "Delete Student",
            "attendance": "Attendance", "marks": "Marks & Results",
            "analytics": "Analytics",
        }
        self.page_title.config(text=titles.get(key, ""))
        getattr(self, f"_page_{key}")()

    def _logout(self):
        self.root.destroy()
        r = tk.Tk()
        LoginWindow(r)
        r.mainloop()

    # ── CLEAR helper ────────────────────────────────────────────────
    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════════
    # PAGE: DASHBOARD
    # ══════════════════════════════════════════════════════════════
    def _page_dashboard(self):
        res = api_get("/analytics/class-dashboard")
        if res.get("success"):
            d = res["data"]
            total_students = d["total_students"]
            avg_marks      = d["avg_marks"]
            total_marks    = total_students
        else:
            total_students = total_marks = avg_marks = 0

        # attendance overview via dedicated endpoint
        att_res = api_get("/attendance/class-summary")
        if att_res.get("success"):
            present_count = att_res["data"]["present"]
            total_att     = att_res["data"]["total"]
        else:
            present_count = total_att = 0

        att_pct = round((present_count/total_att*100) if total_att > 0 else 0, 1)

        # ── STAT CARDS ────
        cards_data = [
            ("👨‍🎓", "Total Students", str(total_students), ACCENT2, "+Active"),
            ("📊", "Avg Marks",      f"{avg_marks}",       ACCENT1, "/ 500 total"),
            ("✅", "Attendance",     f"{att_pct}%",         GREEN,   f"{present_count} present"),
            ("📝", "Records w/ Marks", str(total_marks),   ACCENT3, "students"),
        ]

        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", pady=(10, 16))

        for icon, title, val, col, sub in cards_data:
            c = tk.Frame(top, bg=CARD, bd=0,
                         highlightbackground=col,
                         highlightthickness=2)
            c.pack(side="left", fill="both", expand=True, padx=8)
            tk.Frame(c, bg=col, height=4).pack(fill="x")
            inner = tk.Frame(c, bg=CARD, padx=16, pady=14)
            inner.pack(fill="both", expand=True)
            tk.Label(inner, text=icon, font=("Segoe UI Emoji", 24),
                     bg=CARD, fg=col).pack(anchor="w")
            tk.Label(inner, text=val, font=("Segoe UI", 28, "bold"),
                     bg=CARD, fg=TEXT).pack(anchor="w", pady=(4,0))
            tk.Label(inner, text=title, font=FONT_SMALL,
                     bg=CARD, fg=SUBTEXT).pack(anchor="w")
            tk.Label(inner, text=sub, font=("Segoe UI", 8),
                     bg=CARD, fg=col).pack(anchor="w")

        # ── CHARTS ROW ───
        charts = tk.Frame(self.content, bg=BG)
        charts.pack(fill="both", expand=True, pady=4)

        # left – subject avg bar
        left = card_frame(charts)
        left.pack(side="left", fill="both", expand=True, padx=(8,4))
        tk.Label(left, text="Subject-wise Class Average",
                 font=FONT_H3, fg=TEXT, bg=CARD).pack(anchor="w", padx=12, pady=(10,0))
        self._draw_class_subject_avg(left)

        # right – attendance pie
        right = card_frame(charts)
        right.pack(side="left", fill="both", expand=True, padx=(4,8))
        tk.Label(right, text="Class Attendance Overview",
                 font=FONT_H3, fg=TEXT, bg=CARD).pack(anchor="w", padx=12, pady=(10,0))
        self._draw_attendance_summary(right, present_count, total_att - present_count)

        # ── RECENT TABLE ──
        rec = card_frame(self.content)
        rec.pack(fill="x", padx=8, pady=(10,4))
        tk.Label(rec, text="Recent Students", font=FONT_H3,
                 fg=TEXT, bg=CARD).pack(anchor="w", padx=12, pady=(10,4))
        self._draw_mini_table(rec)

    def _draw_class_subject_avg(self, parent):
        res = api_get("/analytics/class-dashboard")
        if res.get("success"):
            sa = res["data"]["subject_avgs"]
            avgs = [sa["PPS"], sa["AEP"], sa["ESE"], sa["ODVC"], sa["BEE"]]
        else:
            avgs = [0]*5

        fig = Figure(figsize=(5, 2.8), facecolor=CARD)
        ax  = fig.add_subplot(111, facecolor=CARD)
        subjects = ["PPS","AEP","ESE","ODVC","BEE"]
        colors_b = [ACCENT2, ACCENT1, GREEN, ACCENT3, "#f72585"]
        bars = ax.bar(subjects, avgs, color=colors_b, width=0.55, zorder=3)
        ax.set_ylim(0, 110)
        ax.set_ylabel("Avg Marks", color=SUBTEXT, fontsize=8)
        ax.tick_params(colors=SUBTEXT, labelsize=8)
        for spine in ax.spines.values(): spine.set_edgecolor(BORDER)
        ax.yaxis.grid(True, color=BORDER, linestyle="--", alpha=0.6, zorder=0)
        ax.set_facecolor(CARD)
        for bar_, val in zip(bars, avgs):
            ax.text(bar_.get_x() + bar_.get_width()/2, val+1,
                    str(val), ha="center", va="bottom",
                    color=TEXT, fontsize=8)
        fig.tight_layout(pad=1.0)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0,10))

    def _draw_attendance_summary(self, parent, present, absent):
        fig = Figure(figsize=(4, 2.8), facecolor=CARD)
        ax  = fig.add_subplot(111, facecolor=CARD)
        if present + absent == 0:
            present = absent = 1
        vals   = [present, absent]
        colors_p = [GREEN, RED]
        wedges, texts, autotexts = ax.pie(
            vals, labels=["Present","Absent"],
            colors=colors_p, autopct="%1.1f%%",
            startangle=140, wedgeprops=dict(width=0.6))
        for t in texts:     t.set_color(SUBTEXT); t.set_fontsize(8)
        for t in autotexts: t.set_color(TEXT);    t.set_fontsize(8)
        fig.tight_layout(pad=0.5)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0,10))

    def _draw_mini_table(self, parent):
        res = api_get("/students")
        rows = []
        if res.get("success"):
            for d in res["data"][:5]:
                rows.append((d["student_id"], d["student_name"], d["age"], d["department"]))

        cols = ("ID","Name","Age","Department")
        tv   = self._make_treeview(parent, cols)
        for row in rows:
            tv.insert("", "end", values=row)
        tv.pack(fill="x", padx=12, pady=(0,10))

    # ══════════════════════════════════════════════════════════════
    # PAGE: ADD STUDENT
    # ══════════════════════════════════════════════════════════════
    def _page_add_student(self):
        wrap = card_frame(self.content, padx=40, pady=30)
        wrap.pack(pady=20, anchor="n", fill="x", padx=40)

        tk.Label(wrap, text="Add New Student", font=FONT_H2,
                 fg=ACCENT2, bg=CARD).grid(row=0, column=0, columnspan=2,
                                            sticky="w", pady=(0,16))

        fields = [("Student ID", "int"), ("Name", "str"),
                  ("Age", "int"), ("Department", "str")]
        self._entries = {}
        for i, (lbl, _) in enumerate(fields):
            tk.Label(wrap, text=lbl, font=FONT_SMALL, fg=SUBTEXT,
                     bg=CARD).grid(row=i+1, column=0, sticky="w", pady=6, padx=(0,20))
            e = entry_field(wrap, width=32)
            e.grid(row=i+1, column=1, sticky="ew", pady=6)
            self._entries[lbl] = e

        self._msg_var = tk.StringVar()
        tk.Label(wrap, textvariable=self._msg_var, font=FONT_SMALL,
                 fg=GREEN, bg=CARD).grid(row=6, column=0, columnspan=2, pady=6)

        styled_btn(wrap, "  Add Student", self._do_add_student,
                   color=GREEN, width=20).grid(row=7, column=0, columnspan=2, pady=10)

    def _do_add_student(self):
        try:
            sid  = int(self._entries["Student ID"].get())
            name = self._entries["Name"].get().strip()
            age  = int(self._entries["Age"].get())
            dept = self._entries["Department"].get().strip()
            if not name or not dept:
                raise ValueError("Name/Dept empty")
            res = api_post("/students", {"student_id": sid, "student_name": name, "age": age, "department": dept})
            if res.get("success"):
                self._msg_var.set(f"✅ Student {name} added successfully!")
                for e in self._entries.values(): e.delete(0, "end")
            else:
                self._msg_var.set(f"❌ {res.get('error', res.get('message','Failed'))}")
        except Exception as ex:
            self._msg_var.set(f"❌ Error: {ex}")

    # ══════════════════════════════════════════════════════════════
    # PAGE: VIEW STUDENTS
    # ══════════════════════════════════════════════════════════════
    def _page_view_students(self):
        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", pady=(0,10))
        styled_btn(top, "↻ Refresh", self._page_view_students,
                   color=ACCENT3, width=12).pack(side="right")

        frame = card_frame(self.content)
        frame.pack(fill="both", expand=True, padx=4)

        cols = ("ID", "Name", "Age", "Department")
        tv   = self._make_treeview(frame, cols, height=22)
        res  = api_get("/students")
        if res.get("success"):
            for d in res["data"]:
                tv.insert("", "end", values=(d["student_id"], d["student_name"], d["age"], d["department"]))
        else:
            messagebox.showerror("API Error", res.get("error", "Failed to fetch students"))
        tv.pack(fill="both", expand=True, padx=10, pady=10)

    # ══════════════════════════════════════════════════════════════
    # PAGE: SEARCH STUDENT
    # ══════════════════════════════════════════════════════════════
    def _page_search_student(self):
        top = card_frame(self.content, padx=20, pady=16)
        top.pack(fill="x", padx=4, pady=(0,14))

        tk.Label(top, text="Student ID:", font=FONT_BODY, fg=TEXT,
                 bg=CARD).pack(side="left")
        self._search_var = tk.StringVar()
        e = entry_field(top, width=14)
        e.config(textvariable=self._search_var)
        e.pack(side="left", padx=12)
        e.bind("<Return>", lambda ev: self._do_search())
        styled_btn(top, "Search", self._do_search, color=ACCENT2, width=10
                   ).pack(side="left")

        self._search_result_frame = card_frame(self.content)
        self._search_result_frame.pack(fill="both", expand=True, padx=4)

    def _do_search(self):
        for w in self._search_result_frame.winfo_children():
            w.destroy()
        try:
            sid = int(self._search_var.get())
        except ValueError:
            tk.Label(self._search_result_frame, text="⚠  Enter a valid numeric ID",
                     font=FONT_BODY, fg=ACCENT1, bg=CARD).pack(pady=10)
            return

        res = api_get(f"/analytics/student/{sid}")
        if not res.get("success"):
            tk.Label(self._search_result_frame, text="❌  Student not found",
                     font=FONT_H3, fg=RED, bg=CARD).pack(pady=20)
            return

        data    = res["data"]
        student = data["student"]
        marks   = data["marks"]
        att     = data["attendance"]
        result  = data["result"]

        # info grid
        f = tk.Frame(self._search_result_frame, bg=CARD, padx=24, pady=20)
        f.pack(fill="x")
        info = [("Student ID", student["student_id"]), ("Name", student["student_name"]),
                ("Age", student["age"]),               ("Department", student["department"])]
        for i, (k, v) in enumerate(info):
            tk.Label(f, text=k+":", font=FONT_SMALL, fg=SUBTEXT,
                     bg=CARD).grid(row=i//2, column=(i%2)*2, sticky="w", padx=(0,8), pady=4)
            tk.Label(f, text=str(v), font=FONT_H3, fg=TEXT,
                     bg=CARD).grid(row=i//2, column=(i%2)*2+1, sticky="w", padx=(0,40), pady=4)

        if marks:
            tk.Frame(self._search_result_frame, bg=BORDER, height=1).pack(fill="x", padx=10)
            mf = tk.Frame(self._search_result_frame, bg=CARD, padx=24, pady=10)
            mf.pack(fill="x")
            tk.Label(mf, text="Marks", font=FONT_H3, fg=ACCENT1,
                     bg=CARD).grid(row=0, column=0, columnspan=10, sticky="w")
            subjects = ["PPS","AEP","ESE","ODVC","BEE"]
            for j, subj in enumerate(subjects):
                mark = marks[subj]
                col_bg = GREEN if mark >= 40 else RED
                tk.Label(mf, text=subj, font=FONT_SMALL, fg=SUBTEXT,
                         bg=CARD).grid(row=1, column=j*2, padx=(0,4), pady=4)
                tk.Label(mf, text=str(mark), font=FONT_H3, fg=col_bg,
                         bg=CARD).grid(row=1, column=j*2+1, padx=(0,20))

            if result:
                tk.Label(mf, text=f"Grade: {result['grade']}  ({result['percentage']}%)",
                         font=FONT_H3, fg=GREEN if result["grade"] != "FAIL" else RED,
                         bg=CARD).grid(row=2, column=0, columnspan=10, sticky="w", pady=4)

        att_pct = att["percentage"]
        af = tk.Frame(self._search_result_frame, bg=CARD, padx=24, pady=8)
        af.pack(fill="x")
        tk.Label(af, text=f"Attendance: {att_pct}%  ({att['present']}/{att['total']})",
                 font=FONT_H3, fg=GREEN if att_pct >= 75 else RED, bg=CARD).pack(anchor="w")

    # ══════════════════════════════════════════════════════════════
    # PAGE: UPDATE STUDENT
    # ══════════════════════════════════════════════════════════════
    def _page_update_student(self):
        wrap = card_frame(self.content, padx=40, pady=30)
        wrap.pack(pady=20, anchor="n", fill="x", padx=40)

        tk.Label(wrap, text="Update Student Record", font=FONT_H2,
                 fg=ACCENT1, bg=CARD).grid(row=0, column=0, columnspan=2,
                                            sticky="w", pady=(0,16))

        labels = ["Student ID", "New Name", "New Age", "New Department"]
        self._upd_entries = {}
        for i, lbl in enumerate(labels):
            tk.Label(wrap, text=lbl, font=FONT_SMALL, fg=SUBTEXT,
                     bg=CARD).grid(row=i+1, column=0, sticky="w",
                                   pady=6, padx=(0,20))
            e = entry_field(wrap, width=32)
            e.grid(row=i+1, column=1, sticky="ew", pady=6)
            self._upd_entries[lbl] = e

        self._upd_msg = tk.StringVar()
        tk.Label(wrap, textvariable=self._upd_msg, font=FONT_SMALL,
                 fg=GREEN, bg=CARD).grid(row=6, column=0, columnspan=2, pady=6)
        styled_btn(wrap, "  Update", self._do_update,
                   color=ACCENT1, width=20).grid(row=7, column=0,
                                                   columnspan=2, pady=10)

    def _do_update(self):
        try:
            sid  = int(self._upd_entries["Student ID"].get())
            name = self._upd_entries["New Name"].get().strip()
            age  = int(self._upd_entries["New Age"].get())
            dept = self._upd_entries["New Department"].get().strip()
            res  = api_put(f"/students/{sid}", {"student_name": name, "age": age, "department": dept})
            if res.get("success"):
                self._upd_msg.set("✅ Updated successfully!")
            else:
                self._upd_msg.set(f"❌ {res.get('message', res.get('error','Failed'))}")
        except Exception as ex:
            self._upd_msg.set(f"❌ {ex}")

    # ══════════════════════════════════════════════════════════════
    # PAGE: DELETE STUDENT
    # ══════════════════════════════════════════════════════════════
    def _page_delete_student(self):
        wrap = card_frame(self.content, padx=40, pady=30)
        wrap.pack(pady=20, anchor="n", fill="x", padx=40)

        tk.Label(wrap, text="Delete Student", font=FONT_H2,
                 fg=RED, bg=CARD).grid(row=0, column=0, columnspan=2,
                                        sticky="w", pady=(0,16))
        tk.Label(wrap, text="Student ID:", font=FONT_SMALL, fg=SUBTEXT,
                 bg=CARD).grid(row=1, column=0, sticky="w", padx=(0,20))
        self._del_id = entry_field(wrap, width=20)
        self._del_id.grid(row=1, column=1, sticky="ew", pady=6)

        self._del_msg = tk.StringVar()
        tk.Label(wrap, textvariable=self._del_msg, font=FONT_SMALL,
                 fg=RED, bg=CARD).grid(row=2, column=0, columnspan=2)
        styled_btn(wrap, "  Delete", self._do_delete,
                   color=RED, width=20).grid(row=3, column=0,
                                              columnspan=2, pady=10)

    def _do_delete(self):
        try:
            sid = int(self._del_id.get())
            if not messagebox.askyesno("Confirm", f"Delete student {sid}?"):
                return
            res = api_delete(f"/students/{sid}")
            if res.get("success"):
                self._del_msg.set("✅ Deleted successfully!")
                self._del_id.delete(0, "end")
            else:
                self._del_msg.set(f"❌ {res.get('message', res.get('error','Failed'))}")
        except Exception as ex:
            self._del_msg.set(f"❌ {ex}")

    # ══════════════════════════════════════════════════════════════
    # PAGE: ATTENDANCE
    # ══════════════════════════════════════════════════════════════
    def _page_attendance(self):
        nb = ttk.Notebook(self.content)
        nb.pack(fill="both", expand=True)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL,
                         foreground=SUBTEXT, padding=[14, 8],
                         font=("Segoe UI", 10))
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT2)],
                  foreground=[("selected", TEXT)])

        # Tab 1: Mark
        tab1 = tk.Frame(nb, bg=BG); nb.add(tab1, text="  Mark Attendance  ")
        self._att_mark_tab(tab1)

        # Tab 2: View
        tab2 = tk.Frame(nb, bg=BG); nb.add(tab2, text="  View Attendance  ")
        self._att_view_tab(tab2)

        # Tab 3: Report
        tab3 = tk.Frame(nb, bg=BG); nb.add(tab3, text="  Attendance Report  ")
        self._att_report_tab(tab3)

    def _att_mark_tab(self, parent):
        wrap = card_frame(parent, padx=40, pady=30)
        wrap.pack(pady=20, anchor="n", fill="x", padx=40)

        tk.Label(wrap, text="Mark Attendance", font=FONT_H2,
                 fg=ACCENT3, bg=CARD).grid(row=0, column=0, columnspan=2,
                                            sticky="w", pady=(0,14))

        self._att_fields = {}
        for i, lbl in enumerate(["Student ID", "Date (YYYY-MM-DD)"]):
            tk.Label(wrap, text=lbl, font=FONT_SMALL, fg=SUBTEXT,
                     bg=CARD).grid(row=i+1, column=0, sticky="w",
                                   padx=(0,20), pady=6)
            e = entry_field(wrap, width=28)
            e.grid(row=i+1, column=1, sticky="ew", pady=6)
            self._att_fields[lbl] = e

        tk.Label(wrap, text="Status", font=FONT_SMALL, fg=SUBTEXT,
                 bg=CARD).grid(row=3, column=0, sticky="w", padx=(0,20))
        self._att_status = tk.StringVar(value="Present")
        f_radio = tk.Frame(wrap, bg=CARD)
        f_radio.grid(row=3, column=1, sticky="w")
        for val in ["Present", "Absent"]:
            tk.Radiobutton(f_radio, text=val, variable=self._att_status,
                           value=val, font=FONT_BODY,
                           bg=CARD, fg=TEXT, selectcolor=ACCENT2,
                           activebackground=CARD).pack(side="left", padx=8)

        self._att_msg = tk.StringVar()
        tk.Label(wrap, textvariable=self._att_msg, font=FONT_SMALL,
                 fg=GREEN, bg=CARD).grid(row=4, column=0, columnspan=2, pady=6)
        styled_btn(wrap, "  Mark", self._do_mark_att,
                   color=GREEN, width=20).grid(row=5, column=0,
                                                columnspan=2, pady=10)

    def _do_mark_att(self):
        try:
            sid    = int(self._att_fields["Student ID"].get())
            date   = self._att_fields["Date (YYYY-MM-DD)"].get().strip()
            status = self._att_status.get().lower()
            res    = api_post("/attendance", {"student_id": sid, "attendance_date": date, "status": status})
            if res.get("success"):
                self._att_msg.set(f"✅ Attendance marked: {status}")
            else:
                self._att_msg.set(f"❌ {res.get('error', res.get('message','Failed'))}")
        except Exception as ex:
            self._att_msg.set(f"❌ {ex}")

    def _att_view_tab(self, parent):
        frame = card_frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        cols = ("ID", "Student ID", "Date", "Status")
        tv   = self._make_treeview(frame, cols, height=18)
        res = api_get("/attendance")
        if res.get("success"):
            for d in res["data"]:
                tag = "present" if d.get("status") == "present" else "absent"
                tv.insert("", "end", values=(d.get("id",""), d.get("student_id",""), d.get("attendance_date",""), d.get("status","")), tags=(tag,))
        tv.tag_configure("present", foreground=GREEN)
        tv.tag_configure("absent",  foreground=RED)
        tv.pack(fill="both", expand=True, padx=10, pady=10)

    def _att_report_tab(self, parent):
        top = card_frame(parent, padx=20, pady=14)
        top.pack(fill="x", padx=10, pady=10)
        tk.Label(top, text="Student ID:", font=FONT_BODY, fg=TEXT,
                 bg=CARD).pack(side="left")
        self._att_rep_id = entry_field(top, width=12)
        self._att_rep_id.pack(side="left", padx=10)
        styled_btn(top, "Generate", self._do_att_report,
                   color=ACCENT2, width=12).pack(side="left")

        self._att_rep_frame = card_frame(parent)
        self._att_rep_frame.pack(fill="both", expand=True, padx=10, pady=0)

    def _do_att_report(self):
        for w in self._att_rep_frame.winfo_children(): w.destroy()
        try:
            sid = int(self._att_rep_id.get())
            res = api_get(f"/attendance/report/{sid}")
            if not res.get("success"):
                tk.Label(self._att_rep_frame, text=f"❌ {res.get('error','Failed')}",
                         fg=RED, bg=CARD, font=FONT_BODY).pack(pady=10)
                return
            d       = res["data"]
            total   = d["total_classes"]
            present = d["present"]
            absent  = d["absent"]
            pct     = d["percentage"]
            color   = GREEN if pct >= 75 else RED

            if total == 0:
                tk.Label(self._att_rep_frame, text="No records found.",
                         fg=SUBTEXT, bg=CARD, font=FONT_BODY).pack(pady=20)
                return

            info_f = tk.Frame(self._att_rep_frame, bg=CARD, padx=30, pady=20)
            info_f.pack(side="left", fill="y")
            for lbl, val, col in [
                ("Student ID", str(sid), TEXT),
                ("Total Classes", str(total), TEXT),
                ("Present Days", str(present), GREEN),
                ("Absent Days",  str(absent),  RED),
                ("Attendance %", f"{pct}%",    color),
            ]:
                tk.Label(info_f, text=f"{lbl}:", font=FONT_SMALL,
                         fg=SUBTEXT, bg=CARD).pack(anchor="w", pady=2)
                tk.Label(info_f, text=val, font=FONT_H2,
                         fg=col, bg=CARD).pack(anchor="w", pady=(0,8))

            # pie
            pie_f = tk.Frame(self._att_rep_frame, bg=CARD)
            pie_f.pack(side="left", fill="both", expand=True)
            fig = Figure(figsize=(4, 3), facecolor=CARD)
            ax  = fig.add_subplot(111, facecolor=CARD)
            ax.pie([present, absent], labels=["Present","Absent"],
                   colors=[GREEN, RED], autopct="%1.1f%%", startangle=140,
                   wedgeprops=dict(width=0.6))
            fig.tight_layout()
            FigureCanvasTkAgg(fig, master=pie_f).get_tk_widget().pack(
                fill="both", expand=True, padx=10, pady=10)

        except Exception as ex:
            tk.Label(self._att_rep_frame, text=f"❌ {ex}",
                     fg=RED, bg=CARD, font=FONT_BODY).pack(pady=10)

    # ══════════════════════════════════════════════════════════════
    # PAGE: MARKS
    # ══════════════════════════════════════════════════════════════
    def _page_marks(self):
        nb = ttk.Notebook(self.content)
        nb.pack(fill="both", expand=True)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL,
                         foreground=SUBTEXT, padding=[14, 8],
                         font=("Segoe UI", 10))
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT1)],
                  foreground=[("selected", TEXT)])

        tabs = [
            ("  Add Marks  ",    self._marks_add_tab),
            ("  View Marks  ",   self._marks_view_tab),
            ("  Update Marks  ", self._marks_update_tab),
            ("  Result  ",       self._marks_result_tab),
        ]
        for title, fn in tabs:
            t = tk.Frame(nb, bg=BG)
            nb.add(t, text=title)
            fn(t)

    def _marks_form(self, parent, title, btn_text, btn_color, callback):
        wrap = card_frame(parent, padx=40, pady=30)
        wrap.pack(pady=20, anchor="n", fill="x", padx=40)
        tk.Label(wrap, text=title, font=FONT_H2, fg=btn_color,
                 bg=CARD).grid(row=0, column=0, columnspan=2,
                                sticky="w", pady=(0,14))
        entries = {}
        for i, lbl in enumerate(["Student ID","PPS","AEP","ESE","ODVC","BEE"]):
            tk.Label(wrap, text=lbl, font=FONT_SMALL, fg=SUBTEXT,
                     bg=CARD).grid(row=i+1, column=0, sticky="w",
                                   padx=(0,20), pady=5)
            e = entry_field(wrap, width=24)
            e.grid(row=i+1, column=1, sticky="ew", pady=5)
            entries[lbl] = e
        msg_var = tk.StringVar()
        tk.Label(wrap, textvariable=msg_var, font=FONT_SMALL,
                 fg=GREEN, bg=CARD).grid(row=8, column=0, columnspan=2, pady=6)
        styled_btn(wrap, f"  {btn_text}", lambda: callback(entries, msg_var),
                   color=btn_color, width=20).grid(row=9, column=0,
                                                    columnspan=2, pady=8)

    def _marks_add_tab(self, parent):
        def do(entries, msg):
            try:
                sid  = int(entries["Student ID"].get())
                vals = [int(entries[s].get()) for s in ["PPS","AEP","ESE","ODVC","BEE"]]
                res  = api_post("/marks", {"student_id": sid, "PPS": vals[0], "AEP": vals[1], "ESE": vals[2], "ODVC": vals[3], "BEE": vals[4]})
                if res.get("success"):
                    msg.set("✅ Marks added!")
                    for e in entries.values(): e.delete(0,"end")
                else:
                    msg.set(f"❌ {res.get('error', res.get('message','Failed'))}")
            except Exception as ex: msg.set(f"❌ {ex}")
        self._marks_form(parent, "Add Marks", "Add Marks", GREEN, do)

    def _marks_update_tab(self, parent):
        def do(entries, msg):
            try:
                sid  = int(entries["Student ID"].get())
                vals = [int(entries[s].get()) for s in ["PPS","AEP","ESE","ODVC","BEE"]]
                res  = api_put(f"/marks/{sid}", {"PPS": vals[0], "AEP": vals[1], "ESE": vals[2], "ODVC": vals[3], "BEE": vals[4]})
                if res.get("success"):
                    msg.set("✅ Marks updated!")
                else:
                    msg.set(f"❌ {res.get('error', res.get('message','Failed'))}")
            except Exception as ex: msg.set(f"❌ {ex}")
        self._marks_form(parent, "Update Marks", "Update", ACCENT1, do)

    def _marks_view_tab(self, parent):
        top = card_frame(parent, padx=20, pady=14)
        top.pack(fill="x", padx=10, pady=10)
        tk.Label(top, text="Student ID:", font=FONT_BODY, fg=TEXT,
                 bg=CARD).pack(side="left")
        sid_e = entry_field(top, width=12)
        sid_e.pack(side="left", padx=10)
        res_f = card_frame(parent)
        res_f.pack(fill="both", expand=True, padx=10)

        def do():
            for w in res_f.winfo_children(): w.destroy()
            try:
                sid = int(sid_e.get())
                res = api_get(f"/marks/{sid}")
                if not res.get("success"):
                    tk.Label(res_f, text="No records found.", fg=SUBTEXT,
                             bg=CARD, font=FONT_BODY).pack(pady=20)
                    return
                row      = res["data"]
                subjects = ["PPS","AEP","ESE","ODVC","BEE"]
                vals     = [row[s] for s in subjects]
                info_f   = tk.Frame(res_f, bg=CARD, padx=30, pady=20)
                info_f.pack(side="left", fill="y")
                for s, m in zip(subjects, vals):
                    col = GREEN if m >= 40 else RED
                    tk.Label(info_f, text=f"{s}:", font=FONT_SMALL,
                             fg=SUBTEXT, bg=CARD).pack(anchor="w")
                    tk.Label(info_f, text=str(m), font=FONT_H2,
                             fg=col, bg=CARD).pack(anchor="w", pady=(0,6))
                chart_f = tk.Frame(res_f, bg=CARD)
                chart_f.pack(side="left", fill="both", expand=True)
                fig = Figure(figsize=(5,3), facecolor=CARD)
                ax  = fig.add_subplot(111, facecolor=CARD)
                colors_b = [GREEN if m >= 40 else RED for m in vals]
                ax.bar(subjects, vals, color=colors_b, width=0.5)
                ax.set_ylim(0, 110); ax.set_facecolor(CARD)
                ax.tick_params(colors=SUBTEXT, labelsize=8)
                for spine in ax.spines.values(): spine.set_edgecolor(BORDER)
                fig.tight_layout()
                FigureCanvasTkAgg(fig, master=chart_f).get_tk_widget().pack(
                    fill="both", expand=True, padx=10, pady=10)
            except Exception as ex:
                tk.Label(res_f, text=f"❌ {ex}", fg=RED,
                         bg=CARD, font=FONT_BODY).pack(pady=10)

        styled_btn(top, "View", do, color=ACCENT3, width=10).pack(side="left")

    def _marks_result_tab(self, parent):
        top = card_frame(parent, padx=20, pady=14)
        top.pack(fill="x", padx=10, pady=10)
        tk.Label(top, text="Student ID:", font=FONT_BODY, fg=TEXT,
                 bg=CARD).pack(side="left")
        sid_e = entry_field(top, width=12)
        sid_e.pack(side="left", padx=8)
        tk.Label(top, text="Max Marks:", font=FONT_BODY, fg=TEXT,
                 bg=CARD).pack(side="left")
        max_e = entry_field(top, width=8)
        max_e.insert(0, "500")
        max_e.pack(side="left", padx=8)
        res_f = card_frame(parent)
        res_f.pack(fill="both", expand=True, padx=10)

        def do():
            for w in res_f.winfo_children(): w.destroy()
            try:
                sid = int(sid_e.get())
                mx  = int(max_e.get())
                res = api_get(f"/marks/result/{sid}", {"max_marks": mx})
                if not res.get("success"):
                    tk.Label(res_f, text="No marks found.", fg=SUBTEXT,
                             bg=CARD, font=FONT_BODY).pack(pady=20)
                    return
                d     = res["data"]
                total = d["total"]; pct = d["percentage"]; grade = d["grade"]
                gcol  = {
                    "A+": GREEN, "A": ACCENT3, "B": ACCENT1,
                    "C": "#f9c74f", "FAIL": RED
                }.get(grade, TEXT)
                rf = tk.Frame(res_f, bg=CARD, padx=40, pady=20)
                rf.pack(anchor="center", pady=20)
                for lbl, val, col in [
                    ("Student ID",  str(sid),        TEXT),
                    ("Total Marks", f"{total}/{mx}",  TEXT),
                    ("Percentage",  f"{pct}%",        gcol),
                    ("Grade",       grade,             gcol),
                ]:
                    tk.Label(rf, text=lbl, font=FONT_SMALL, fg=SUBTEXT,
                             bg=CARD).pack(anchor="w")
                    tk.Label(rf, text=val, font=("Segoe UI", 32, "bold"),
                             fg=col, bg=CARD).pack(anchor="w", pady=(0,12))
            except Exception as ex:
                tk.Label(res_f, text=f"❌ {ex}", fg=RED,
                         bg=CARD, font=FONT_BODY).pack(pady=10)

        styled_btn(top, "Generate", do, color=ACCENT2, width=12).pack(side="left")

    # ══════════════════════════════════════════════════════════════
    # PAGE: ANALYTICS
    # ══════════════════════════════════════════════════════════════
    def _page_analytics(self):
        nb = ttk.Notebook(self.content)
        nb.pack(fill="both", expand=True)
        style = ttk.Style()
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL,
                         foreground=SUBTEXT, padding=[14,8],
                         font=("Segoe UI",10))
        style.map("TNotebook.Tab",
                  background=[("selected", "#7b2ff7")],
                  foreground=[("selected", TEXT)])

        t1 = tk.Frame(nb, bg=BG); nb.add(t1, text="  Student Performance  ")
        t2 = tk.Frame(nb, bg=BG); nb.add(t2, text="  Subject Chart  ")
        t3 = tk.Frame(nb, bg=BG); nb.add(t3, text="  Attendance Pie  ")
        t4 = tk.Frame(nb, bg=BG); nb.add(t4, text="  Class Dashboard  ")

        self._analytics_performance(t1)
        self._analytics_subject_chart(t2)
        self._analytics_att_pie(t3)
        self._analytics_class_dashboard(t4)

    def _analytics_performance(self, parent):
        top = card_frame(parent, padx=20, pady=14)
        top.pack(fill="x", padx=10, pady=10)
        tk.Label(top, text="Student ID:", font=FONT_BODY, fg=TEXT,
                 bg=CARD).pack(side="left")
        sid_e = entry_field(top, width=12)
        sid_e.pack(side="left", padx=8)
        tk.Label(top, text="Max Marks:", font=FONT_BODY, fg=TEXT,
                 bg=CARD).pack(side="left")
        max_e = entry_field(top, width=8)
        max_e.insert(0,"500")
        max_e.pack(side="left", padx=8)
        res_f = card_frame(parent)
        res_f.pack(fill="both", expand=True, padx=10)

        def do():
            for w in res_f.winfo_children(): w.destroy()
            try:
                sid = int(sid_e.get()); mx = int(max_e.get())
                res = api_get(f"/analytics/student/{sid}")
                if not res.get("success"):
                    tk.Label(res_f, text="No record.", fg=SUBTEXT,
                             bg=CARD, font=FONT_BODY).pack(pady=20); return
                d     = res["data"]
                marks = d["marks"]
                result= d["result"]
                subjects = ["PPS","AEP","ESE","ODVC","BEE"]
                if not marks:
                    tk.Label(res_f, text="No marks.", fg=SUBTEXT, bg=CARD, font=FONT_BODY).pack(pady=20); return
                vals  = [marks[s] for s in subjects]
                total = sum(vals); pct = round(total/mx*100,2)
                if pct>=90: grade,gcol="A+",GREEN
                elif pct>=75: grade,gcol="A",ACCENT3
                elif pct>=60: grade,gcol="B",ACCENT1
                elif pct>=40: grade,gcol="C","#f9c74f"
                else: grade,gcol="FAIL",RED

                left = tk.Frame(res_f, bg=CARD, padx=24, pady=20)
                left.pack(side="left", fill="y")
                for s, m in zip(subjects, vals):
                    col = GREEN if m>=40 else RED
                    tk.Label(left, text=s+":", font=FONT_SMALL, fg=SUBTEXT, bg=CARD).pack(anchor="w")
                    tk.Label(left, text=str(m), font=FONT_H2, fg=col, bg=CARD).pack(anchor="w", pady=(0,4))
                tk.Frame(left,bg=BORDER,height=1).pack(fill="x",pady=6)
                tk.Label(left,text="Total:",font=FONT_SMALL,fg=SUBTEXT,bg=CARD).pack(anchor="w")
                tk.Label(left,text=f"{total}/{mx}",font=FONT_H2,fg=TEXT,bg=CARD).pack(anchor="w")
                tk.Label(left,text="Grade:",font=FONT_SMALL,fg=SUBTEXT,bg=CARD).pack(anchor="w",pady=(8,0))
                tk.Label(left,text=grade,font=("Segoe UI",36,"bold"),fg=gcol,bg=CARD).pack(anchor="w")

                right = tk.Frame(res_f, bg=CARD)
                right.pack(side="left", fill="both", expand=True)
                fig = Figure(figsize=(5,3.5), facecolor=CARD)
                ax  = fig.add_subplot(111, facecolor=CARD)
                colors_b = [GREEN if v>=40 else RED for v in vals]
                ax.barh(subjects, vals, color=colors_b, height=0.5)
                ax.set_xlim(0,110)
                ax.axvline(40, color=ACCENT1, linestyle="--", alpha=0.7, linewidth=1)
                ax.set_facecolor(CARD)
                ax.tick_params(colors=SUBTEXT, labelsize=8)
                for spine in ax.spines.values(): spine.set_edgecolor(BORDER)
                for i, v in enumerate(vals):
                    ax.text(v+1, i, str(v), va="center", color=TEXT, fontsize=8)
                fig.tight_layout()
                FigureCanvasTkAgg(fig, master=right).get_tk_widget().pack(
                    fill="both", expand=True, padx=10, pady=10)
            except Exception as ex:
                tk.Label(res_f,text=f"❌ {ex}",fg=RED,bg=CARD,font=FONT_BODY).pack(pady=10)

        styled_btn(top,"Generate",do,color=ACCENT2,width=12).pack(side="left")

    def _analytics_subject_chart(self, parent):
        top = card_frame(parent, padx=20, pady=14)
        top.pack(fill="x", padx=10, pady=10)
        tk.Label(top, text="Student ID:", font=FONT_BODY, fg=TEXT,
                 bg=CARD).pack(side="left")
        sid_e = entry_field(top, width=12)
        sid_e.pack(side="left", padx=8)
        chart_f = card_frame(parent)
        chart_f.pack(fill="both", expand=True, padx=10)

        def do():
            for w in chart_f.winfo_children(): w.destroy()
            try:
                sid  = int(sid_e.get())
                res  = api_get(f"/marks/{sid}")
                if not res.get("success"):
                    tk.Label(chart_f, text="No marks.", fg=SUBTEXT,
                             bg=CARD, font=FONT_BODY).pack(pady=20); return
                subjects = ["PPS","AEP","ESE","ODVC","BEE"]
                row      = res["data"]
                marks    = [row[s] for s in subjects]
                colors_b = [ACCENT2, ACCENT1, GREEN, ACCENT3, "#f72585"]
                fig = Figure(figsize=(7,4), facecolor=CARD)
                ax  = fig.add_subplot(111, facecolor=CARD)
                bars = ax.bar(subjects, marks, color=colors_b, width=0.55, zorder=3)
                ax.set_ylim(0,110)
                ax.set_title(f"Subject-wise Marks — Student {sid}",
                             color=TEXT, fontsize=11, pad=10)
                ax.set_ylabel("Marks", color=SUBTEXT, fontsize=9)
                ax.tick_params(colors=SUBTEXT, labelsize=9)
                for spine in ax.spines.values(): spine.set_edgecolor(BORDER)
                ax.yaxis.grid(True, color=BORDER, linestyle="--", alpha=0.5, zorder=0)
                for b, v in zip(bars, marks):
                    ax.text(b.get_x()+b.get_width()/2, v+1, str(v),
                            ha="center", va="bottom", color=TEXT, fontsize=9)
                fig.tight_layout()
                FigureCanvasTkAgg(fig, master=chart_f).get_tk_widget().pack(
                    fill="both", expand=True, padx=10, pady=10)
            except Exception as ex:
                tk.Label(chart_f, text=f"❌ {ex}", fg=RED,
                         bg=CARD, font=FONT_BODY).pack(pady=10)

        styled_btn(top,"Show Chart",do,color=ACCENT1,width=12).pack(side="left")

    def _analytics_att_pie(self, parent):
        top = card_frame(parent, padx=20, pady=14)
        top.pack(fill="x", padx=10, pady=10)
        tk.Label(top, text="Student ID:", font=FONT_BODY, fg=TEXT,
                 bg=CARD).pack(side="left")
        sid_e = entry_field(top, width=12)
        sid_e.pack(side="left", padx=8)
        chart_f = card_frame(parent)
        chart_f.pack(fill="both", expand=True, padx=10)

        def do():
            for w in chart_f.winfo_children(): w.destroy()
            try:
                sid = int(sid_e.get())
                res = api_get(f"/attendance/report/{sid}")
                if not res.get("success"):
                    tk.Label(chart_f, text="No attendance records.",
                             fg=SUBTEXT, bg=CARD, font=FONT_BODY).pack(pady=20); return
                d       = res["data"]
                present = d["present"]
                absent  = d["absent"]
                if present+absent == 0:
                    tk.Label(chart_f, text="No attendance records.",
                             fg=SUBTEXT, bg=CARD, font=FONT_BODY).pack(pady=20); return
                fig = Figure(figsize=(5,4), facecolor=CARD)
                ax  = fig.add_subplot(111, facecolor=CARD)
                ax.pie([present, absent], labels=["Present","Absent"],
                       colors=[GREEN, RED], autopct="%1.1f%%", startangle=140,
                       wedgeprops=dict(width=0.6))
                ax.set_title(f"Attendance — Student {sid}", color=TEXT, fontsize=11)
                fig.tight_layout()
                FigureCanvasTkAgg(fig, master=chart_f).get_tk_widget().pack(
                    fill="both", expand=True, padx=10, pady=10)
            except Exception as ex:
                tk.Label(chart_f, text=f"❌ {ex}", fg=RED,
                         bg=CARD, font=FONT_BODY).pack(pady=10)

        styled_btn(top,"Show Chart",do,color=GREEN,width=12).pack(side="left")

    def _analytics_class_dashboard(self, parent):
        res = api_get("/analytics/class-dashboard")
        if res.get("success"):
            d    = res["data"]
            total = d["total_students"]
            avg   = d["avg_marks"]
            high  = d["highest_marks"]
            low   = d["lowest_marks"]
            top5_raw = d["top5_students"]
            top5  = [(r["student_id"], r["total"]) for r in top5_raw]
        else:
            total=avg=high=low=0; top5=[]

        wrap = tk.Frame(parent, bg=BG)
        wrap.pack(fill="both", expand=True)

        stat_row = tk.Frame(wrap, bg=BG)
        stat_row.pack(fill="x", padx=10, pady=10)
        for icon, title, val, col in [
            ("👥","Total Students",str(total),ACCENT2),
            ("📊","Avg Total Marks",str(avg),ACCENT1),
            ("🏆","Highest Total",str(high),GREEN),
            ("📉","Lowest Total",str(low),RED),
        ]:
            c = tk.Frame(stat_row, bg=CARD, bd=0,
                         highlightbackground=col, highlightthickness=2)
            c.pack(side="left", fill="both", expand=True, padx=6)
            tk.Frame(c, bg=col, height=3).pack(fill="x")
            inner = tk.Frame(c, bg=CARD, padx=16, pady=14)
            inner.pack()
            tk.Label(inner, text=icon, font=("Segoe UI Emoji",22),
                     bg=CARD, fg=col).pack()
            tk.Label(inner, text=val, font=("Segoe UI",26,"bold"),
                     bg=CARD, fg=TEXT).pack()
            tk.Label(inner, text=title, font=FONT_SMALL,
                     bg=CARD, fg=SUBTEXT).pack()

        if top5:
            lf = card_frame(wrap)
            lf.pack(fill="x", padx=10, pady=4)
            tk.Label(lf, text="Top 5 Students", font=FONT_H3,
                     fg=TEXT, bg=CARD).pack(anchor="w", padx=12, pady=(10,4))
            cols = ("Student ID","Total Marks")
            tv   = self._make_treeview(lf, cols, height=5)
            for row in top5:
                tv.insert("","end",values=row)
            tv.pack(fill="x", padx=12, pady=(0,10))

    # ── TREEVIEW helper ─────────────────────────────────────────────
    def _make_treeview(self, parent, columns, height=8):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=28,
                        font=("Segoe UI", 10),
                        borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                        background=ACCENT2, foreground=TEXT,
                        font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", ACCENT2)],
                  foreground=[("selected", TEXT)])

        tv = ttk.Treeview(parent, columns=columns, show="headings",
                          height=height, style="Custom.Treeview")
        for col in columns:
            tv.heading(col, text=col)
            tv.column(col, width=140, anchor="center")

        sb = ttk.Scrollbar(parent, orient="vertical", command=tv.yview)
        tv.configure(yscroll=sb.set)
        return tv

# ─── MAIN ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()