"""
Task5: Favorite Books and Student Database

This module demonstrates basic data handling and formatting in Python.
It works with two main data structures:

1. `favorite_books` (list of dicts)
   - Stores a list of books with their titles and authors.
   - Example element: {"title": "The Way of Kings", "author": "Brandon Sanderson"}

2. `student_database` (dict of dicts)
   - Stores students with unique ID numbers as keys and a dictionary containing
     student information (currently only "name") as values.
   - Example element: 100: {"name": "Alice"}

Functions
---------
find_first_three_books()
    Returns the first three books formatted as "Book {n}: {title}, Author: {author}".

get_student_name(student_id)
    Returns the name of a student for a given ID. Returns None if the ID is not found.

main()
    Prints the first three books and a list of all student names.
    Serves as the entry point when running the module as a script.
"""

favorite_books = [
    {"title": "The Way of Kings", "author": "Brandon Sanderson"},
    {"title": "The Wise Man's Fear", "author": "Patrick Rothfuss"},
    {"title": "The Crippled God", "author": "Steven Erikson"},
    {"title": "The Fifth Season", "author": "N.K. Jemisin"},
    {"title": "The Name of the Wind", "author": "Patrick Rothfuss"},
    {"title": "The Broken Earth Trilogy", "author": "N.K. Jemisin"},
    {"title": "The Night Circus", "author": "Erin Morgenstern"},
    {"title": "The Starless Sea", "author": "Erin Morgenstern"},
    {"title": "The Shadow of What Was Lost", "author": "James Islington"},
    {"title": "The Black Prism", "author": "Brent Weeks"}
]

student_database = {
    100: {"name": "Alice"},
    101: {"name": "Bob"},
    102: {"name": "Charlie"},
    103: {"name": "Diana"},
    104: {"name": "Ethan"},
    105: {"name": "Fiona"},
    106: {"name": "George"},
    107: {"name": "Hannah"},
    108: {"name": "Ian"},
    109: {"name": "Julia"}
}

def find_first_three_books():
    """
    Return the first three books in a formatted string list.

    Returns
    -------
    list of str
        Each string is formatted as "Book {n}: {title}, Author: {author}".
    """
    first_three_books = []
    for i, book in enumerate(favorite_books[:3], start=1):
        first_three_books.append(f"Book {i}: {book['title']}, Author: {book['author']}")
    return first_three_books

# Access student data
def get_student_name(student_id):
    """Return the student name for a given ID."""
    return student_database.get(student_id, {}).get("name")
  

if __name__ == "__main__":
    # Print books
    for line in find_first_three_books():
        print(line)
    
    # Print students
    print("All students: ") 
    for line in [student["name"] for student in student_database.values()]:
        print(line)