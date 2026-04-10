import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1100x750")
        self.root.configure(bg="#08080c")
        
        self.books = [
            "Attack on Titan", "Solo Leveling", "Naruto", "One Piece", "Dragon Ball Z",
            "Demon Slayer", "My Hero Academia", "Death Note", "Fullmetal Alchemist",
            "One Punch Man", "Tokyo Revengers", "Jujutsu Kaisen", "Chainsaw Man",
            "Bleach", "Hunter x Hunter"
        ]
        self.issued_books = []
        
        self.style_ui()
        self.create_widgets()
        
    def style_ui(self):
        self.c = {
            "bg": "#08080c",
            "sidebar": "#0e0e14",
            "panel": "#14141c",
            "card": "#1a1a24",
            "card_hover": "#22222e",
            "accent": "#6366f1",
            "accent_hover": "#818cf8",
            "success": "#22c55e",
            "warning": "#f59e0b",
            "danger": "#ef4444",
            "fg": "#fafafa",
            "fg_sec": "#a1a1aa",
            "fg_mt": "#71717a",
            "border": "#27272a",
        }
        
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
        
        menu_items = [
            ("📋 All Books", "all", self.c["accent"]),
            ("📗 Available", "available", self.c["success"]),
            ("📙 Issued", "issued", self.c["warning"]),
            ("➕ Add Book", "add", self.c["fg_sec"]),
            ("🔍 Search", "search", self.c["fg_sec"]),
            ("📊 Reports", "reports", self.c["fg_sec"]),
        ]
        
        self.menu_buttons = {}
        for text, key, color in menu_items:
            btn = tk.Button(menu_frame, text=text, font=("Segoe UI", 12),
                          bg=self.c["sidebar"], fg=self.c["fg_sec"],
                          relief="flat", bd=0, pady=12, padx=15, anchor="w",
                          command=lambda k=key: self.show_section(k),
                          cursor="hand2")
            btn.pack(fill="x", pady=2)
            self.menu_buttons[key] = btn
            
        self.menu_buttons["all"].config(bg=self.c["accent"], fg="#ffffff")
        
        stats_box = tk.Frame(sidebar, bg=self.c["panel"])
        stats_box.pack(side="bottom", fill="x", padx=10, pady=15)
        
        tk.Label(stats_box, text="Quick Stats", font=("Segoe UI", 10, "bold"),
                bg=self.c["panel"], fg=self.c["fg"]).pack(pady=(12, 8))
        
        self.total_stat = tk.Label(stats_box, text="", font=("Segoe UI", 11),
                                  bg=self.c["panel"], fg=self.c["fg_sec"])
        self.total_stat.pack()
        
    def create_main_area(self):
        self.main_frame = tk.Frame(self.root, bg=self.c["bg"])
        self.main_frame.pack(side="right", expand=True, fill="both")
        
        self.header = tk.Frame(self.main_frame, bg=self.c["bg"])
        self.header.pack(fill="x", padx=25, pady=(20, 0))
        
        self.title_label = tk.Label(self.header, text="📋 All Books", 
                                   font=("Segoe UI", 22, "bold"), 
                                   bg=self.c["bg"], fg=self.c["fg"])
        self.title_label.pack(side="left")
        
        self.subtitle = tk.Label(self.header, text="", font=("Segoe UI", 11),
                                bg=self.c["bg"], fg=self.c["fg_sec"])
        self.subtitle.pack(side="right")
        
        self.content = tk.Frame(self.main_frame, bg=self.c["bg"])
        self.content.pack(expand=True, fill="both", padx=25, pady=15)
        
        self.status_bar = tk.Frame(self.main_frame, bg=self.c["panel"])
        self.status_bar.pack(fill="x", padx=25, pady=(0, 15))
        
        self.status = tk.Label(self.status_bar, text="✓ System ready", 
                              font=("Segoe UI", 10), bg=self.c["panel"], 
                              fg=self.c["success"], pady=12)
        self.status.pack(side="left")
        
    def show_section(self, section):
        for btn in self.menu_buttons.values():
            btn.config(bg=self.c["sidebar"], fg=self.c["fg_sec"])
        self.menu_buttons[section].config(bg=self.c["accent"], fg="#ffffff")
        
        titles = {
            "all": "📋 All Books",
            "available": "📗 Available Books",
            "issued": "📙 Issued Books",
            "add": "➕ Add New Book",
            "search": "🔍 Search Books",
            "reports": "📊 Library Reports"
        }
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
        
        left = self.create_list_panel(split, "All Books", self.books + self.issued_books, "all")
        split.add(left, width=450)
        
        right = tk.Frame(split, bg=self.c["panel"])
        split.add(right)
        
        tk.Label(right, text="Actions", font=("Segoe UI", 14, "bold"),
                bg=self.c["panel"], fg=self.c["fg"]).pack(pady=15)
        
        self.create_action_button(right, "⬇ Issue Book", self.c["danger"], self.issue_from_all)
        self.create_action_button(right, "⬆ Return Book", self.c["success"], self.return_from_all)
        
    def show_available(self):
        split = tk.PanedWindow(self.content, bg=self.c["bg"], orient="horizontal", bd=0)
        split.pack(expand=True, fill="both")
        
        left = self.create_list_panel(split, "Available Books", self.books, "available")
        split.add(left, width=450)
        
        right = tk.Frame(split, bg=self.c["panel"])
        split.add(right)
        
        tk.Label(right, text="Issue Book", font=("Segoe UI", 14, "bold"),
                bg=self.c["panel"], fg=self.c["fg"]).pack(pady=15)
        
        tk.Label(right, text="Select a book and click Issue", font=("Segoe UI", 10),
                bg=self.c["panel"], fg=self.c["fg_mt"]).pack()
        
        self.create_action_button(right, "⬇ Issue Selected Book", self.c["danger"], self.issue_selected)
        
        tk.Label(right, text="Or choose:", font=("Segoe UI", 10),
                bg=self.c["panel"], fg=self.c["fg_mt"]).pack(pady=(20, 10))
        
        for book in self.books[:5]:
            btn = tk.Button(right, text=f"📗 {book[:30]}", font=("Segoe UI", 10),
                          bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0,
                          pady=10, anchor="w", command=lambda b=book: self.issue_book_quick(b),
                          cursor="hand2")
            btn.pack(fill="x", pady=2, padx=20)
            
    def show_issued(self):
        split = tk.PanedWindow(self.content, bg=self.c["bg"], orient="horizontal", bd=0)
        split.pack(expand=True, fill="both")
        
        left = self.create_list_panel(split, "Issued Books", self.issued_books, "issued")
        split.add(left, width=450)
        
        right = tk.Frame(split, bg=self.c["panel"])
        split.add(right)
        
        tk.Label(right, text="Return Book", font=("Segoe UI", 14, "bold"),
                bg=self.c["panel"], fg=self.c["fg"]).pack(pady=15)
        
        tk.Label(right, text="Select a book and click Return", font=("Segoe UI", 10),
                bg=self.c["panel"], fg=self.c["fg_mt"]).pack()
        
        self.create_action_button(right, "⬆ Return Selected Book", self.c["success"], self.return_selected)
        
        tk.Label(right, text="Or choose:", font=("Segoe UI", 10),
                bg=self.c["panel"], fg=self.c["fg_mt"]).pack(pady=(20, 10))
        
        for book in self.issued_books[:5]:
            btn = tk.Button(right, text=f"📙 {book[:30]}", font=("Segoe UI", 10),
                          bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0,
                          pady=10, anchor="w", command=lambda b=book: self.return_book_quick(b),
                          cursor="hand2")
            btn.pack(fill="x", pady=2, padx=20)
            
    def show_add_book(self):
        panel = tk.Frame(self.content, bg=self.c["panel"])
        panel.pack(expand=True, fill="both")
        
        tk.Label(panel, text="Add a new book to the library", font=("Segoe UI", 12),
                bg=self.c["panel"], fg=self.c["fg_sec"]).pack(pady=(20, 15))
        
        self.new_book_entry = tk.Entry(panel, font=("Segoe UI", 14), bg=self.c["card"],
                                      fg=self.c["fg"], relief="flat", bd=0, 
                                      insertbackground=self.c["fg"])
        self.new_book_entry.pack(fill="x", padx=30, pady=(0, 15))
        self.new_book_entry.bind("<Return>", lambda e: self.add_new_book())
        
        self.create_action_button(panel, "➕ Add Book", self.c["accent"], self.add_new_book)
        
        tk.Label(panel, text="Quick Add:", font=("Segoe UI", 11, "bold"),
                bg=self.c["panel"], fg=self.c["fg"]).pack(pady=(30, 10))
        
        quick = ["Tokyo Ghoul", "AOT", "Violet Evergarden", "Steins;Gate", "Erased"]
        for book in quick:
            btn = tk.Button(panel, text=f"  {book}", font=("Segoe UI", 11),
                          bg=self.c["card"], fg=self.c["fg"], relief="flat", bd=0,
                          pady=8, anchor="w", command=lambda b=book: self.quick_add(b),
                          cursor="hand2")
            btn.pack(fill="x", pady=3, padx=30)
            
    def show_search(self):
        panel = tk.Frame(self.content, bg=self.c["panel"])
        panel.pack(expand=True, fill="both")
        
        tk.Label(panel, text="Search for books in the library", font=("Segoe UI", 12),
                bg=self.c["panel"], fg=self.c["fg_sec"]).pack(pady=(20, 15))
        
        self.search_entry = tk.Entry(panel, font=("Segoe UI", 14), bg=self.c["card"],
                                   fg=self.c["fg"], relief="flat", bd=0,
                                   insertbackground=self.c["fg"])
        self.search_entry.pack(fill="x", padx=30, pady=(0, 15))
        self.search_entry.bind("<KeyRelease>", lambda e: self.do_search())
        
        self.search_results = tk.Label(panel, text="Type to search...", font=("Segoe UI", 11),
                                     bg=self.c["panel"], fg=self.c["fg_mt"])
        self.search_results.pack(pady=10)
        
    def do_search(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.search_results.config(text="Type to search...", fg=self.c["fg_mt"])
            return
            
        results = []
        for book in self.books:
            if query in book.lower():
                results.append(f"✅ {book} (Available)")
        for book in self.issued_books:
            if query in book.lower():
                results.append(f"📙 {book} (Issued)")
                
        if results:
            self.search_results.config(
                text=f"Found {len(results)} book(s):\n\n" + "\n".join(results),
                fg=self.c["success"]
            )
        else:
            self.search_results.config(text="No books found", fg=self.c["danger"])
            
    def show_reports(self):
        panel = tk.Frame(self.content, bg=self.c["panel"])
        panel.pack(expand=True, fill="both")
        
        total = len(self.books) + len(self.issued_books)
        available = len(self.books)
        issued = len(self.issued_books)
        
        stats = [
            ("📚 Total Books", total, self.c["accent"]),
            ("✅ Available", available, self.c["success"]),
            ("📙 Issued", issued, self.c["warning"]),
        ]
        
        grid = tk.Frame(panel, bg=self.c["panel"])
        grid.pack(expand=True)
        
        for i, (label, count, color) in enumerate(stats):
            card = tk.Frame(grid, bg=self.c["card"], padx=30, pady=25)
            card.grid(row=0, column=i, padx=15, pady=30)
            
            tk.Label(card, text=label, font=("Segoe UI", 12),
                    bg=self.c["card"], fg=self.c["fg_sec"]).pack()
            tk.Label(card, text=str(count), font=("Segoe UI", 32, "bold"),
                    bg=self.c["card"], fg=color).pack()
                    
    def create_list_panel(self, parent, title, items, section):
        frame = tk.Frame(parent, bg=self.c["panel"])
        
        tk.Label(frame, text=title, font=("Segoe UI", 14, "bold"),
                bg=self.c["panel"], fg=self.c["fg"]).pack(pady=15, padx=20, anchor="w")
        
        list_frame = tk.Frame(frame, bg=self.c["card"])
        list_frame.pack(expand=True, fill="both", padx=15, pady=(0, 15))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        listbox = tk.Listbox(list_frame, font=("Segoe UI", 12), bg=self.c["card"],
                            fg=self.c["fg"], relief="flat", bd=0,
                            selectbackground=self.c["accent"], selectforeground="#ffffff",
                            activestyle="none", yscrollcommand=scrollbar.set,
                            highlightthickness=0, borderwidth=0)
        listbox.pack(side="left", expand=True, fill="both", padx=(10, 0))
        scrollbar.config(command=listbox.yview)
        
        for item in items:
            icon = "📗" if section == "available" else "📙" if section == "issued" else "📖"
            listbox.insert(tk.END, f"  {icon}  {item}")
            
        if section == "available":
            self.available_list = listbox
        elif section == "issued":
            self.issued_list = listbox
        elif section == "all":
            self.all_list = listbox
            
        return frame
        
    def create_action_button(self, parent, text, color, command):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 12, "bold"),
                      bg=color, fg="#ffffff", relief="flat", bd=0,
                      padx=20, pady=12, command=command, cursor="hand2")
        btn.pack(fill="x", padx=20, pady=10)
        
        def on_enter(e):
            btn.config(bg=self.c["accent_hover"])
        def on_leave(e):
            btn.config(bg=color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
        
    def update_stats(self):
        total = len(self.books) + len(self.issued_books)
        self.total_stat.config(text=f"Total: {total} | Available: {len(self.books)} | Issued: {len(self.issued_books)}")
        self.subtitle.config(text=f"{len(self.books)} available • {len(self.issued_books)} issued")
        
    def add_new_book(self):
        book = self.new_book_entry.get().strip()
        if book:
            self.books.append(book)
            self.new_book_entry.delete(0, tk.END)
            self.set_status(f"✓ Added: {book}", self.c["success"])
            self.show_section("add")
            
    def quick_add(self, book):
        self.books.append(book)
        self.set_status(f"✓ Added: {book}", self.c["success"])
        self.show_section("add")
        
    def issue_selected(self):
        selection = self.available_list.curselection()
        if selection:
            book = self.books[selection[0]]
            self.books.remove(book)
            self.issued_books.append(book)
            self.set_status(f"↓ Issued: {book}", self.c["danger"])
            self.show_section("available")
            
    def return_selected(self):
        selection = self.issued_list.curselection()
        if selection:
            book = self.issued_books[selection[0]]
            self.issued_books.remove(book)
            self.books.append(book)
            self.set_status(f"↑ Returned: {book}", self.c["success"])
            self.show_section("issued")
            
    def issue_book_quick(self, book):
        self.books.remove(book)
        self.issued_books.append(book)
        self.set_status(f"↓ Issued: {book}", self.c["danger"])
        self.show_section("available")
        
    def return_book_quick(self, book):
        self.issued_books.remove(book)
        self.books.append(book)
        self.set_status(f"↑ Returned: {book}", self.c["success"])
        self.show_section("issued")
        
    def issue_from_all(self):
        selection = self.all_list.curselection()
        if selection:
            index = selection[0]
            all_books = self.books + self.issued_books
            if index < len(all_books):
                book = all_books[index]
                if book in self.books:
                    self.books.remove(book)
                    self.issued_books.append(book)
                    self.set_status(f"↓ Issued: {book}", self.c["danger"])
                self.show_section("all")
                
    def return_from_all(self):
        selection = self.all_list.curselection()
        if selection:
            index = selection[0]
            all_books = self.books + self.issued_books
            if index < len(all_books):
                book = all_books[index]
                if book in self.issued_books:
                    self.issued_books.remove(book)
                    self.books.append(book)
                    self.set_status(f"↑ Returned: {book}", self.c["success"])
                self.show_section("all")
        
    def set_status(self, message, color):
        self.status.config(text=message, fg=color)
        self.root.after(2500, lambda: self.status.config(text="✓ System ready", fg=self.c["success"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()