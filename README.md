# 📚 Anime Library Management System

A simple command-line and GUI library management system built with Python using dictionary-based book records. Designed for college projects with clean, readable code.

## Features

- **Dictionary-Based Storage** - All book records stored in dictionaries for efficient O(1) lookup
- **Two Interfaces** - Command-line (`library.py`) and GUI (`gui.py`) versions
- **Book Management** - Add, view, and search anime/manga titles
- **Issue System** - Track issued books with student names, issue dates, and due dates
- **Fine Calculation** - Automatic **$10/week** late fee (rounded up) for overdue returns
- **Anime Dataset** - Pre-loaded with 10 popular anime/manga titles

## Files

- `library.py` - Command-line version (simple, clean code)
- `gui.py` - GUI version with Tkinter (modern dark theme)
- `main.py` - Original list-based version (for comparison)

## How to Run

### Command-Line Version
```bash
python library.py
```

### GUI Version
```bash
python gui.py
```

## Requirements

- Python 3.x
- Tkinter (included with standard Python installation)

## Sample Dataset

Pre-loaded with popular anime/manga titles:

| ID | Title | Author | Copies |
|----|-------|--------|--------|
| A001 | Naruto Vol.1 | Masashi Kishimoto | 5 |
| A002 | One Piece Vol.1 | Eiichiro Oda | 4 |
| A003 | Attack on Titan Vol.1 | Hajime Isayama | 6 |
| A004 | Demon Slayer Vol.1 | Koyoharu Gotouge | 3 |
| A005 | My Hero Academia Vol.1 | Kohei Horikoshi | 4 |
| A006 | Death Note Vol.1 | Tsugumi Ohba | 3 |
| A007 | Fullmetal Alchemist Vol.1 | Hiromu Arakawa | 2 |
| A008 | Jujutsu Kaisen Vol.1 | Gege Akutami | 5 |
| A009 | Tokyo Ghoul Vol.1 | Sui Ishida | 3 |
| A010 | Hunter x Hunter Vol.1 | Yoshihiro Togashi | 2 |

## Menu Options (CLI)

- **1. Add Book** - Add new anime/manga to the library
- **2. Show Books** - Display all available books with quantities
- **3. Search** - Find books by title or author
- **4. Issue** - Issue a book to a student (with due date tracking)
- **5. Return** - Process book returns (calculates late fees automatically)
- **6. Issued Books** - View all currently issued books
- **7. Check Fine** - Check outstanding fines for a student
- **8. Exit** - Close the program

## Fine Policy

- **$10 per week** (7 days) late fee
- Rounded up: 1-7 days late = $10, 8-14 days = $20, etc.
- Calculated automatically on book return

## Code Structure

### Dictionary-Based Design

```python
books = {
    "A001": {
        "title": "Naruto Vol.1",
        "author": "Masashi Kishimoto",
        "quantity": 5
    }
}

issued_books = {
    "A001": [
        {
            "student_name": "John Doe",
            "issue_date": "2026-04-25",
            "due_date": "2026-05-09",
            "returned": False
        }
    ]
}
```

**Why dictionaries?**
- **O(1) lookup speed** - Finding a book by ID is instant
- **Unique keys** - Each book ID is unique, preventing duplicates
- **Nested data** - Title, author, quantity stored together
- **Efficient updates** - `books[book_id]["quantity"] -= 1` is direct

### Key Variables

- `book_id` - Dictionary key for each book (e.g., "A001")
- `info` - Dictionary value containing book details
- `rec` - Individual issue record in issued_books list
- `kw` - Search **keyword** (short for keyword) used in search functions

## Search Function Explanation

**Why use `kw` for keyword?**

`kw` is a common convention short for **"keyword"** — the search term entered by the user. It's widely used in codebases for search queries:

```python
def search_book():
    kw = input("Search: ").lower()  # kw = keyword
    for book_id, info in books.items():
        if kw in info["title"].lower():  # Check if keyword matches
            print(info["title"])
```

It's concise, clear, and follows standard naming conventions (like `txt` for text, `msg` for message).

## Project Notes

This project demonstrates:
- Dictionary data structures for efficient data management
- Date/time handling with `datetime` module
- Menu-driven program flow
- CRUD operations (Create, Read, Update, Delete)
- Fine calculation logic with progressive weekly charges
- Separation of concerns (CLI vs GUI interfaces)

## License

MIT License
