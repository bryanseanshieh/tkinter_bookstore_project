import sqlite3

def connect():
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    lcCreate = '''CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                year INTEGER,
                ISBN TEXT
        ) '''
    cur.execute(lcCreate)
    conn.commit()
    conn.close()
    return

def add_entry(title, author, year, isbn):
    # Add entry for a book.
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO book values (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
    conn.commit()
    conn.close()
    return

def filter(title = "", author = "", year = 2000, isbn = ""):
    # Set default parameters as only subsets of the search criteria may be utilized.
    if len(title) > 0:
        lctitle = "%" + title.lower() + "%"
    else:
        lctitle = title

    if len(author) > 0:
        lcauthor = "%" + author.lower() + "%"
    else:
        lcauthor = author

    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    lcSearch = '''SELECT *
                    FROM book
                    WHERE lower(title) like ?
                        OR lower(author) like ?
                        OR year = ?
                        OR ISBN = ?
                    ORDER BY author, title
        '''
    cur.execute(lcSearch, (lctitle, lcauthor, year, isbn))
    bookinfo = cur.fetchall()
    conn.close()
    return bookinfo

def update_info(id, title, author, year, isbn):
    # Update information for selected book entry. The actual criteria uses id to locate entry.
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    lcUpdate = '''UPDATE book
                    SET title = ?,
                        author = ?,
                        year = ?,
                        isbn = ?
                    WHERE id = ?
    '''
    print(lcUpdate)
    cur.execute(lcUpdate, (title, author, year, isbn, id))
    conn.commit()
    conn.close()
    return

def delete_entry(id):
    # Delete selected book entry. The actual criteria uses id to locate entry.
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE id = ?", id)
    conn.commit()
    conn.close()
    return
    return

def view_data():
    # Query list of all books
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book ORDER BY author, title")
    bookinfo = cur.fetchall()
    conn.close()
    return bookinfo

def close_app():
    return

connect()
#add_book("To Kill a MockingBird", "Harper Lee", 1988, "978-0446310789")
#add_book("Of Mice and Men", "John Steinbeck", 1993, "978-0140177398")
#add_book("My Brother Sam is Dead", "James Lincoln Collier,  Christopher Collier", 1974, "978-1566449526")
#update_info(3, "My Brother Sam is Dead", "James Lincoln Collier & Christopher Collier", 1975, "978-1566449526")
#print(search_list(title = "dead"))
#print(get_booklist())
