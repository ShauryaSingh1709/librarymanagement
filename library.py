books = {
    "A001": {"title": "Naruto Vol.1", "author": "Masashi Kishimoto", "quantity": 5},
    "A002": {"title": "One Piece Vol.1", "author": "Eiichiro Oda", "quantity": 4},
    "A003": {"title": "Attack on Titan Vol.1", "author": "Hajime Isayama", "quantity": 6},
    "A004": {"title": "Demon Slayer Vol.1", "author": "Koyoharu Gotouge", "quantity": 3},
    "A005": {"title": "My Hero Academia Vol.1", "author": "Kohei Horikoshi", "quantity": 4},
    "A006": {"title": "Death Note Vol.1", "author": "Tsugumi Ohba", "quantity": 3},
    "A007": {"title": "Fullmetal Alchemist Vol.1", "author": "Hiromu Arakawa", "quantity": 2},
    "A008": {"title": "Jujutsu Kaisen Vol.1", "author": "Gege Akutami", "quantity": 5},
    "A009": {"title": "Tokyo Ghoul Vol.1", "author": "Sui Ishida", "quantity": 3},
    "A010": {"title": "Hunter x Hunter Vol.1", "author": "Yoshihiro Togashi", "quantity": 2}
}

issued_books = {}
FINE_PER_WEEK = 10

def add_book():
    print()
    book_id = input("Enter Book ID: ")
    if book_id in books:
        print("Book ID already exists!")
        return
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    qty = int(input("Enter Quantity: "))
    books[book_id] = {"title": title, "author": author, "quantity": qty}
    print(f"{title} added!")

def show_books():
    print()
    print("=== AVAILABLE BOOKS ===")
    print(f"{'ID':<8}{'Title':<25}{'Author':<20}{'Qty':<6}")
    print("-" * 60)
    for book_id, info in books.items():
        print(f"{book_id:<8}{info['title']:<25}{info['author']:<20}{info['quantity']:<6}")

def search_book():
    print()
    kw = input("Search title/author: ").lower()
    found = 0
    for book_id, info in books.items():
        if kw in info["title"].lower() or kw in info["author"].lower():
            print(f"{book_id}: {info['title']} by {info['author']} (Qty: {info['quantity']})")
            found = 1
    if not found:
        print("No books found!")

def issue_book():
    print()
    book_id = input("Enter Book ID: ")
    if book_id not in books:
        print("Book not found!")
        return
    if books[book_id]["quantity"] <= 0:
        print("No copies available!")
        return
    name = input("Student Name: ")
    days = int(input("Days (max 30): "))
    issue = __import__("datetime").datetime.now()
    due = issue + __import__("datetime").timedelta(days=days)
    if book_id not in issued_books:
        issued_books[book_id] = []
    issued_books[book_id].append({"student": name, "issue": issue.strftime("%Y-%m-%d"), "due": due.strftime("%Y-%m-%d"), "returned": False})
    books[book_id]["quantity"] -= 1
    print(f"Issued! Due: {due.strftime('%Y-%m-%d')}")

def return_book():
    print()
    book_id = input("Enter Book ID: ")
    name = input("Student Name: ")
    if book_id not in issued_books:
        print("No records!")
        return
    for rec in issued_books[book_id]:
        if rec["student"] == name and not rec["returned"]:
            rec["returned"] = True
            rec["return_date"] = __import__("datetime").datetime.now().strftime("%Y-%m-%d")
            books[book_id]["quantity"] += 1
            due = __import__("datetime").datetime.strptime(rec["due"], "%Y-%m-%d")
            ret = __import__("datetime").datetime.strptime(rec["return_date"], "%Y-%m-%d")
            late = (ret - due).days
            if late > 0:
                weeks = (late + 6) // 7
                fine = weeks * FINE_PER_WEEK
                print(f"Late {late} days. Fine: ${fine}")
            else:
                print("Returned on time!")
            return
    print("No active issue found!")

def show_issued():
    print()
    print("=== ISSUED BOOKS ===")
    for book_id, recs in issued_books.items():
        for r in recs:
            status = "RETURNED" if r["returned"] else "ACTIVE"
            title = books.get(book_id, {}).get("title", book_id)
            print(f"{title} - {r['student']} - {r['issue']} to {r['due']} [{status}]")

def check_fine():
    print()
    book_id = input("Book ID: ")
    name = input("Student Name: ")
    if book_id not in issued_books:
        print("No records!")
        return
    for rec in issued_books[book_id]:
        if rec["student"] == name and not rec["returned"]:
            rec["returned"] = True
            rec["return_date"] = __import__("datetime").datetime.now().strftime("%Y-%m-%d")
            books[book_id]["quantity"] += 1
            due = __import__("datetime").datetime.strptime(rec["due"], "%Y-%m-%d")
            ret = __import__("datetime").datetime.strptime(rec["return_date"], "%Y-%m-%d")
            late = (ret - due).days
            if late > 0:
                weeks = (late + 6) // 7
                fine = weeks * FINE_PER_WEEK
                print(f"Days late: {late}. Fine: ${fine}")
            else:
                print(f"On time. {-late} days left.")
            return
    print("No active record!")

def main():
    while True:
        print()
        print("=== ANIME LIBRARY SYSTEM ===")
        print("1. Add Book  2. Show Books  3. Search  4. Issue  5. Return  6. Issued  7. Fine  8. Exit")
        ch = input("Choice: ")
        if ch == "1": add_book()
        elif ch == "2": show_books()
        elif ch == "3": search_book()
        elif ch == "4": issue_book()
        elif ch == "5": return_book()
        elif ch == "6": show_issued()
        elif ch == "7": check_fine()
        elif ch == "8": print("Bye!"); break
        else: print("Invalid!")

main()
