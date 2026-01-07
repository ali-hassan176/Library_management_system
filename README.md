# Backend Documentation - UET Library Management System

## 📁 Backend File Structure

```
backend/
├── avl.py              # AVL Tree implementation
├── hash.py             # Hash Table with chaining
├── hashes.py           # Secondary indexes (Author, Title, Members)
├── library_system.py   # Main library operations
└── main.py             # CLI interface (original)
```

---

## 🌳 1. AVL.PY - AVL Tree Implementation

### Purpose
Stores books using ISBN as the key in a self-balancing binary search tree for O(log n) operations.

### Classes

#### `Booknode`
```python
class Booknode:
    def __init__(self, ISBN, title, author, year, category, copies):
        self.key = ISBN              # Primary key
        self.value = {               # Book data
            'title': title,
            'author': author,
            'year': year,
            'category': category,
            'available_copies': copies
        }
        self.left = None             # Left child
        self.right = None            # Right child
        self.height = -1             # Node height (leaf = 0)
```

#### `AVLTree`
**Core Methods:**

1. **`insert(ISBN, value)`** - O(log n)
   - Inserts new book node
   - Auto-balances tree using rotations
   - Prevents duplicates

2. **`search(ISBN)`** - O(log n)
   - Binary search for book by ISBN
   - Returns node or None

3. **`inorder()`** - O(n)
   - Returns sorted list of all books
   - Traverses left → root → right

4. **Rotation Methods:**
   - `right_rotate(y)` - LL case
   - `left_rotate(x)` - RR case
   - Maintains AVL property (balance factor: -1, 0, 1)

### Balance Factor Calculation
```python
balance_factor = height(left) - height(right)
```

**Rebalancing Cases:**
- **LL:** `balance > 1` and `ISBN < left.key` → Right Rotate
- **RR:** `balance < -1` and `ISBN > right.key` → Left Rotate
- **LR:** `balance > 1` and `ISBN > left.key` → Left-Right Rotate
- **RL:** `balance < -1` and `ISBN < right.key` → Right-Left Rotate

---

## 🔗 2. HASH.PY - Hash Table with Chaining

### Purpose
Provides O(1) average-case lookup for secondary indexes.

### Class: `HashTable`

#### Hash Function
```python
def _hash(self, key):
    prime = 31
    hash_value = 0
    for char in key:
        hash_value = (hash_value * prime + ord(char)) % self.size
    return hash_value
```
**Polynomial rolling hash** - distributes keys uniformly.

#### Core Methods

1. **`insert(key, value)`** - O(1) average
   - Hashes key to index
   - Updates if exists, else inserts at head
   - Uses chaining for collision resolution

2. **`search(key)`** - O(1) average
   - Returns value or None
   - Linear search in chain

3. **`delete(key)`** - O(1) average
   - Removes node from chain
   - Returns True/False

---

## 📚 3. HASHES.PY - Secondary Indexes

### Classes

#### `AuthorIndex`
**Purpose:** Find all books by an author

```python
def add_book(author, isbn):
    # Normalizes author name (lowercase, trim spaces)
    # Stores list of ISBNs for each author
    # Example: "Nimra Ahmed" → [ISBN1, ISBN2, ISBN3]

def get_books(author):
    # Returns slist of ISBNs
```

**Data Structure:** `HashTable → author_name → slist(ISBNs)`

---

#### `TitleIndex`
**Purpose:** Find book by exact title

```python
def add_book(title, isbn):
    # Normalizes title (lowercase, trim spaces)
    # Maps title → single ISBN

def get_isbn(title):
    # Returns ISBN or None
```

**Data Structure:** `HashTable → book_title → ISBN`

---

#### `MemberDatabase`
**Purpose:** Store and manage library members

```python
class MemberNode:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []  # List of ISBNs
    
    def can_borrow(self):
        return len(self.borrowed_books) < 5  # Max 5 books
```

**Methods:**

1. **`add_member(member_id, name)`**
   - Creates new member
   - Returns False if exists

