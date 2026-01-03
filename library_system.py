from hash import HashTable
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
class Membernode():
    def __init__(self,member_id,name):
        self.memberid=member_id
        self.name = name
        self.borrowed_books = []
    def can_borrow(self):
        return len(self.borrowed_books)<5
class Member():
    def __init__(self):
        self.table = HashTable()
    def insertion(self):
        pass
    