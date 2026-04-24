from datetime import datetime, timedelta

books = {}
issued_books = {}
FINE_RATE_PER_WEEK = 10

famous_books = {
    "B001": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "quantity": 3},
    "B002": {"title": "To Kill a Mockingbird", "author": "Harper Lee", "quantity": 4},
    "B003": {"title": "1984", "author": "George Orwell", "quantity": 5},
    "B004": {"title": "Pride and Prejudice", "author": "Jane Austen", "quantity": 3},
    "B005": {"title": "The Hobbit", "author": "J.R.R. Tolkien", "quantity": 2},
    "B006": {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "quantity": 6},
    "B007": {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "quantity": 3},
    "B008": {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "quantity": 4},
    "B009": {"title": "Animal Farm", "author": "George Orwell", "quantity": 5},
    "B010": {"title": "Brave New World", "author": "Aldous Huxley", "quantity": 2},
}

for bid, info in famous_books.items():
    books[bid] = info
    books[bid]["total_copies"] = info["quantity"]


def add_book():
    print("\n" + "="*50)
    print("ADD NEW BOOK")
    print("="*50)
    book_id = input("Enter Book ID: ").strip()
    if book_id in books:
        print(f"Book ID '{book_id}' already exists!")
        return
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()
    while True:
        try:
            quantity = int(input("Enter Number of Copies: "))
            if quantity > 0:
                break
            print("Quantity must be positive.")
        except ValueError:
            print("Invalid input. Enter a number.")
    books[book_id] = {"title": title, "author": author, "quantity": quantity, "total_copies": quantity}
    print(f"\n'{title}' by {author} added successfully ({quantity} copies).")
    input("\nPress Enter to continue...")


def show_books():
    print("\n" + "="*70)
    print("AVAILABLE BOOKS IN LIBRARY")
    print("="*70)
    if not books:
        print("No books in the library.")
    else:
        print(f"{'ID':<8} {'Title':<35} {'Author':<20} {'Available':<10}")
        print("-"*75)
        for book_id, info in books.items():
            available = info["quantity"]
            status = "✓" if available > 0 else "✗"
            print(f"{book_id:<8} {info['title'][:35]:<35} {info['author'][:20]:<20} {available:<10} {status}")
    input("\nPress Enter to continue...")


def search_book():
    print("\n" + "="*50)
    print("SEARCH BOOK")
    print("="*50)
    keyword = input("Enter title or author keyword: ").strip().lower()
    results = []
    for book_id, info in books.items():
        if keyword in info["title"].lower() or keyword in info["author"].lower():
            results.append((book_id, info))
    if not results:
        print("No books found matching your search.")
    else:
        print(f"\nFound {len(results)} book(s):")
        print(f"{'ID':<8} {'Title':<35} {'Author':<20} {'Available':<10}")
        print("-"*75)
        for book_id, info in results:
            available = info["quantity"]
            print(f"{book_id:<8} {info['title'][:35]:<35} {info['author'][:20]:<20} {available:<10}")
    input("\nPress Enter to continue...")


