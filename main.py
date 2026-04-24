books = [
    "Naruto Vol.1",
    "One Piece Vol.1",
    "Attack on Titan Vol.1",
]
issued_books = []
def add_book():
    book = input("Enter the name of the book: ")
    books.append(book)
    print(f"{book} has been added to the library.")
def show_books():
    if len(books) == 0:
        print("No books are available in the library.")
    else:
        print("Available books:")
        for b in books:
            print(b)
def issue_book():
    book = input("Enter the name of the book to issue:")
    if book in books:
        books.remove(book)
        issued_books.append(book)
        print(f"{book} has been issued to you.")
    else:
        print(f"{book} is not available in the library.")
def return_book():
    book = input("Enter the name of the book to return: ")
    if book in issued_books:
        issued_books.remove(book)
        books.append(book)
        print(f"{book} has been returned to the library.")
    else:
        print(f"{book} was not issued from the library.")
def library():
    while True:
        print("LIBRARY MANAGEMENT SYSTEM")
        print("1. ADD BOOK")
        print("2. SHOW BOOKS")
        print("3. ISSUE BOOK")
        print("4. RETURN BOOK")
        print("5. EXIT")
        choice = int(input("Enter your choice: ")) 
        if choice == 1:
            add_book()
        elif choice == 2:
            show_books()
        elif choice == 3:
            issue_book()
        elif choice == 4:
            return_book()
        elif choice == 5:
            print("Thank you for using the Library Management System. Visit again!")
            break
        else:
            print("Invalid choice. Please try again.")
library()
