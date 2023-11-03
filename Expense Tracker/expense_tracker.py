from tkinter import *
from tkinter import ttk
import sqlite3 as db
from tkcalendar import DateEntry

# Initialize the SQLite database and create the 'expenses' table if it doesn't exist.
def init():
    connectionObjs = db.connect("expenseTracker.db")
    curr = connectionObjs.cursor()
    query = '''
    CREATE TABLE IF NOT EXISTS expenses (
        date STRING,
        name STRING,
        title STRING,
        expense NUMBER
    )
    '''
    curr.execute(query)
    connectionObjs.commit()


# Function to submit an expense to the database and update the displayed list.
def submitexpense():
    values = [dateEntry.get(), Name.get(), Title.get(), Expense.get()]
    print(values)
    Enable.insert('', 'end', values=values)  # Add the expense to the Treeview widget.

    connectionObjs = db.connect("expenseTracker.db")
    curr = connectionObjs.cursor()
    query = '''
    INSERT INTO expenses VALUES (?, ?, ?, ?)
    '''
    curr.execute(query, (dateEntry.get(), Name.get(), Title.get(), Expense.get()))
    connectionObjs.commit()


# Function to view all expenses from the database.
def viewexpense():
    connectionObjs = db.connect("expenseTracker.db")
    curr = connectionObjs.cursor()
    query = '''
    SELECT * FROM expenses
    '''
    total = '''
    SELECT SUM(expense) FROM expenses
    '''
    curr.execute(query)
    rows = curr.fetchall()
    curr.execute(total)
    amount = curr.fetchall()[0]
    print(rows)
    print(amount)


    # Display the list of expenses and the total amount in a label.
    l = Label(root, text="Date\t  Name\t  Title\t  Expense", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white")
    l.grid(row=6, column=0, padx=7, pady=7)

    st = ""
    for i in rows:
        for j in i:
            st += str(j) + '\t'
        st += '\n'
    print(st)
    l = Label(root, text=st, font=('arial', 12))
    l.grid(row=7, column=0, padx=7, pady=7)


# Initialize the database and create the main GUI window.
init()
root = Tk()
root.title("Expense Tracker")
root.geometry('800x600')


# Create GUI components for date, name, title, and expense input.
dateLabel = Label(root, text="Date", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
dateLabel.grid(row=0, column=0, padx=7, pady=7)

dateEntry = DateEntry(root, width=12, font=('arial', 15, 'bold'))
dateEntry.grid(row=0, column=1, padx=7, pady=7)

Name = StringVar()
nameLabel = Label(root, text="Name", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
nameLabel.grid(row=1, column=0, padx=7, pady=7)

NameEntry = Entry(root, textvariable=Name, font=('arial', 15, 'bold'))
NameEntry.grid(row=1, column=1, padx=7, pady=7)

Title = StringVar()
titleLabel = Label(root, text="Title", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
titleLabel.grid(row=2, column=0, padx=7, pady=7)

titleEntry = Entry(root, textvariable=Title, font=('arial', 15, 'bold'))
titleEntry.grid(row=2, column=1, padx=7, pady=7)

Expense = IntVar()
expenseLabel = Label(root, text="Expense", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
expenseLabel.grid(row=3, column=0, padx=7, pady=7)

expenseEntry = Entry(root, textvariable=Expense, font=('arial', 15, 'bold'))
expenseEntry.grid(row=3, column=1, padx=7, pady=7)


# Buttons to submit expenses and view expenses.
submitbtn = Button(root, command=submitexpense, text="Submit", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
submitbtn.grid(row=4, column=0, padx=13, pady=13)

viewtn = Button(root, command=viewexpense, text="View expenses", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
viewtn.grid(row=4, column=1, padx=13, pady=13)

# Create a Treeview widget to display the list of saved expenses.
Elist = ['Date', 'Name', 'Title', 'Expense']
Enable = ttk.Treeview(root, column=Elist, show='headings', height=7)
for c in Elist:
    Enable.heading(c, text=c.title())
Enable.grid(row=5, column=0, padx=7, pady=7, columnspan=3)


# Function to reset expenses by deleting all records from the 'expenses' table.
def reset_expenses():
    connectionObjs = db.connect("expenseTracker.db")
    curr = connectionObjs.cursor()
    query = '''
    DELETE FROM expenses
    '''
    curr.execute(query)
    connectionObjs.commit()
    
    # Clear the Treeview widget to reflect the empty database.
    for item in Enable.get_children():
        Enable.delete(item)

# Create a button to reset expenses.
resetbtn = Button(root, command=reset_expenses, text="Reset Expenses", font=('arial', 15, 'bold'), bg="red", fg="white", width=12)
resetbtn.grid(row=4, column=2, padx=13, pady=13)


# Start the main loop for the GUI application.
mainloop()