2. **`borrow_book(member_id, isbn)`**
   - Checks borrow limit (5 books)
   - Adds ISBN to member's list

3. **`return_book(member_id, isbn)`**
   - Removes ISBN from member's list

**Data Structure:** `HashTable → member_id → MemberNode`

---

## 🏛️ 4. LIBRARY_SYSTEM.PY - Main Library Operations

### Class: `LibrarySystem`

#### Initialization
```python
def __init__(self):
    self.books = AVLTree()              # Main book storage
    self.title_index = TitleIndex()     # Title → ISBN
    self.author_index = AuthorIndex()   # Author → ISBNs
    self.members = MemberDatabase()     # Member management
```

---

### 📖 Book Operations

#### `add_book(ISBN, title, author, year, category, copies)`

**Flow:**
1. Check if ISBN exists in AVL tree → Return False if duplicate
2. Create book data dictionary
3. **Insert into AVL tree** (primary storage)
4. **Add to title index** → `title_index.add_book(title, ISBN)`
5. **Add to author index** → `author_index.add_book(author, ISBN)`
6. Save to CSV if requested
7. Return True

**Time Complexity:** O(log n) for AVL + O(1) for hash tables

---

#### `search_by_isbn(ISBN)`

**Flow:**
```
User Input: ISBN
    ↓
AVLTree.search(ISBN)  [O(log n)]
    ↓
Returns: Booknode or None
    ↓
Extract: node.value (book dictionary)
    ↓
Return: [book_dict] or []
```

**Code Path:**
```python
library_system.py:95  → search_by_isbn()
    ↓
avl.py:65            → AVLTree.search()
    ↓
avl.py:68-72         → Binary search recursion
```

---

#### `search_by_title(title)`

**Flow:**
```
User Input: "Clean Code"
    ↓
title_index.normalize(title)  → "clean code"
    ↓
title_index.get_isbn("clean code")  [O(1)]
    ↓
HashTable.search("clean code")  → Returns ISBN
    ↓
AVLTree.search(ISBN)  [O(log n)]
    ↓
Returns: [book_dict] or []
```

**Code Path:**
```python
library_system.py:99  → search_by_title()
    ↓
hashes.py:67         → TitleIndex.get_isbn()
    ↓
hash.py:44           → HashTable.search()
    ↓
avl.py:65            → AVLTree.search()
```

**Time Complexity:** O(1) for hash lookup + O(log n) for AVL

---

#### `search_by_author(author)`

**Flow:**
```
User Input: "Nimra Ahmed"
    ↓
author_index.normalize(author)  → "nimra ahmed"
    ↓
author_index.get_books_list("nimra ahmed")  [O(1)]
    ↓
Returns: List of ISBNs [ISBN1, ISBN2, ISBN3]
    ↓
For each ISBN:
    AVLTree.search(ISBN)  [O(log n)]
    ↓
Collect all book dictionaries
    ↓
Returns: [book1_dict, book2_dict, book3_dict]
```

**Code Path:**
```python
library_system.py:105 → search_by_author()
    ↓
hashes.py:38         → AuthorIndex.get_books_list()
    ↓
hashes.py:35         → AuthorIndex.get_books()
    ↓
hash.py:44           → HashTable.search()
    ↓
(For each ISBN found)
avl.py:65            → AVLTree.search()
```

**Time Complexity:** O(1) + O(k log n) where k = books by author

---

### 👥 Member Operations

#### `add_member(member_id, name)`

**Flow:**
```
User Input: "2024-EE-200", "Ali Hassan"
    ↓
MemberDatabase.add_member()
    ↓
Check if member exists in hash table  [O(1)]
    ↓
If not exists:
    Create MemberNode
    Insert into hash table
    Return True
Else:
    Return False
```

**Code Path:**
```python
library_system.py:113 → add_member()
    ↓
hashes.py:53         → MemberDatabase.add_member()
    ↓
hash.py:30           → HashTable.insert()
```

