import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1100x750")
        self.root.configure(bg="#08080c")
        self.books = {}
        self.issued_books = {}
        self.FINE_RATE_PER_WEEK = 10
        famous_books = {
            "B001": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "quantity": 3, "total_copies": 3},
            "B002": {"title": "To Kill a Mockingbird", "author": "Harper Lee", "quantity": 4, "total_copies": 4},
            "B003": {"title": "1984", "author": "George Orwell", "quantity": 5, "total_copies": 5},
            "B004": {"title": "Pride and Prejudice", "author": "Jane Austen", "quantity": 3, "total_copies": 3},
            "B005": {"title": "The Hobbit", "author": "J.R.R. Tolkien", "quantity": 2, "total_copies": 2},
            "B006": {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "quantity": 6, "total_copies": 6},
            "B007": {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "quantity": 3, "total_copies": 3},
            "B008": {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "quantity": 4, "total_copies": 4},
            "B009": {"title": "Animal Farm", "author": "George Orwell", "quantity": 5, "total_copies": 5},
            "B010": {"title": "Brave New World", "author": "Aldous Huxley", "quantity": 2, "total_copies": 2},
        }
        for bid, info in famous_books.items():
            self.books[bid] = info
        self.style_ui()
        self.create_widgets()

    def style_ui(self):
        self.c = {"bg": "#08080c", "sidebar": "#0e0e14", "panel": "#14141c", "card": "#1a1a24", "accent": "#6366f1", "success": "#22c55e", "warning": "#f59e0b", "danger": "#ef4444", "fg": "#fafafa", "fg_sec": "#a1a1aa", "fg_mt": "#71717a"}

    def create_widgets(self):
        self.create_sidebar()
        self.create_main_area()
        self.show_section("all")

    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg=self.c["sidebar"], width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        logo = tk.Frame(sidebar, bg=self.c["sidebar"])
        logo.pack(pady=20, padx=15, fill="x")
        tk.Label(logo, text="📚", font=("Segoe UI", 24), bg=self.c["sidebar"]).pack()
        tk.Label(logo, text="Library", font=("Segoe UI", 18, "bold"), bg=self.c["sidebar"], fg=self.c["fg"]).pack()
        tk.Label(logo, text="Management System", font=("Segoe UI", 10), bg=self.c["sidebar"], fg=self.c["fg_mt"]).pack()
        menu_frame = tk.Frame(sidebar, bg=self.c["sidebar"])
        menu_frame.pack(fill="x", padx=10, pady=30)
        menu_items = [("📋 All Books", "all", self.c["accent"]), ("📗 Available", "available", self.c["success"]), ("📙 Issued", "issued", self.c["warning"]), ("➕ Add Book", "add", self.c["fg_sec"]), ("🔍 Search", "search", self.c["fg_sec"]), ("📊 Reports", "reports", self.c["fg_sec"])]
        self.menu_buttons = {}
        for text, key, color in menu_items:
            btn = tk.Button(menu_frame, text=text, font=("Segoe UI", 12), bg=self.c["sidebar"], fg=self.c["fg_sec"], relief="flat", bd=0, pady=12, padx=15, anchor="w", command=lambda k=key: self.show_section(k), cursor="hand2")
            btn.pack(fill="x", pady=2)
            self.menu_buttons[key] = btn
        self.menu_buttons["all"].config(bg=self.c["accent"], fg="#ffffff")
        stats_box = tk.Frame(sidebar, bg=self.c["panel"])
        stats_box.pack(side="bottom", fill="x", padx=10, pady=15)
        tk.Label(stats_box, text="Quick Stats", font=("Segoe UI", 10, "bold"), bg=self.c["panel"], fg=self.c["fg"]).pack(pady=(12, 8))
        self.total_stat = tk.Label(stats_box, text="", font=("Segoe UI", 11), bg=self.c["panel"], fg=self.c["fg_sec"])
        self.total_stat.pack()

    def create_main_area(self):
        self.main_frame = tk.Frame(self.root, bg=self.c["bg"])
        self.main_frame.pack(side="right", expand=True, fill="both")
        self.header = tk.Frame(self.main_frame, bg=self.c["bg"])
        self.header.pack(fill="x", padx=25, pady=(20, 0))
        self.title_label = tk.Label(self.header, text="📋 All Books", font=("Segoe UI", 22, "bold"), bg=self.c["bg"], fg=self.c["fg"])
        self.title_label.pack(side="left")
        self.subtitle = tk.Label(self.header, text="", font=("Segoe UI", 11), bg=self.c["bg"], fg=self.c["fg_sec"])
        self.subtitle.pack(side="right")
        self.content = tk.Frame(self.main_frame, bg=self.c["bg"])
        self.content.pack(expand=True, fill="both", padx=25, pady=15)
        self.status_bar = tk.Frame(self.main_frame, bg=self.c["panel"])
        self.status_bar.pack(fill="x", padx=25, pady=(0, 15))
        self.status = tk.Label(self.status_bar, text="✓ System ready", font=("Segoe UI", 10), bg=self.c["panel"], fg=self.c["success"], pady=12)
        self.status.pack(side="left")

    def show_section(self, section):
        for btn in self.menu_buttons.values():
            btn.config(bg=self.c["sidebar"], fg=self.c["fg_sec"])
        self.menu_buttons[section].config(bg=self.c["accent"], fg="#ffffff")
        titles = {"all": "📋 All Books", "available": "📗 Available Books", "issued": "📙 Issued Books", "add": "➕ Add New Book", "search": "🔍 Search Books", "reports": "📊 Library Reports"}
        self.title_label.config(text=titles[section])
        for widget in self.content.winfo_children():
            widget.destroy()
        if section == "all":
            self.show_all_books()
        elif section == "available":
            self.show_available()
        elif section == "issued":
            self.show_issued()
        elif section == "add":
            self.show_add_book()
        elif section == "search":
            self.show_search()
        elif section == "reports":
            self.show_reports()
        self.update_stats()

    def show_all_books(self):
        split = tk.PanedWindow(self.content, bg=self.c["bg"], orient="horizontal", bd=0)
        split.pack(expand=True, fill="both")
        all_items = []
        for book_id, info in self.books.items():
            all_items.append((book_id, info, "available"))
        for book_id, records in self.issued_books.items():
            if records:
                all_items.append((book_id, self.books.get(book_id, {}), "issued"))
        left = self.create_dict_list_panel(split, "All Books", all_items, "all")
        split.add(left, width=450)
        right = tk.Frame(split, bg=self.c["panel"])
        split.add(right)
        tk.Label(right, text="Actions", font=("Segoe UI", 14, "bold"), bg=self.c["panel"], fg=self.c["fg"]).pack(pady=15)
        self.create_action_button(right, "⬇ Issue Book", self.c["danger"], self.issue_from_all)
        self.create_action_button(right, "⬆ Return Book", self.c["success"], self.return_from_all)

    def show_available(self):
        split = tk.PanedWindow(self.content, bg=self.c["bg"], orient="horizontal", bd=0)
        split.pack(expand=True, fill="both")
        items = [(book_id, info) for book_id, info in self.books.items() if info["quantity"] > 0]
        left = self.create_dict_list_panel(split, "Available Books", items, "available")
        split.add(left, width=450)
        right = tk.Frame(split, bg=self.c["panel"])
        split.add(right)
        tk.Label(right, text="Issue Book", font=("Segoe UI", 14, "bold"), bg=self.c["panel"], fg=self.c["fg"]).pack(pady=15)
        tk.Label(right, text="Select a book and click Issue", font=("Segoe UI", 10), bg=self.c["panel"], fg=self.c["fg_mt"]).pack()
        self.create_action_button(right, "⬇ Issue Selected Book", self.c["danger"], self.issue_selected)
        tk.Label(right, text="Or choose:", font=("Segoe UI", 10), bg=self.c["panel"], fg=self.c["fg_mt"]).pack(pady=(20, 10))
        for i, (book_id, info) in enumerate(items[:5]):
            btn = tk.Button(right, text=f"📗 {info['title'][:30]}", font=("Segoe UI", 10), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, pady=10, anchor="w", command=lambda b_id=book_id: self.issue_book_quick(b_id), cursor="hand2")
            btn.pack(fill="x", pady=2, padx=20)

    def show_issued(self):
        split = tk.PanedWindow(self.content, bg=self.c["bg"], orient="horizontal", bd=0)
        split.pack(expand=True, fill="both")
        items = []
        for book_id, records in self.issued_books.items():
            for rec in records:
                if not rec["returned"]:
                    items.append((book_id, self.books.get(book_id, {}), rec))
        left = self.create_issued_list_panel(split, "Issued Books", items, "issued")
        split.add(left, width=450)
        right = tk.Frame(split, bg=self.c["panel"])
        split.add(right)
        tk.Label(right, text="Return Book", font=("Segoe UI", 14, "bold"), bg=self.c["panel"], fg=self.c["fg"]).pack(pady=15)
        tk.Label(right, text="Select a book and click Return", font=("Segoe UI", 10), bg=self.c["panel"], fg=self.c["fg_mt"]).pack()
        self.create_action_button(right, "⬆ Return Selected Book", self.c["success"], self.return_selected)
        tk.Label(right, text="Or choose:", font=("Segoe UI", 10), bg=self.c["panel"], fg=self.c["fg_mt"]).pack(pady=(20, 10))
        for i, (book_id, info, rec) in enumerate(items[:5]):
            btn = tk.Button(right, text=f"📙 {info.get('title', 'Unknown')[:30]} - {rec['student_name']}", font=("Segoe UI", 10), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, pady=10, anchor="w", command=lambda b_id=book_id, s=rec["student_name"]: self.return_book_quick(b_id, s), cursor="hand2")
            btn.pack(fill="x", pady=2, padx=20)

    def show_add_book(self):
        panel = tk.Frame(self.content, bg=self.c["panel"])
        panel.pack(expand=True, fill="both")
        tk.Label(panel, text="Add a new book to the library", font=("Segoe UI", 12), bg=self.c["panel"], fg=self.c["fg_sec"]).pack(pady=(20, 15))
        fields_frame = tk.Frame(panel, bg=self.c["panel"])
        fields_frame.pack(pady=10)
        tk.Label(fields_frame, text="Book ID:", font=("Segoe UI", 11), bg=self.c["panel"], fg=self.c["fg"]).grid(row=0, column=0, sticky="w", padx=20, pady=8)
        self.book_id_entry = tk.Entry(fields_frame, font=("Segoe UI", 12), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, insertbackground=self.c["fg"], width=25)
        self.book_id_entry.grid(row=0, column=1, padx=10, pady=8)
        tk.Label(fields_frame, text="Title:", font=("Segoe UI", 11), bg=self.c["panel"], fg=self.c["fg"]).grid(row=1, column=0, sticky="w", padx=20, pady=8)
        self.title_entry = tk.Entry(fields_frame, font=("Segoe UI", 12), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, insertbackground=self.c["fg"], width=25)
        self.title_entry.grid(row=1, column=1, padx=10, pady=8)
        tk.Label(fields_frame, text="Author:", font=("Segoe UI", 11), bg=self.c["panel"], fg=self.c["fg"]).grid(row=2, column=0, sticky="w", padx=20, pady=8)
        self.author_entry = tk.Entry(fields_frame, font=("Segoe UI", 12), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, insertbackground=self.c["fg"], width=25)
        self.author_entry.grid(row=2, column=1, padx=10, pady=8)
        tk.Label(fields_frame, text="Copies:", font=("Segoe UI", 11), bg=self.c["panel"], fg=self.c["fg"]).grid(row=3, column=0, sticky="w", padx=20, pady=8)
        self.copies_entry = tk.Entry(fields_frame, font=("Segoe UI", 12), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, insertbackground=self.c["fg"], width=25)
        self.copies_entry.grid(row=3, column=1, padx=10, pady=8)
        self.create_action_button(panel, "➕ Add Book", self.c["accent"], self.add_new_book)

    def show_search(self):
        panel = tk.Frame(self.content, bg=self.c["panel"])
        panel.pack(expand=True, fill="both")
        tk.Label(panel, text="Search for books in the library", font=("Segoe UI", 12), bg=self.c["panel"], fg=self.c["fg_sec"]).pack(pady=(20, 15))
        self.search_entry = tk.Entry(panel, font=("Segoe UI", 14), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, insertbackground=self.c["fg"])
        self.search_entry.pack(fill="x", padx=30, pady=(0, 15))
        self.search_entry.bind("<KeyRelease>", lambda e: self.do_search())
        self.search_results = tk.Label(panel, text="Type to search...", font=("Segoe UI", 11), bg=self.c["panel"], fg=self.c["fg_mt"])
        self.search_results.pack(pady=10)

    def do_search(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.search_results.config(text="Type to search...", fg=self.c["fg_mt"])
            return
        results = []
        for book_id, info in self.books.items():
            if query in info["title"].lower() or query in info["author"].lower():
                status = f"Available ({info['quantity']} copies)"
                results.append(f"✅ {info['title']} by {info['author']} - {status}")
        for book_id, records in self.issued_books.items():
            for rec in records:
                if not rec["returned"] and query in self.books.get(book_id, {}).get("title", "").lower():
                    results.append(f"📙 {self.books[book_id]['title']} - Issued to {rec['student_name']} (Due: {rec['due_date']})")
        if results:
            self.search_results.config(text=f"Found {len(results)} book(s):\n\n" + "\n".join(results[:10]), fg=self.c["success"])
        else:
            self.search_results.config(text="No books found", fg=self.c["danger"])

    def show_reports(self):
        panel = tk.Frame(self.content, bg=self.c["panel"])
        panel.pack(expand=True, fill="both")
        total_books = sum(info["total_copies"] for info in self.books.values())
        available = sum(info["quantity"] for info in self.books.values())
        issued_count = sum(len([r for r in records if not r["returned"]]) for records in self.issued_books.values())
        stats = [("📚 Total Copies", total_books, self.c["accent"]), ("✅ Available", available, self.c["success"]), ("📙 Issued", issued_count, self.c["warning"])]
        grid = tk.Frame(panel, bg=self.c["panel"])
        grid.pack(expand=True)
        for i, (label, count, color) in enumerate(stats):
            card = tk.Frame(grid, bg=self.c["card"], padx=30, pady=25)
            card.grid(row=0, column=i, padx=15, pady=30)
            tk.Label(card, text=label, font=("Segoe UI", 12), bg=self.c["card"], fg=self.c["fg_sec"]).pack()
            tk.Label(card, text=str(count), font=("Segoe UI", 32, "bold"), bg=self.c["card"], fg=color).pack()
        fines_frame = tk.Frame(panel, bg=self.c["panel"])
        fines_frame.pack(pady=20)
        tk.Label(fines_frame, text="Overdue Fines:", font=("Segoe UI", 14, "bold"), bg=self.c["panel"], fg=self.c["fg"]).pack()
        total_fines = 0
        for book_id, records in self.issued_books.items():
            for rec in records:
                if not rec["returned"]:
                    due = datetime.strptime(rec["due_date"], "%Y-%m-%d")
                    days_late = (datetime.now() - due).days
                    if days_late > 0:
                        weeks = (days_late + 6) // 7
                        fine = weeks * self.FINE_RATE_PER_WEEK
                        total_fines += fine
        tk.Label(fines_frame, text=f"Total Outstanding Fines: ${total_fines}", font=("Segoe UI", 16, "bold"), bg=self.c["panel"], fg=self.c["danger"]).pack()

    def create_dict_list_panel(self, parent, title, items, section):
        frame = tk.Frame(parent, bg=self.c["panel"])
        tk.Label(frame, text=title, font=("Segoe UI", 14, "bold"), bg=self.c["panel"], fg=self.c["fg"]).pack(pady=15, padx=20, anchor="w")
        list_frame = tk.Frame(frame, bg=self.c["card"])
        list_frame.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        listbox = tk.Listbox(list_frame, font=("Segoe UI", 11), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, selectbackground=self.c["accent"], selectforeground="#ffffff", activestyle="none", yscrollcommand=scrollbar.set, highlightthickness=0, borderwidth=0)
        listbox.pack(side="left", expand=True, fill="both", padx=(10, 0))
        scrollbar.config(command=listbox.yview)
        for item in items:
            if section == "all":
                book_id, info, item_type = item
                title = info.get("title", "Unknown")
                qty = info.get("quantity", 0)
                icon = "📗" if item_type == "available" else "📙"
                listbox.insert(tk.END, f"  {icon}  [{book_id}] {title} (Avail: {qty})")
            else:
                book_id, info = item
                title = info.get("title", "Unknown")
                qty = info.get("quantity", 0)
                listbox.insert(tk.END, f"  📗  [{book_id}] {title} (Copies: {qty})")
        if section == "available":
            self.available_list = listbox
        elif section == "issued":
            self.issued_list = listbox
        elif section == "all":
            self.all_list = listbox
        return frame

    def create_issued_list_panel(self, parent, title, items, section):
        frame = tk.Frame(parent, bg=self.c["panel"])
        tk.Label(frame, text=title, font=("Segoe UI", 14, "bold"), bg=self.c["panel"], fg=self.c["fg"]).pack(pady=15, padx=20, anchor="w")
        list_frame = tk.Frame(frame, bg=self.c["card"])
        list_frame.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        listbox = tk.Listbox(list_frame, font=("Segoe UI", 10), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, selectbackground=self.c["accent"], selectforeground="#ffffff", activestyle="none", yscrollcommand=scrollbar.set, highlightthickness=0, borderwidth=0)
        listbox.pack(side="left", expand=True, fill="both", padx=(10, 0))
        scrollbar.config(command=listbox.yview)
        for item in items:
            book_id, info, rec = item
            title = info.get("title", "Unknown")[:25]
            student = rec["student_name"][:15]
            due = rec["due_date"]
            listbox.insert(tk.END, f"  📙  {title:25} | {student:15} | Due: {due}")
        self.issued_list = listbox
        return frame

    def create_action_button(self, parent, text, color, command):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 12, "bold"), bg=color, fg="#ffffff", relief="flat", bd=0, padx=20, pady=12, command=command, cursor="hand2")
        btn.pack(fill="x", padx=20, pady=10)
        def on_enter(e):
            btn.config(bg=self.c["accent_hover"] if color == self.c["accent"] else color)
        def on_leave(e):
            btn.config(bg=color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def update_stats(self):
        total_books = sum(info["total_copies"] for info in self.books.values())
        available = sum(info["quantity"] for info in self.books.values())
        issued = sum(len([r for r in records if not r["returned"]]) for records in self.issued_books.values())
        self.total_stat.config(text=f"Total: {total_books} | Avail: {available} | Issued: {issued}")
        self.subtitle.config(text=f"{available} available • {issued} issued")

    def add_new_book(self):
        book_id = self.book_id_entry.get().strip()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        copies_str = self.copies_entry.get().strip()
        if not all([book_id, title, author, copies_str]):
            self.set_status("✗ All fields required!", self.c["danger"])
            return
        if book_id in self.books:
            self.set_status("✗ Book ID already exists!", self.c["danger"])
            return
        try:
            copies = int(copies_str)
            if copies <= 0:
                raise ValueError
        except ValueError:
            self.set_status("✗ Invalid copies count!", self.c["danger"])
            return
        self.books[book_id] = {"title": title, "author": author, "quantity": copies, "total_copies": copies}
        self.book_id_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.copies_entry.delete(0, tk.END)
        self.set_status(f"✓ Added: {title}", self.c["success"])
        self.show_section("add")

    def issue_selected(self):
        selection = self.available_list.curselection()
        if not selection:
            self.set_status("✗ Select a book first!", self.c["warning"])
            return
        idx = selection[0]
        available_items = [(book_id, info) for book_id, info in self.books.items() if info["quantity"] > 0]
        if idx >= len(available_items):
            return
        book_id, info = available_items[idx]
        self.open_issue_dialog(book_id, info["title"])

    def issue_book_quick(self, book_id):
        info = self.books.get(book_id)
        if info and info["quantity"] > 0:
            self.open_issue_dialog(book_id, info["title"])

    def open_issue_dialog(self, book_id, title):
        dialog = tk.Toplevel(self.root)
        dialog.title("Issue Book")
        dialog.geometry("400x300")
        dialog.configure(bg=self.c["panel"])
        dialog.transient(self.root)
        dialog.grab_set()
        tk.Label(dialog, text=f"Issue: {title}", font=("Segoe UI", 14, "bold"), bg=self.c["panel"], fg=self.c["fg"]).pack(pady=15)
        fields = tk.Frame(dialog, bg=self.c["panel"])
        fields.pack(pady=10)
        tk.Label(fields, text="Student Name:", font=("Segoe UI", 11), bg=self.c["panel"], fg=self.c["fg"]).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        student_entry = tk.Entry(fields, font=("Segoe UI", 11), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, insertbackground=self.c["fg"], width=20)
        student_entry.grid(row=0, column=1, padx=10, pady=8)
        tk.Label(fields, text="Duration (days):", font=("Segoe UI", 11), bg=self.c["panel"], fg=self.c["fg"]).grid(row=1, column=0, sticky="w", padx=10, pady=8)
        duration_entry = tk.Entry(fields, font=("Segoe UI", 11), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, insertbackground=self.c["fg"], width=20)
        duration_entry.insert(0, "14")
        duration_entry.grid(row=1, column=1, padx=10, pady=8)
        def confirm_issue():
            student = student_entry.get().strip()
            duration_str = duration_entry.get().strip()
            if not student:
                messagebox.showwarning("Required", "Enter student name")
                return
            try:
                duration = int(duration_str)
                if not (1 <= duration <= 30):
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Invalid", "Duration must be 1-30 days")
                return
            issue_date = datetime.now()
            due_date = issue_date + timedelta(days=duration)
            if book_id not in self.issued_books:
                self.issued_books[book_id] = []
            self.issued_books[book_id].append({"student_name": student, "issue_date": issue_date.strftime("%Y-%m-%d %H:%M"), "due_date": due_date.strftime("%Y-%m-%d"), "returned": False})
            self.books[book_id]["quantity"] -= 1
            self.set_status(f"✓ Issued to {student}", self.c["success"])
            dialog.destroy()
            self.show_section("available")
        btn_frame = tk.Frame(dialog, bg=self.c["panel"])
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Confirm Issue", font=("Segoe UI", 11, "bold"), bg=self.c["success"], fg="#fff", relief="flat", bd=0, padx=20, pady=8, command=confirm_issue).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", font=("Segoe UI", 11), bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0, padx=20, pady=8, command=dialog.destroy).pack(side="left", padx=5)

    def return_selected(self):
        selection = self.issued_list.curselection()
        if not selection:
            self.set_status("✗ Select a book first!", self.c["warning"])
            return
        idx = selection[0]
        issued_items = []
        for book_id, records in self.issued_books.items():
            for rec in records:
                if not rec["returned"]:
                    issued_items.append((book_id, self.books.get(book_id, {}), rec))
        if idx >= len(issued_items):
            return
        book_id, info, rec = issued_items[idx]
        self.process_return(book_id, info, rec)

    def return_book_quick(self, book_id, student_name):
        for rec in self.issued_books.get(book_id, []):
            if rec["student_name"] == student_name and not rec["returned"]:
                self.process_return(book_id, self.books.get(book_id, {}), rec)
                break

    def process_return(self, book_id, info, rec):
        return_date = datetime.now()
        due_date = datetime.strptime(rec["due_date"], "%Y-%m-%d")
        days_late = (return_date - due_date).days
        fine = 0
        if days_late > 0:
            weeks_late = (days_late + 6) // 7
            fine = weeks_late * self.FINE_RATE_PER_WEEK
        rec["returned"] = True
        rec["return_date"] = return_date.strftime("%Y-%m-%d %H:%M")
        self.books[book_id]["quantity"] += 1
        msg = f"✓ Returned: {info.get('title', 'Unknown')}"
        if fine > 0:
            msg += f" | Fine: ${fine}"
        self.set_status(msg, self.c["success"])
        self.show_section("issued")

    def issue_from_all(self):
        selection = self.all_list.curselection()
        if not selection:
            self.set_status("✗ Select a book first!", self.c["warning"])
            return
        idx = selection[0]
        all_items = []
        for book_id, info in self.books.items():
            if info["quantity"] > 0:
                all_items.append(("available", book_id, info))
        for book_id, records in self.issued_books.items():
            for rec in records:
                if not rec["returned"]:
                    all_items.append(("issued", book_id, self.books.get(book_id, {})))
        if idx < len(all_items):
            item_type, book_id, info = all_items[idx]
            if item_type == "available":
                self.open_issue_dialog(book_id, info["title"])

    def return_from_all(self):
        selection = self.all_list.curselection()
        if not selection:
            self.set_status("✗ Select a book first!", self.c["warning"])
            return
        idx = selection[0]
        all_items = []
        for book_id, records in self.issued_books.items():
            for rec in records:
                if not rec["returned"]:
                    all_items.append((book_id, self.books.get(book_id, {}), rec))
        if idx < len(all_items):
            book_id, info, rec = all_items[idx]
            self.process_return(book_id, info, rec)

    def set_status(self, message, color):
        self.status.config(text=message, fg=color)
        self.root.after(2500, lambda: self.status.config(text="✓ System ready", fg=self.c["success"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
