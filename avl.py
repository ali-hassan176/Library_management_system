# =========================
# AVL Tree Implementation
# Empty node height = -1
# Leaf height = 0
# =========================

class Booknode:
    def __init__(self, ISBN, title, author, year, category, copies):
        self.key = ISBN
        self.value = {
            'title': title,
            'author': author,
            'year': year,
            'category': category,       
            'available_copies': copies
        }
        self.left = None
        self.right = None
        self.height = -1  # Empty node height = -1

class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def height(self, node):
        return node.height if node else -1

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    # Rotations
    def right_rotate(self, y):
        x = y.left
        B = x.right
        x.right = y
        y.left = B
        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        y = x.right
        B = y.left
        y.left = x
        x.right = B
        self.update_height(x)
        self.update_height(y)
        return y

    # Insert
    def insert(self, ISBN, value):
        self.root = self._insert(self.root, ISBN, value)

    def _insert(self, node, ISBN, value):
        if not node:
            self.size += 1
            return Booknode(
                ISBN,
                value['title'],
                value['author'],
                value['year'],
                value['category'],
                value['available_copies']
            )

        if ISBN < node.key:
            node.left = self._insert(node.left, ISBN, value)
        elif ISBN > node.key:
            node.right = self._insert(node.right, ISBN, value)
        else:
            return node  # No duplicates

        self.update_height(node)
        balance = self.balance_factor(node)

        # LL
        if balance > 1 and ISBN < node.left.key:
            return self.right_rotate(node)
        # RR
        if balance < -1 and ISBN > node.right.key:
            return self.left_rotate(node)
        # LR
        if balance > 1 and ISBN > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # RL
        if balance < -1 and ISBN < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    # Search
    def search(self, ISBN):
        return self._search(self.root, ISBN)

    def _search(self, node, ISBN):
        if not node or node.key == ISBN:
            return node
        if ISBN < node.key:
            return self._search(node.left, ISBN)
        return self._search(node.right, ISBN)

    # Inorder
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)
