# =========================
# Hash Table with Chaining
# =========================

class HashNode:
    def __init__(self, key, value):
        self.key = key          # key (string)
        self.value = value      # value (any object)
        self.next = None        # next node in chain


class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size

    # ---------------------
    # Hash Function
    # ---------------------
    def _hash(self, key):
        """
        Polynomial rolling hash for strings
        """
        prime = 31
        hash_value = 0
        for char in key:
            hash_value = (hash_value * prime + ord(char)) % self.size
        return hash_value

    # ---------------------
    # Insert / Update
    # ---------------------
    def insert(self, key, value):
        index = self._hash(key)
        head = self.table[index]

        # If key already exists → update
        current = head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # Insert new node at head (chaining)
        new_node = HashNode(key, value)
        new_node.next = head
        self.table[index] = new_node

    # ---------------------
    # Search
    # ---------------------
    def search(self, key):
        index = self._hash(key)
        current = self.table[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        return None  # key not found

    # ---------------------
    # Delete
    # ---------------------
    def delete(self, key):
        index = self._hash(key)
        current = self.table[index]
        prev = None

        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                return True  # deleted successfully
            prev = current
            current = current.next

        return False  # key not found
