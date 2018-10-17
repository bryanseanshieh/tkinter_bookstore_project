"""
This is a program that stores the following book information:
- Title
- Author
- Year
- ISBN

User can....
- View all records
- Search entries
- Add / update / delete entries
"""
from tkinter import *   # Allows you to call tkinter methods without referencing
                        # tkinter object
from tkinter import messagebox
from bookstore_backend import DatabaseItem

# Define application class
class Bookstore_App(object):
    """ Class object for a book store.
        - class contains methods for running a book store, but requires
          a tkinter window to serve a a platform to host access to
          methods.
        """
    def __init__(self, window):
        # Generate a window beforehand and pass in as a variable.
        self.window = window

        # Instantiation helpler Functions

        def instantiate_input(tclabel, tcrow, tccol):
            lolbl = Label(self.window, text = tclabel)
            lolbl.grid(row = tcrow, column = tccol)
            lcinput = StringVar()
            loentry = Entry(self.window, textvar = lcinput)
            loentry.grid(row = tcrow, column = tccol  + 1)
            return [lolbl, loentry, lcinput]

        def add_button(tclabel, tcrow, tcfunc):
            lobtn = Button(self.window, width = 12, text = tclabel, command = tcfunc)
            lobtn.grid(row = tcrow, column = 3)
            return lobtn

        # Instantiate widgets
        [self.ltitle, self.etitle, self.vtitle] = instantiate_input("Title", 0, 0)
        [self.lauth, self.eauth, self.vauth] = instantiate_input("Author", 0, 2)
        [self.lyr, self.eyr, self.vyr] = instantiate_input("Year", 1, 0)
        [self.lisbn, self.eisbn, self.visbn] = instantiate_input("ISBN", 1, 2)

        self.loview = add_button("View All", 3, self.get_booklist)
        self.loadd = add_button("Add Entry", 4, self.add_book)
        self.losearch = add_button("Search Entry", 5, self.find_book)
        self.loupdate = add_button("Update", 6, self.update_book_info)
        self.lodelete = add_button("Delete", 7, self.remove_book)
        self.loclose = add_button("Close", 8, self.close_app)

        self.lodb = Listbox(window,  width  = 35)
        self.lodb.grid(row = 2, column = 0, rowspan = 8, columnspan = 2)

        self.lodb.bind('<<ListboxSelect>>', self.get_row)

        self.loscrollbar = Scrollbar(self.window)
        self.loscrollbar.grid(row = 2, column = 2, rowspan = 8)

        self.lodb.configure(yscrollcommand = self.loscrollbar.set)    # Set list to scroll bar
        self.loscrollbar.configure(command = self.lodb.yview)         # Set scroll bar to list

    #   Helper Methods
    def get_row(self, event):
        index = self.lodb.curselection()[0]          # Get index of selected cursor. Note that curselection returns a 1-element tuple
        dbf.book_item = self.lodb.get(index)
        self.vtitle.set(dbf.book_item[1])
        self.vauth.set(dbf.book_item[2])
        self.vyr.set(str(dbf.book_item[3]))
        self.visbn.set(dbf.book_item[4])
        return

    def get_booklist(self):
        self.lodb.delete(0,END)  # Clear listbox for re-processing
        for row in dbf.view_data():
            self.lodb.insert(END, row)

    def add_book(self):
        title = self.vtitle.get()
        author = self.vauth.get()
        if title == "":
            messagebox.showerror("Error", "Title not included for new entry.")
            return
        elif author == "":
            result = messagebox.askquestion("Warning", "Author as not been included for new entry. Proceed?", icon="warning")
            if result == "No":
                messagebox.showinfo("FYI","Entry not added.")
                return

        dbf.add_entry(self.vtitle.get(), self.vauth.get(), self.vyr.get(), self.visbn.get())
        return

    def find_book(self):
        self.lodb.delete(0,END)  # Clear listbox for re-processing
        try:
            year = int(self.vyr.get())
            book_data = dbf.filter(title = self.vtitle.get(), author = self.vauth.get(),year = int(self.vyr.get()), isbn = self.visbn.get())
        except:
            book_data = dbf.filter(title = self.vtitle.get(), author = self.vauth.get(), isbn = self.visbn.get())

        for row in book_data:
            self.lodb.insert(END, row)

    def update_book_info(self):
        if self.lodb.curselection() == ():     #Nothing assigned yet.
            print("No entry selected")
        else:
            dbf.update_info(dbf.book_item[0], title = self.vtitle.get(), author = self.vauth.get(),year = int(self.vyr.get()), isbn = self.visbn.get())
            return

    def remove_book(self):
        # Check for selected entry.
        if self.lodb.curselection() == ():     #Nothing assigned yet.
            print("No entry selected")
        else:
            dbf.delete_entry(dbf.book_item[0])
            self.vtitle.set("")
            self.vauth.set("")
            self.vyr.set("")
            self.visbn.set("")
            dbf.book_item = None
        return

    def close_app(self):
        self.window.destroy()



dbf = DatabaseItem("bookstore.db")

 # Create window
window = Tk(screenName=None, baseName=None, className =" Book Store")
bookstore = Bookstore_App(window)





window.mainloop()   # All GUI interface code must be between window declaration and this line
