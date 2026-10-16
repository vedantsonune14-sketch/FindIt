import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Dict, Optional

import database
from matcher import rank_matches
from sample_data import load_sample_data

NAVY = "#14213D"
TEAL = "#0F766E"
LIGHT = "#F4F7FA"
WHITE = "#FFFFFF"
TEXT = "#172033"
MUTED = "#667085"
BORDER = "#D9E1EA"
GREEN = "#15803D"
AMBER = "#B45309"
RED = "#B91C1C"

CATEGORIES = [
    "Electronics", "Stationery", "Bags", "Documents",
    "Accessories", "Keys", "Clothing", "Other"
]


class FindItApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FindIt — Smart Lost-and-Found Matcher")
        self.geometry("1180x720")
        self.minsize(1000, 650)
        self.configure(bg=LIGHT)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=LIGHT)
        self.style.configure("Card.TFrame", background=WHITE)
        self.style.configure("TLabel", background=LIGHT, foreground=TEXT, font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", background=LIGHT, foreground=NAVY, font=("Segoe UI", 22, "bold"))
        self.style.configure("Subtitle.TLabel", background=LIGHT, foreground=MUTED, font=("Segoe UI", 10))
        self.style.configure("CardTitle.TLabel", background=WHITE, foreground=MUTED, font=("Segoe UI", 9, "bold"))
        self.style.configure("CardValue.TLabel", background=WHITE, foreground=NAVY, font=("Segoe UI", 22, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8))
        self.style.configure("Primary.TButton", background=TEAL, foreground=WHITE)
        self.style.map("Primary.TButton", background=[("active", "#0B5E59")])
        self.style.configure("Treeview", rowheight=30, font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        self.current_lost_id: Optional[int] = None
        self.build_shell()
        self.show_dashboard()

    def build_shell(self):
        self.sidebar = tk.Frame(self, bg=NAVY, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar, text="FIND", bg=NAVY, fg="#66D9C9",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=24, pady=(28, 0))
        tk.Label(
            self.sidebar, text="IT", bg=NAVY, fg=WHITE,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=24)
        tk.Label(
            self.sidebar, text="Smart Lost-and-Found", bg=NAVY, fg="#B8C4D6",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=24, pady=(0, 28))

        self.nav_button("Dashboard", self.show_dashboard)
        self.nav_button("Report Lost Item", lambda: self.show_report_form("lost"))
        self.nav_button("Report Found Item", lambda: self.show_report_form("found"))
        self.nav_button("Manage Reports", self.show_reports)
        self.nav_button("Load Demo Data", self.load_demo)
        self.nav_button("About / DSA", self.show_about)

        tk.Label(
            self.sidebar,
            text="Local desktop application\nSQLite • Tkinter • Python",
            bg=NAVY, fg="#8492A8", justify="left",
            font=("Segoe UI", 8)
        ).pack(side="bottom", anchor="w", padx=24, pady=24)

        self.main = tk.Frame(self, bg=LIGHT)
        self.main.pack(side="left", fill="both", expand=True)

    def nav_button(self, text, command):
        btn = tk.Button(
            self.sidebar, text=text, command=command, anchor="w",
            bg=NAVY, fg=WHITE, activebackground="#21355D",
            activeforeground=WHITE, relief="flat", bd=0,
            font=("Segoe UI", 10, "bold"), padx=24, pady=12
        )
        btn.pack(fill="x")

    def clear_main(self):
        for child in self.main.winfo_children():
            child.destroy()

    def page_header(self, title, subtitle=""):
        frame = tk.Frame(self.main, bg=LIGHT)
        frame.pack(fill="x", padx=30, pady=(26, 18))
        tk.Label(frame, text=title, bg=LIGHT, fg=NAVY,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(frame, text=subtitle, bg=LIGHT, fg=MUTED,
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))
        return frame

    def show_dashboard(self):
        self.clear_main()
        self.page_header(
            "Dashboard",
            "A local, privacy-conscious way to connect lost and found reports."
        )

        stats = database.dashboard_stats()
        cards = tk.Frame(self.main, bg=LIGHT)
        cards.pack(fill="x", padx=30)

        card_data = [
            ("Lost reports", stats["lost"]),
            ("Found reports", stats["found"]),
            ("Active reports", stats["active"]),
            ("Reunited", stats["reunited"]),
        ]
        for title, value in card_data:
            card = tk.Frame(cards, bg=WHITE, highlightbackground=BORDER,
                            highlightthickness=1)
            card.pack(side="left", fill="x", expand=True, padx=(0, 12))
            tk.Label(card, text=title.upper(), bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=18, pady=(16, 3))
            tk.Label(card, text=str(value), bg=WHITE, fg=NAVY,
                     font=("Segoe UI", 23, "bold")).pack(anchor="w", padx=18, pady=(0, 16))

        actions = tk.Frame(self.main, bg=LIGHT)
        actions.pack(fill="x", padx=30, pady=24)
        ttk.Button(actions, text="＋ Report Lost Item",
                   style="Primary.TButton",
                   command=lambda: self.show_report_form("lost")).pack(side="left", padx=(0, 10))
        ttk.Button(actions, text="＋ Report Found Item",
                   style="Primary.TButton",
                   command=lambda: self.show_report_form("found")).pack(side="left")

        recent_box = tk.Frame(self.main, bg=WHITE, highlightbackground=BORDER,
                              highlightthickness=1)
        recent_box.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        tk.Label(recent_box, text="Recent Reports", bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(15, 8))

        reports = database.get_reports()
        if not reports:
            tk.Label(
                recent_box,
                text="No reports yet.\nUse the buttons above or load demo data to explore FindIt.",
                bg=WHITE, fg=MUTED, justify="left",
                font=("Segoe UI", 10)
            ).pack(anchor="w", padx=18, pady=25)
            return

        tree = self.make_tree(recent_box, [
            ("id", "ID", 60), ("report_type", "Type", 80),
            ("item_name", "Item", 190), ("category", "Category", 120),
            ("location", "Location", 170), ("status", "Status", 100)
        ])
        for r in reports[:8]:
            tree.insert("", "end", values=(
                r["id"], r["report_type"].title(), r["item_name"],
                r["category"], r["location"], r["status"]
            ))

    def make_tree(self, parent, columns):
        holder = tk.Frame(parent, bg=parent.cget("bg"))
        holder.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        col_ids = [c[0] for c in columns]
        tree = ttk.Treeview(holder, columns=col_ids, show="headings")
        for cid, heading, width in columns:
            tree.heading(cid, text=heading)
            tree.column(cid, width=width, anchor="w")
        y = ttk.Scrollbar(holder, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=y.set)
        tree.pack(side="left", fill="both", expand=True)
        y.pack(side="right", fill="y")
        return tree

    def show_report_form(self, report_type, existing=None):
        self.clear_main()
        title = "Report a Lost Item" if report_type == "lost" else "Report a Found Item"
        subtitle = "Enter the details below. Contact information is optional and stored locally."
        self.page_header(title, subtitle)

        outer = tk.Frame(self.main, bg=WHITE, highlightbackground=BORDER,
                         highlightthickness=1)
        outer.pack(fill="both", expand=True, padx=30, pady=(0, 25))

        form = tk.Frame(outer, bg=WHITE)
        form.pack(fill="both", expand=True, padx=28, pady=22)

        vars_ = {}
        fields = [
            ("item_name", "Item name *"),
            ("category", "Category *"),
            ("color", "Color"),
            ("location", "Last-seen location *" if report_type == "lost" else "Found location *"),
            ("report_date", "Date lost *" if report_type == "lost" else "Date found *"),
            ("reporter_name", "Reporter / Finder name *"),
        ]

        for row, (key, label) in enumerate(fields):
            tk.Label(form, text=label, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", padx=(0, 20), pady=8)
            if key == "category":
                var = tk.StringVar(value=existing.get(key, "") if existing else "")
                widget = ttk.Combobox(form, textvariable=var, values=CATEGORIES, state="readonly", width=42)
            else:
                var = tk.StringVar(value=existing.get(key, "") if existing else "")
                widget = ttk.Entry(form, textvariable=var, width=45)
            widget.grid(row=row, column=1, sticky="w", pady=8)
            vars_[key] = var

        next_row = len(fields)
        tk.Label(form, text="Description", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 9, "bold")).grid(row=next_row, column=0, sticky="nw", pady=8)
        desc = tk.Text(form, width=43, height=5, font=("Segoe UI", 10),
                       relief="solid", bd=1, highlightthickness=0)
        desc.grid(row=next_row, column=1, sticky="w", pady=8)
        if existing:
            desc.insert("1.0", existing.get("description", ""))

        row = next_row + 1
        tk.Label(form, text="Contact type", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", pady=8)
        contact_type = tk.StringVar(value=existing.get("contact_type", "") if existing else "")
        contact_box = ttk.Combobox(form, textvariable=contact_type,
                                    values=["", "email", "phone"], state="readonly", width=42)
        contact_box.grid(row=row, column=1, sticky="w", pady=8)

        row += 1
        tk.Label(form, text="Contact information", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", pady=8)
        contact_info = tk.StringVar(value=existing.get("contact_info", "") if existing else "")
        ttk.Entry(form, textvariable=contact_info, width=45).grid(row=row, column=1, sticky="w", pady=8)

        hint = "Required fields are marked *. Date format: YYYY-MM-DD."
        tk.Label(form, text=hint, bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 8)).grid(row=row + 1, column=1, sticky="w", pady=(0, 12))

        def save():
            data = {
                "report_type": report_type,
                "item_name": vars_["item_name"].get().strip(),
                "category": vars_["category"].get().strip(),
                "color": vars_["color"].get().strip(),
                "location": vars_["location"].get().strip(),
                "report_date": vars_["report_date"].get().strip(),
                "description": desc.get("1.0", "end").strip(),
                "reporter_name": vars_["reporter_name"].get().strip(),
                "contact_type": contact_type.get().strip(),
                "contact_info": contact_info.get().strip(),
                "status": existing.get("status", "Active") if existing else "Active",
            }

            required = {
                "Item name": data["item_name"],
                "Category": data["category"],
                "Location": data["location"],
                "Date": data["report_date"],
                "Reporter / Finder name": data["reporter_name"],
            }
            missing = [name for name, value in required.items() if not value]
            if missing:
                messagebox.showerror("Missing information",
                                     "Please fill in: " + ", ".join(missing))
                return

            try:
                datetime.strptime(data["report_date"], "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid date",
                                     "Please use the date format YYYY-MM-DD.")
                return

            if data["contact_info"] and data["contact_type"] == "":
                messagebox.showerror("Contact type required",
                                     "Select email or phone when contact information is provided.")
                return

            if data["contact_type"] == "email" and data["contact_info"]:
                if "@" not in data["contact_info"]:
                    messagebox.showerror("Invalid email", "Please enter a valid email address.")
                    return

            if existing:
                database.update_report(existing["id"], data)
                messagebox.showinfo("Updated", "Report updated successfully.")
            else:
                new_id = database.add_report(data)
                messagebox.showinfo("Saved", f"Report #{new_id} saved successfully.")
            self.show_reports()

        buttons = tk.Frame(form, bg=WHITE)
        buttons.grid(row=row + 2, column=1, sticky="w", pady=10)
        ttk.Button(buttons, text="Save Report", style="Primary.TButton",
                   command=save).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Cancel",
                   command=self.show_reports).pack(side="left")

    def show_reports(self):
        self.clear_main()
        self.page_header("Manage Reports",
                         "Search, filter, edit, delete, reunite, or match active reports.")

        controls = tk.Frame(self.main, bg=LIGHT)
        controls.pack(fill="x", padx=30, pady=(0, 12))

        search_var = tk.StringVar()
        type_var = tk.StringVar(value="All")
        category_var = tk.StringVar(value="All")
        status_var = tk.StringVar(value="All")

        tk.Label(controls, text="Search", bg=LIGHT, fg=TEXT).pack(side="left")
        ttk.Entry(controls, textvariable=search_var, width=22).pack(side="left", padx=6)
        ttk.Combobox(controls, textvariable=type_var,
                     values=["All", "Lost", "Found"], state="readonly", width=9).pack(side="left", padx=5)
        ttk.Combobox(controls, textvariable=category_var,
                     values=["All"] + CATEGORIES, state="readonly", width=15).pack(side="left", padx=5)
        ttk.Combobox(controls, textvariable=status_var,
                     values=["All", "Active", "Reunited", "Closed"], state="readonly", width=12).pack(side="left", padx=5)

        holder = tk.Frame(self.main, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        holder.pack(fill="both", expand=True, padx=30, pady=(0, 25))

        tree = self.make_tree(holder, [
            ("id", "ID", 55), ("report_type", "Type", 75),
            ("item_name", "Item", 170), ("category", "Category", 110),
            ("color", "Color", 90), ("location", "Location", 150),
            ("report_date", "Date", 95), ("status", "Status", 90)
        ])

        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            selected_type = type_var.get().lower()
            if selected_type == "all":
                selected_type = None
            reports = database.get_reports(
                report_type=selected_type,
                search=search_var.get(),
                category=category_var.get(),
                status=status_var.get(),
            )
            for r in reports:
                tree.insert("", "end", iid=str(r["id"]), values=(
                    r["id"], r["report_type"].title(), r["item_name"],
                    r["category"], r["color"], r["location"],
                    r["report_date"], r["status"]
                ))

        refresh()

        buttons = tk.Frame(holder, bg=WHITE)
        buttons.pack(fill="x", padx=15, pady=(0, 15))

        def selected_report():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select a report", "Please select a report first.")
                return None
            return database.get_report(int(selected[0]))

        def edit():
            r = selected_report()
            if r:
                self.show_report_form(r["report_type"], r)

        def delete():
            r = selected_report()
            if not r:
                return
            if messagebox.askyesno("Confirm delete",
                                   f"Delete report #{r['id']}? This cannot be undone."):
                database.delete_report(r["id"])
                refresh()
                self.show_dashboard()

        def reunite():
            r = selected_report()
            if not r:
                return
            if r["status"] == "Reunited":
                messagebox.showinfo("Already reunited", "This report is already marked as reunited.")
                return
            if messagebox.askyesno(
                "Mark as reunited",
                "Mark this report as reunited?\n\n"
                "Only do this after verifying ownership and the return of the item."
            ):
                database.set_status(r["id"], "Reunited")
                refresh()
                self.show_dashboard()

        def details():
            r = selected_report()
            if r:
                self.show_report_details(r)

        def match():
            r = selected_report()
            if not r:
                return
            if r["report_type"] != "lost":
                messagebox.showinfo("Match a lost report",
                                    "Select a lost report to find possible found-item matches.")
                return
            if r["status"] != "Active":
                messagebox.showinfo("Inactive report",
                                    "Only active lost reports can be matched.")
                return
            self.show_match_results(r)

        for text, cmd in [
            ("View Details", details), ("Edit", edit), ("Delete", delete),
            ("Mark Reunited", reunite), ("Find Matches", match)
        ]:
            ttk.Button(buttons, text=text, command=cmd).pack(side="left", padx=(0, 7))

        search_var.trace_add("write", lambda *_: refresh())
        type_var.trace_add("write", lambda *_: refresh())
        category_var.trace_add("write", lambda *_: refresh())
        status_var.trace_add("write", lambda *_: refresh())

    def show_report_details(self, report):
        win = tk.Toplevel(self)
        win.title(f"Report #{report['id']}")
        win.geometry("520x590")
        win.configure(bg=WHITE)

        tk.Label(win, text=f"Report #{report['id']}", bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=25, pady=(22, 2))
        tk.Label(win, text=report["report_type"].title() + " report",
                 bg=WHITE, fg=TEAL, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=25)

        details = [
            ("Item", report["item_name"]),
            ("Category", report["category"]),
            ("Color", report["color"] or "Not provided"),
            ("Location", report["location"]),
            ("Date", report["report_date"]),
            ("Description", report["description"] or "Not provided"),
            ("Reporter", report["reporter_name"]),
            ("Status", report["status"]),
        ]
        box = tk.Frame(win, bg=WHITE)
        box.pack(fill="both", expand=True, padx=25, pady=20)
        for label, value in details:
            tk.Label(box, text=label, bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(7, 0))
            tk.Label(box, text=value, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 10), wraplength=450,
                     justify="left").pack(anchor="w")

        ttk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 20))

    def show_match_results(self, lost_report):
        self.clear_main()
        self.page_header(
            f"Matches for Lost Report #{lost_report['id']}",
            f"{lost_report['item_name']} • Results are heuristic suggestions, not proof of ownership."
        )

        found_reports = database.get_active_found_reports()
        results = rank_matches(lost_report, found_reports)

        if not results:
            tk.Label(
                self.main,
                text="No active found reports are available yet.\nTry again after a found-item report is added.",
                bg=LIGHT, fg=MUTED, justify="left",
                font=("Segoe UI", 11)
            ).pack(anchor="w", padx=30, pady=25)
            ttk.Button(self.main, text="Back to Reports",
                       command=self.show_reports).pack(anchor="w", padx=30)
            return

        top = tk.Frame(self.main, bg=LIGHT)
        top.pack(fill="x", padx=30, pady=(0, 10))
        tk.Label(top, text="Sorted by highest score", bg=LIGHT, fg=MUTED,
                 font=("Segoe UI", 9)).pack(side="left")

        box = tk.Frame(self.main, bg=WHITE, highlightbackground=BORDER,
                       highlightthickness=1)
        box.pack(fill="both", expand=True, padx=30, pady=(0, 25))

        tree = self.make_tree(box, [
            ("id", "Found ID", 70), ("item", "Item", 160),
            ("category", "Category", 110), ("color", "Color", 85),
            ("location", "Location", 150), ("date", "Date", 90),
            ("score", "Score", 70), ("strength", "Strength", 160)
        ])

        result_map = {}
        for i, result in enumerate(results):
            r = result["report"]
            iid = str(r["id"])
            result_map[iid] = result
            tree.insert("", "end", iid=iid, values=(
                r["id"], r["item_name"], r["category"], r["color"],
                r["location"], r["report_date"],
                f"{result['score']:.1f}/100", result["strength"]
            ))

        bottom = tk.Frame(box, bg=WHITE)
        bottom.pack(fill="x", padx=15, pady=(0, 15))

        def chosen_result():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select a match", "Select a candidate first.")
                return None
            return result_map[selected[0]]

        def show_explanation():
            result = chosen_result()
            if not result:
                return
            text = (
                f"Match score: {result['score']:.1f}/100\n"
                f"Strength: {result['strength']}\n\n"
                "Why this candidate was ranked here:\n• "
                + "\n• ".join(result["reasons"])
                + "\n\n"
                "The score is a heuristic ranking. It does not prove ownership."
            )
            messagebox.showinfo("Match explanation", text)

        def contact():
            result = chosen_result()
            if not result:
                return
            self.show_contact(result["report"])

        def details():
            result = chosen_result()
            if result:
                self.show_report_details(result["report"])

        ttk.Button(bottom, text="Explain Match", command=show_explanation).pack(side="left", padx=(0, 7))
        ttk.Button(bottom, text="View Contact", command=contact).pack(side="left", padx=(0, 7))
        ttk.Button(bottom, text="View Full Report", command=details).pack(side="left")

        note = tk.Label(
            self.main,
            text="Verify ownership using a private identifying feature before returning an item.",
            bg=LIGHT, fg=AMBER, font=("Segoe UI", 9, "bold")
        )
        note.pack(anchor="w", padx=30, pady=(0, 8))

        ttk.Button(self.main, text="Back to Reports",
                   command=self.show_reports).pack(anchor="w", padx=30, pady=(0, 20))

    def show_contact(self, report):
        win = tk.Toplevel(self)
        win.title("View Contact")
        win.geometry("420x300")
        win.configure(bg=WHITE)

        tk.Label(win, text="Reporter Contact", bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 17, "bold")).pack(anchor="w", padx=25, pady=(22, 6))
        tk.Label(win, text="Contact details are supplied by the reporter and may not be verified.",
                 bg=WHITE, fg=MUTED, wraplength=360, justify="left",
                 font=("Segoe UI", 9)).pack(anchor="w", padx=25)

        body = tk.Frame(win, bg=WHITE)
        body.pack(fill="both", expand=True, padx=25, pady=18)

        tk.Label(body, text="Name", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(body, text=report["reporter_name"], bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 10))

        contact = report.get("contact_info", "")
        ctype = report.get("contact_type", "")
        if contact:
            tk.Label(body, text=ctype.title(), bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w")
            tk.Label(body, text=contact, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 11)).pack(anchor="w")
        else:
            tk.Label(body, text="No contact information was provided.",
                     bg=WHITE, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w")

        tk.Label(
            body,
            text="Verify ownership before handing over the item.",
            bg=WHITE, fg=AMBER, wraplength=360,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=18)

        ttk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 20))

    def load_demo(self):
        count = load_sample_data()
        messagebox.showinfo(
            "Demo data",
            f"{count} new demonstration report(s) loaded.\n"
            "Running this again will not duplicate the same demo records."
        )
        self.show_dashboard()

    def show_about(self):
        self.clear_main()
        self.page_header("About FindIt / DSA",
                         "The mini-project demonstrates practical data structures and algorithms.")
        text = (
            "FindIt ranks possible lost/found matches using a weighted heuristic.\n\n"
            "DSA concepts:\n"
            "• Dictionaries / hash-map style lookups: reports are retrieved efficiently by ID.\n"
            "• Sets: description keywords are converted to sets and compared using intersection.\n"
            "• Sorting: candidate matches are sorted by descending score.\n"
            "• String similarity: difflib.SequenceMatcher handles slightly different item names.\n"
            "• Scoring: category, name, color, location and description contribute weighted points.\n\n"
            "Important: a high score is only a possible match. It is not proof of ownership.\n"
            "This is a local single-computer demonstration and has no authentication or network sync."
        )
        tk.Label(
            self.main, text=text, bg=WHITE, fg=TEXT, justify="left",
            wraplength=800, font=("Segoe UI", 11), padx=25, pady=25
        ).pack(anchor="w", padx=30, pady=10)


if __name__ == "__main__":
    database.init_db()
    FindItApp().mainloop()
