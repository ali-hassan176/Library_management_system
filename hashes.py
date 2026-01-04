from hash import HashTable
from avl import AVLTree
class LinkedlistNode:
    def __init__(self, value):
        self.data = value     # stores the value of the node
        self.next = None      # pointer to the next node

class slist:
    def __init__(self):
        self.head = None
        self.n = 0
    def __len__(self):
        return self.n

    def insert_head(self, value):
        new_node = LinkedlistNode(value)
        new_node.next = self.head
        self.head = new_node
        self.n += 1

    def contains(self, value):
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


class AuthorIndex:
    def __init__(self):
        self.table = HashTable()

    def normalize(self, name):
        return " ".join(name.lower().split())

    def add_book(self, author, isbn):
        author = self.normalize(author)

        isbn_list = self.table.search(author)

        if isbn_list is None:
            isbn_list = slist()

        if not isbn_list.contains(isbn):
            isbn_list.insert_head(isbn)

        self.table.insert(author, isbn_list)

    def get_books(self, author):
        author = self.normalize(author)
        return self.table.search(author)  # returns slist
    def get_books_list(self, author):
        s_list = self.get_books(author)
        return s_list.to_list() if s_list else []

class MemberNode:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []  # list of ISBNs

    def can_borrow(self):
        return len(self.borrowed_books) < 5

class MemberDatabase:
    def __init__(self):
        self.table = HashTable()

    def add_member(self, member_id, name):
        if self.table.search(member_id) is not None:
            return False  # already exists

        member = MemberNode(member_id, name)
        self.table.insert(member_id, member)
        return True

    def get_member(self, member_id):
        return self.table.search(member_id)

    def borrow_book(self, member_id, isbn):
        member = self.get_member(member_id)

        if member is None:
            return False

        if not member.can_borrow():
            return False

        member.borrowed_books.append(isbn)
        return True

    def return_book(self, member_id, isbn):
        member = self.get_member(member_id)

        if member is None or isbn not in member.borrowed_books:
            return False

        member.borrowed_books.remove(isbn)
        return True
    def table_items(self):
        """Yield (member_id, MemberNode) for all members."""
        for bucket in self.table.table:
            current = bucket
            while current:
                yield current.key, current.value
                current = current.next

class TitleIndex:
    def __init__(self):
        self.table = HashTable()

    def normalize(self, title):
        return " ".join(title.lower().split())

    def add_book(self, title, isbn):
        title = self.normalize(title)
        self.table.insert(title, isbn)

    def remove_book(self, title):
        title = self.normalize(title)
        self.table.delete(title)

    def get_isbn(self, title):
        title = self.normalize(title)
        return self.table.search(title)
    def exists(self, title):
        return self.get_isbn(title) is not None
