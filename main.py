from library_system import LibrarySystem

def print_menu():
    print("\n===== UET Library Management System =====")
    print("1. Load books from CSV")
    print("2. Add new book")
    print("3. Search book by ISBN")
    print("4. Search book by Title")
    print("5. Search books by Author")
    print("6. Add member")
    print("7. Borrow book")
    print("8. Return book")
    print("9. List all books")
    print("10. Show member info")
    print("0. Exit")


def main():
    lib = LibrarySystem()
    
    # Load books and members at startup
    lib.load_books_from_csv("books.csv")
    lib.load_members_from_csv("members.csv")
    print("Books and members loaded successfully.")

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        # --------------------
        # Books
        # --------------------
        if choice == "1":
            lib.load_books_from_csv("books.csv")
            lib.load_members_from_csv("members.csv")
            print("Books and members loaded successfully.")

        elif choice == "2":
            ISBN = input("ISBN: ").strip()
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            year = int(input("Year: ").strip())
            category = input("Category: ").strip()
            copies = int(input("Copies: ").strip())

            if lib.add_book(ISBN, title, author, year, category, copies):
                lib.save_books()
                print("Book added and saved to CSV.")
            else:
                print("Book already exists.")

        elif choice == "3":
            ISBN = input("Enter ISBN: ").strip()
            book = lib.search_by_isbn(ISBN)
            print(book if book else "Book not found.")

        elif choice == "4":
            title = input("Enter title: ").strip()
            book = lib.search_by_title(title)
            print(book if book else "Book not found.")

        elif choice == "5":
            author = input("Enter author: ").strip()
            books = lib.search_by_author(author)
            if books:
                for b in books:
                    print(b)
            else:
                print("No books found.")

        # --------------------
        # Members
        # --------------------
        elif choice == "6":
            member_id = input("Member ID: ").strip()
            name = input("Name: ").strip()
            if lib.add_member(member_id, name):
                lib.save_members()
                print("Member added.")
            else:
                print("Member already exists.")

        elif choice == "7":
            member_id = input("Member ID: ").strip()
            ISBN = input("ISBN: ").strip()
            if lib.borrow_book(member_id, ISBN):
                lib.save_books()
                lib.save_members()
                print("Book borrowed.")
            else:
                print("Borrow failed.")

        elif choice == "8":
            member_id = input("Member ID: ").strip()
            ISBN = input("ISBN: ").strip()
            if lib.return_book(member_id, ISBN):
                lib.save_books()
                lib.save_members()
                print("Book returned.")
            else:
                print("Return failed.")

        elif choice == "9":
            books = lib.list_all_books()
            if books:
                for isbn, data in books:
                    print(f"{isbn} | {data['title']} | {data['author']} | {data['year']} | {data['category']} | Copies: {data['available_copies']}")
            else:
                print("No books in library.")

        elif choice == "10":
            member_id = input("Enter Member ID: ").strip()
            member = lib.members.get_member(member_id)
            if member:
                print(f"Name: {member.name}")
                if member.borrowed_books:
                    print("Borrowed books:")
                    for isbn in member.borrowed_books:
                        book = lib.books.search(isbn)
                        if book:
                            print(f"  {isbn} - {book.value['title']}")
                else:
                    print("No borrowed books.")
            else:
                print("Member not found.")

        elif choice == "0":
            print("Exiting system.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