---

#### `borrow_book(member_id, ISBN)`

**Flow:**
```
User Input: "2024-EE-176", "9780134093413"
    ↓
1. Search book in AVL tree  [O(log n)]
    ↓
2. Check if available_copies > 0
    ↓
3. Get member from hash table  [O(1)]
    ↓
4. Check if member.can_borrow() (< 5 books)
    ↓
5. member.borrowed_books.append(ISBN)
    ↓
6. book.available_copies -= 1
    ↓
7. Save to CSV
    ↓
Return: True/False
```

**Code Path:**
```python
library_system.py:119 → borrow_book()
    ↓
avl.py:65            → AVLTree.search(ISBN)
    ↓
hashes.py:66         → MemberDatabase.borrow_book()
    ↓
hashes.py:47         → MemberNode.can_borrow()
    ↓
hashes.py:70         → member.borrowed_books.append()
    ↓
library_system.py:123 → book.value['available_copies'] -= 1
```

**Time Complexity:** O(log n) + O(1)

---

#### `return_book(member_id, ISBN)`

**Flow:**
```
User Input: "2024-EE-176", "9780134093413"
    ↓
1. Search book in AVL tree  [O(log n)]
    ↓
2. Get member from hash table  [O(1)]
    ↓
3. Check if ISBN in member.borrowed_books
    ↓
4. member.borrowed_books.remove(ISBN)
    ↓
5. book.available_copies += 1
    ↓
6. Save to CSV
    ↓
Return: True/False
```

**Code Path:**
```python
library_system.py:128 → return_book()
    ↓
avl.py:65            → AVLTree.search(ISBN)
    ↓
hashes.py:73         → MemberDatabase.return_book()
    ↓
hashes.py:78         → member.borrowed_books.remove(ISBN)
    ↓
library_system.py:132 → book.value['available_copies'] += 1
```

---

### 💾 CSV Operations

#### `save_books(filepath="books.csv")`

**Flow:**
```python
1. books.inorder()  → Get sorted list of all books  [O(n)]
    ↓
2. Open CSV file for writing
    ↓
3. Write header row
    ↓
4. For each (isbn, data) in books:
       Write: ISBN, Title, Author, Year, Category, TotalCopies
    ↓
5. Close file
```

---

#### `load_books_from_csv(filepath)`

**Flow:**
```python
1. Open CSV file
    ↓
2. Read using csv.DictReader
    ↓
3. For each row:
       add_book(
           ISBN, Title, Author, Year, Category, TotalCopies,
           save=False  # Don't rewrite CSV during load
       )
    ↓
4. This populates:
   - AVL tree (books)
   - Title index
   - Author index
```

---

## 🖥️ 5. MAIN.PY - CLI Interface

### Menu Options Flow

#### Option 1: Load books from CSV
```
main.py:31 → lib.load_books_from_csv("books.csv")
    ↓
library_system.py:72 → load_books_from_csv()
    ↓
(For each row in CSV)
library_system.py:32 → add_book()
```

#### Option 3: Search book by ISBN
```
main.py:43 → ISBN input
    ↓
main.py:44 → lib.search_by_isbn(ISBN)
    ↓
library_system.py:95 → search_by_isbn()
    ↓
avl.py:65 → AVLTree.search()
```

#### Option 7: Borrow book
```
main.py:63 → member_id, ISBN input
    ↓
main.py:65 → lib.borrow_book(member_id, ISBN)
    ↓
library_system.py:119 → borrow_book()
    ↓
(Updates AVL tree + Member hash table)
    ↓
main.py:66-68 → Save both books.csv and members.csv
```

---

## 📊 Time Complexity Summary

| Operation | AVL Tree | Hash Table | Total |
|-----------|----------|------------|-------|
| Add Book | O(log n) | O(1) | O(log n) |
| Search ISBN | O(log n) | - | O(log n) |
| Search Title | O(log n) | O(1) | O(log n) |
| Search Author | O(k log n) | O(1) | O(k log n) |
| Add Member | - | O(1) | O(1) |
| Borrow Book | O(log n) | O(1) | O(log n) |
| Return Book | O(log n) | O(1) | O(log n) |
| List All Books | O(n) | - | O(n) |