def issue_book():
    print("\n" + "="*50)
    print("ISSUE BOOK")
    print("="*50)
    book_id = input("Enter Book ID: ").strip()
    if book_id not in books:
        print("Book not found.")
        input("\nPress Enter to continue...")
        return
    if books[book_id]["quantity"] <= 0:
        print("All copies are currently issued.")
        input("\nPress Enter to continue...")
        return
    student_name = input("Enter Student Name: ").strip()
    while True:
        duration_days = input("Enter Issue Duration (days, max 30): ")
        try:
            duration = int(duration_days)
            if 1 <= duration <= 30:
                break
            print("Duration must be between 1 and 30 days.")
        except ValueError:
            print("Invalid input. Enter a number.")
    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=duration)
    if book_id not in issued_books:
        issued_books[book_id] = []
    issued_books[book_id].append({"student_name": student_name, "issue_date": issue_date.strftime("%Y-%m-%d %H:%M"), "due_date": due_date.strftime("%Y-%m-%d"), "returned": False})
    books[book_id]["quantity"] -= 1
    print(f"\nBook issued successfully!")
    print(f"Book Title : {books[book_id]['title']}")
    print(f"Student    : {student_name}")
    print(f"Issue Date : {issue_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"Due Date   : {due_date.strftime('%Y-%m-%d')}")
    print(f"Remaining Copies: {books[book_id]['quantity']}")
    input("\nPress Enter to continue...")


def return_book():
    print("\n" + "="*50)
    print("RETURN BOOK")
    print("="*50)
    book_id = input("Enter Book ID: ").strip()
    if book_id not in issued_books or not issued_books[book_id]:
        print("No issued records found for this book.")
        input("\nPress Enter to continue...")
        return
    student_name = input("Enter Student Name: ").strip()
    found_record = None
    for record in issued_books[book_id]:
        if record["student_name"].lower() == student_name.lower() and not record["returned"]:
            found_record = record
            break
    if not found_record:
        print(f"No active issue record found for {student_name}.")
        input("\nPress Enter to continue...")
        return
    return_date = datetime.now()
    due_date = datetime.strptime(found_record["due_date"], "%Y-%m-%d")
    days_late = (return_date - due_date).days
    fine = 0
    if days_late > 0:
        weeks_late = (days_late + 6) // 7
        fine = weeks_late * FINE_RATE_PER_WEEK
    found_record["returned"] = True
    found_record["return_date"] = return_date.strftime("%Y-%m-%d %H:%M")
    books[book_id]["quantity"] += 1
    print("\nReturn processed successfully!")
    print(f"Book Title  : {books[book_id]['title']}")
    print(f"Student     : {student_name}")
    print(f"Issue Date  : {found_record['issue_date']}")
    print(f"Due Date    : {found_record['due_date']}")
    print(f"Return Date : {return_date.strftime('%Y-%m-%d %H:%M')}")
    if days_late > 0:
        print(f"\nReturned {days_late} day(s) late.")
        print(f"Weeks overdue: {weeks_late}")
        print(f"Fine Amount : ${fine}")
    else:
        print("\nReturned on time. No fine.")
    input("\nPress Enter to continue...")


def show_issued_books():
    print("\n" + "="*70)
    print("ISSUED BOOKS RECORDS")
    print("="*70)
    if not issued_books:
        print("No books have been issued.")
    else:
        for book_id, records in issued_books.items():
            if records:
                book_title = books.get(book_id, {}).get("title", "Unknown")
                print(f"\nBook: {book_title} (ID: {book_id})")
                print(f"{'Student':<20} {'Issue Date':<20} {'Due Date':<12} {'Status':<12}")
                print("-"*70)
                for rec in records:
                    status = "RETURNED" if rec["returned"] else "ACTIVE"
                    print(f"{rec['student_name'][:20]:<20} {rec['issue_date']:<20} {rec['due_date']:<12} {status:<12}")
                    if rec["returned"]:
                        print(f"{'':<20} Returned: {rec.get('return_date', '-')}")
    input("\nPress Enter to continue...")


def calculate_fine():
    print("\n" + "="*50)
    print("CHECK FINE")
    print("="*50)
    book_id = input("Enter Book ID: ").strip()
    student_name = input("Enter Student Name: ").strip()
    if book_id not in issued_books:
        print("No issued records for this book.")
        input("\nPress Enter to continue...")
        return
    found_active = False
    for rec in issued_books[book_id]:
        if rec["student_name"].lower() == student_name.lower() and not rec["returned"]:
            found_active = True
            due_date = datetime.strptime(rec["due_date"], "%Y-%m-%d")
            current_date = datetime.now()
            days_late = (current_date - due_date).days
            if days_late > 0:
                weeks_late = (days_late + 6) // 7
                fine = weeks_late * FINE_RATE_PER_WEEK
                print(f"\n⚠ OVERDUE BOOK")
                print(f"Student    : {student_name}")
                print(f"Book       : {books.get(book_id, {}).get('title', 'Unknown')}")
                print(f"Due Date   : {rec['due_date']}")
                print(f"Days Late  : {days_late}")
                print(f"Weeks Late : {weeks_late}")
                print(f"Fine Total : ${fine}")
            else:
                print(f"\n✓ No fine applicable.")
                print(f"Due Date : {rec['due_date']}")
                print(f"Days remaining: {-days_late}")
            break
    if not found_active:
        print("No active issue record found.")
    input("\nPress Enter to continue...")


def library_menu():
    while True:
        print("\n" + "="*60)
        print("📚 LIBRARY MANAGEMENT SYSTEM")
        print("="*60)
        print("Fine Policy: $10 per week (7 days) late return")
        print("Charged weekly, rounded up (e.g., 1-7 days = $10, 8-14 days = $20)")
        print("-"*60)
        print("1.  Add Book")
        print("2.  Show All Books")
        print("3.  Search Book")
        print("4.  Issue Book")
        print("5.  Return Book")
        print("6.  View Issued Books")
        print("7.  Check Fine")
        print("8.  Exit")
        print("-"*60)
        choice = input("Enter your choice (1-8): ").strip()
        if choice == "1":
            add_book()
        elif choice == "2":
            show_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            issue_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            show_issued_books()
        elif choice == "7":
            calculate_fine()
        elif choice == "8":
            print("\nThank you for using Library Management System!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    library_menu()
