import sqlite3
import sys

class DatabaseItem:

    book_item = None
    conn = None
    curr = None

    def __init__(self, dbf):

        print("Connecting to " + dbf + ".")

        # Update variables as functions of parameters.
        try:
            self.conn = sqlite3.connect(dbf)
        except ConnectionError:
            print("Unable to connect to sqllie database file '" + dbf + "''")
            sys.exit()

        self.cur = self.conn.cursor()

        lcCreate = '''CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                year INTEGER,
                ISBN TEXT
        ) '''
        self.cur.execute(lcCreate)
        self.conn.commit()
        return


    def view_data(self):
        # Query list of all books
        self.cur.execute("SELECT * FROM book ORDER BY author, title")
        bookinfo = self.cur.fetchall()
        return bookinfo

    def add_entry(self, title, author, year, isbn):
        # Add entry for a book.
        self.cur.execute("INSERT INTO book values (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
        self.conn.commit()
        return

    def filter(self, title = "", author = "", year = 2000, isbn = ""):
        # Set default parameters as only subsets of the search criteria may be utilized.
        if len(title) > 0:
            lctitle = "%" + title.lower() + "%"
        else:
            lctitle = title

        if len(author) > 0:
            lcauthor = "%" + author.lower() + "%"
        else:
            lcauthor = author

        lcSearch = '''SELECT *
                        FROM book
                        WHERE lower(title) like ?
                            OR lower(author) like ?
                            OR year = ?
                            OR ISBN = ?
                        ORDER BY author, title
            '''

        self.cur.execute(lcSearch, (lctitle, lcauthor, year, isbn))
        bookinfo = self.cur.fetchall()
        return bookinfo

    def update_info(self, id, title, author, year, isbn):
        # Update information for selected book entry. The actual criteria uses id to locate entry.
        lcUpdate = '''UPDATE book
                        SET title = ?,
                            author = ?,
                            year = ?,
                            isbn = ?
                        WHERE id = ?
        '''
        self.cur.execute(lcUpdate, (title, author, year, isbn, str(id)))
        self.conn.commit()
        return

    def delete_entry(self, id):
        # Delete selected book entry. The actual criteria uses id to locate entry.
        print(type(id))
        self.cur.execute("DELETE FROM book WHERE id = ?", str(id))
        self.conn.commit()
        return


    def __del__(self):
        # Close connection before exiting applicaiton.
        print("Exiting bookstore...")
        self.conn.close()