*k = number of books by author*

---

## 🔄 Data Flow Example: Borrow a Book

```
User wants to borrow "Clean Code" (ISBN: 9780132350884)

Step 1: User enters Member ID and ISBN
    ↓
Step 2: main.py receives input
    ↓
Step 3: Calls lib.borrow_book("2024-EE-176", "9780132350884")
    ↓
Step 4: library_system.py → borrow_book()
    |
    ├→ AVLTree.search("9780132350884")  [Find book node]
    |   ↓
    |   Binary search in AVL tree
    |   ↓
    |   Returns Booknode
    |
    ├→ Check: book.value['available_copies'] > 0?
    |   ↓
    |   If NO → Return False
    |
    ├→ MemberDatabase.get_member("2024-EE-176")
    |   ↓
    |   HashTable.search("2024-EE-176")  [Hash function → index → chain search]
    |   ↓
    |   Returns MemberNode
    |
    ├→ Check: member.can_borrow()?  [len(borrowed_books) < 5]
    |   ↓
    |   If NO → Return False
    |
    ├→ member.borrowed_books.append("9780132350884")
    |   ↓
    |   Updates member's list in hash table
    |
    ├→ book.value['available_copies'] -= 1
    |   ↓
    |   Updates book node in AVL tree
    |
    └→ Save changes to CSV files
        ↓
        Return True

Step 5: main.py displays success message
```

---

## 🎯 Key Design Decisions

### 1. **Why AVL Tree for Books?**
- **Sorted access:** Inorder traversal gives alphabetically sorted ISBNs
- **Balanced operations:** Guaranteed O(log n) for all operations
- **No collisions:** Unlike hash tables, no collision resolution needed

### 2. **Why Hash Tables for Indexes?**
- **Fast lookups:** O(1) average case for title/author search
- **Space efficient:** Only stores references (ISBNs), not full book data
- **Flexible:** Can handle multiple books per author (slist)

### 3. **Why Separate Indexes?**
- **Multiple access patterns:** Search by ISBN, title, or author
- **Query optimization:** Direct hash lookup vs tree traversal
- **Data integrity:** Single source of truth (AVL tree), multiple views

### 4. **Why CSV Storage?**
- **Human-readable:** Easy to inspect and edit
- **Simple persistence:** No database setup required
- **Educational:** Clear demonstration of data structures

---

## 🔧 Backend Limitations & Improvements

### Current Limitations:
1. **No transaction support** - Partial failures not handled
2. **In-memory only** - Changes lost if program crashes before save
3. **No data validation** - Invalid data can be inserted
4. **Fixed borrow limit** - Hardcoded to 5 books

### Potential Improvements:
1. Add database backend (SQLite/PostgreSQL)
2. Implement logging for debugging
3. Add data validation layer
4. Support soft deletes (mark as deleted vs actual deletion)
5. Add book reservation system
6. Implement due dates and fine calculation

---

## 📝 Testing the Backend

```python
# Test script
from library_system import LibrarySystem

lib = LibrarySystem()

# Test 1: Add book
lib.add_book("TEST123", "Test Book", "Test Author", 2024, "Science", 5)

# Test 2: Search by ISBN
result = lib.search_by_isbn("TEST123")
print(result)  # Should print book dictionary

# Test 3: Search by title
result = lib.search_by_title("Test Book")
print(result)  # Should print book dictionary

# Test 4: Add member
lib.add_member("TEST-001", "Test User")

# Test 5: Borrow book
success = lib.borrow_book("TEST-001", "TEST123")
print(success)  # Should print True

# Test 6: Check member
member = lib.members.get_member("TEST-001")
print(member.borrowed_books)  # Should contain ["TEST123"]
```

---

**End of Backend Documentation**
