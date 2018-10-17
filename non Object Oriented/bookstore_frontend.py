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
import bookstore_backend

global book_item                                                               # This must be declared before window is generated.
book_item = None
window = Tk(screenName=None, baseName=None, className=" Book Store")           # Create window


#   Functions
def get_row(event):
    index = lodb.curselection()[0]          # Get index of selected cursor. Note that curselection returns a 1-element tuple
    book_item = lodb.get(index)
    vtitle.set(book_item[1])
    vauth.set(book_item[2])
    vyr.set(str(book_item[3]))
    visbn.set(book_item[4])
    return

def instantiate_input(tclabel, tcrow, tccol):
    lolbl = Label(window, text = tclabel)
    lolbl.grid(row = tcrow, column = tccol)
    lcinput = StringVar()
    loentry = Entry(window, textvar = lcinput)
    loentry.grid(row = tcrow, column = tccol  + 1)
    return [lolbl, loentry, lcinput]

def add_button(tclabel, tcrow, tcfunc):
    lobtn = Button(window, width = 12, text = tclabel, command = tcfunc)
    lobtn.grid(row = tcrow, column = 3)
    return lobtn

def get_booklist():
    lodb.delete(0,END)
    for row in bookstore_backend.view_data():
        lodb.insert(END, row)

def add_book():
    title = vtitle.get()
    author = vauth.get()
    if title == "":
        messagebox.showerror("Error", "Title not included for new entry.")
        return
    elif author == "":
        result = messagebox.askquestion("Warning", "Author as not been included for new entry. Proceed?", icon="warning")
        if result == "No":
            messagebox.showinfo("FYI","Entry not added.")
            return

    bookstore_backend.add_entry(vtitle.get(), vauth.get(), vyr.get(), visbn.get())
    return

def find_book():
    lodb.delete(0,END)
    try:
        year = int(vyr.get())
        book_data = bookstore_backend.filter(title =vtitle.get(), author = vauth.get(),year = int(vyr.get()), isbn = visbn.get())
    except:
        book_data = bookstore_backend.filter(title = vtitle.get(), author = vauth.get(), isbn = visbn.get())

    for row in book_data:
        lodb.insert(END, row)

def update_book_info():
    if type(book_item) == 'tuple':
        update_info(book_item[0], title =vtitle.get(), author = vauth.get(),year = int(vyr.get()), isbn = visbn.get())
    else:
        print("No entry selected")

    return

def remove_book():
    if type(book_item) == 'tuple':
        backend.delete_entry(book_item[0])
        vtitle.set("")
        vauth.set("")
        vyr.set("")
        visbn.set("")
        book_item = None
    else:
        print("No entry selected")

    return

def close_app():
    window.destroy()

[ltitle, etitle, vtitle] = instantiate_input("Title", 0, 0)
[lauth, eauth, vauth] = instantiate_input("Author", 0, 2)
[lyr, eyr, vyr] = instantiate_input("Year", 1, 0)
[lisbn, eisbn, visbn] = instantiate_input("ISBN", 1, 2)

loview = add_button("View All", 3, get_booklist)
loadd = add_button("Add Entry", 4, add_book)
losearch = add_button("Search Entry", 5, find_book)
loupdate = add_button("Update", 6, update_book_info)
lodelete = add_button("Delete", 7, remove_book)
loclose = add_button("Close", 8, close_app)

lodb = Listbox(window,  width  = 35)
lodb.grid(row = 2, column = 0, rowspan = 8, columnspan = 2)

lodb.bind('<<ListboxSelect>>', get_row)

loscrollbar = Scrollbar(window)
loscrollbar.grid(row = 2, column = 2, rowspan = 8)

lodb.configure(yscrollcommand = loscrollbar.set)    # Set list to scroll bar
loscrollbar.configure(command = lodb.yview)         # Set scroll bar to list

window.mainloop()   # All GUI interface code must be between window declaration and this line
