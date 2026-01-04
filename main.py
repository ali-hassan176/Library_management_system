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
    print("0. Exit")


def main():
    lib = LibrarySystem()

    while True:
        print_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            lib.load_books_from_csv("books.csv")
            print("Books loaded successfully.")

        elif choice == "2":
            ISBN = input("ISBN: ")
            title = input("Title: ")
            author = input("Author: ")
            year = int(input("Year: "))
            category = input("Category: ")
            copies = int(input("Copies: "))

            if lib.add_book(ISBN, title, author, year, category, copies):
                print("Book added and saved to CSV.")
            else:
                print("Book already exists.")

        elif choice == "3":
            ISBN = input("Enter ISBN: ")
            book = lib.search_by_isbn(ISBN)
            print(book if book else "Book not found.")

        elif choice == "4":
            title = input("Enter title: ")
            book = lib.search_by_title(title)
            print(book if book else "Book not found.")

        elif choice == "5":
            author = input("Enter author: ")
            books = lib.search_by_author(author)
            if books:
                for b in books:
                    print(b)
            else:
                print("No books found.")

        elif choice == "6":
            member_id = input("Member ID: ")
            name = input("Name: ")
            if lib.add_member(member_id, name):
                print("Member added.")
            else:
                print("Member already exists.")

        elif choice == "7":
            member_id = input("Member ID: ")
            ISBN = input("ISBN: ")
            if lib.borrow_book(member_id, ISBN):
                print("Book borrowed.")
            else:
                print("Borrow failed.")

        elif choice == "8":
            member_id = input("Member ID: ")
            ISBN = input("ISBN: ")
            if lib.return_book(member_id, ISBN):
                print("Book returned.")
            else:
                print("Return failed.")

        elif choice == "9":
            for isbn, data in lib.list_all_books():
                print(isbn, data)

        elif choice == "0":
            print("Exiting system.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
