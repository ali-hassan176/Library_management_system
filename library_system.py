from avl import AVLTree
from hashes import TitleIndex, AuthorIndex, MemberDatabase
import csv

class LibrarySystem:
    def __init__(self):
        self.books = AVLTree()
        self.title_index = TitleIndex()
        self.author_index = AuthorIndex()
        self.members = MemberDatabase()
    def load_members_from_csv(self, filepath="members.csv"):
        try:
            with open(filepath, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.members.add_member(row["MemberID"], row["Name"])
                    member = self.members.get_member(row["MemberID"])
                    if row["BorrowedBooks"]:
                        member.borrowed_books = row["BorrowedBooks"].split(";")
        except FileNotFoundError:
            # No members.csv yet, that's fine
            pass

    # --------------------
    # Save members to CSV
    # --------------------
    def save_members(self, filepath="members.csv"):
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["MemberID", "Name", "BorrowedBooks"])
            for member_id, member in self.members.table_items():
                borrowed = ";".join(member.borrowed_books)
                writer.writerow([member_id, member.name, borrowed])
    # --------------------
    # Add a book
    # --------------------
    def add_book(self, ISBN, title, author, year, category, copies, save=True):
        if self.books.search(ISBN):
            return False

        book_data = {
            'title': title,
            'author': author,
            'year': year,
            'category': category,
            'available_copies': copies
        }

        self.books.insert(ISBN, book_data)
        self.title_index.add_book(title, ISBN)
        self.author_index.add_book(author, ISBN)

        if save:
            self.save_books("books.csv")
        return True

    # --------------------
    # Save books to CSV
    # --------------------
    def save_books(self, filepath="books.csv"):
        books = self.books.inorder()
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ISBN", "Title", "Author", "Year", "Category", "TotalCopies"])
            for isbn, data in books:
                writer.writerow([
                    isbn,
                    data.get('title', ''),
                    data.get('author', ''),
                    data.get('year', ''),
                    data.get('category', ''),
                    data.get('available_copies', '')
                ])

    # --------------------
    # Load books from CSV
    # --------------------
    def load_books_from_csv(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_book(
                    row['ISBN'],
                    row['Title'],
                    row['Author'],
                    int(row['Year']),
                    row['Category'],
                    int(row['TotalCopies']),
                    save=False  # avoid overwriting CSV
                )

    # --------------------
    # Search operations
    # --------------------
    def search_by_isbn(self, ISBN):
        node = self.books.search(ISBN)
        return node.value if node else None

    def search_by_title(self, title):
        isbn = self.title_index.get_isbn(title)
        if not isbn:
            return None
        node = self.books.search(isbn)
        return node.value if node else None

    def search_by_author(self, author):
        isbns = self.author_index.get_books_list(author)
        return [self.books.search(isbn).value for isbn in isbns if self.books.search(isbn)]

    # --------------------
    # Members
    # --------------------
    def add_member(self, member_id, name):
        return self.members.add_member(member_id, name)

    # --------------------
    # Borrow / Return
    # --------------------
    def borrow_book(self, member_id, ISBN):
        book_node = self.books.search(ISBN)
        if not book_node or book_node.value['available_copies'] <= 0:
            return False
        if not self.members.borrow_book(member_id, ISBN):
            return False
        book_node.value['available_copies'] -= 1
        return True

    def return_book(self, member_id, ISBN):
        book_node = self.books.search(ISBN)
        if not book_node:
            return False
        if not self.members.return_book(member_id, ISBN):
            return False
        book_node.value['available_copies'] += 1
        return True

    # --------------------
    # List all books
    # --------------------
    def list_all_books(self):
        return self.books.inorder()
