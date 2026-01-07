from PyQt5 import QtWidgets, uic
from tkinter import messagebox
from datetime import datetime,date
import sqlite3

class IssueModule(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()

    def issue_book_ui(self):
        uic.loadUi("issue_book_ui.ui",self)
        self.issue_book_button.clicked.connect(self.issue_book)
        self.exec_()

    def issue_book(self):
        memberID = self.member_id_entry.text()
        bookID = self.book_id_entry.text()
        issueDate = self.issue_date_edit.date().toString("yyyy-MM-dd")
        dueDate = self.due_date_edit.date().toString("yyyy-MM-dd")

        if not memberID or not bookID or not issueDate or not dueDate:
            messagebox.showerror("Error", "All fields are mandatory")
            return

        connect = sqlite3.connect("library.db")
        cursor = connect.cursor()

        cursor.execute("SELECT available_copies FROM books WHERE book_id = ?", (bookID,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", "Invalid Book ID")
            connect.close()
            return

        if result[0] <= 0:
            messagebox.showerror("Error", "No copies available")
            connect.close()
            return

        cursor.execute("INSERT INTO issue (member_id, book_id, issue_date, due_date) VALUES (?,?,?,?)",
                        (memberID, bookID, issueDate, dueDate))

        cursor.execute("UPDATE books SET available_copies = available_copies - 1 WHERE book_id = ?",
                        (bookID,))

        cursor.execute("UPDATE members SET currently_issued_count = currently_issued_count + 1 WHERE member_id = ?",
                        (memberID,))

        connect.commit()
        connect.close()

        messagebox.showinfo("Success", "Book issued successfully")
        self.close()

class ReturnModule(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()

    def return_book_ui(self):
        uic.loadUi("return_book_ui.ui",self)
        self.return_button.clicked.connect(self.return_book)
        self.confirm_button.clicked.connect(self.insert_data)
        self.confirm_button.hide()
        self.exec_()

    def return_book(self):
        self.issueID=self.issue_id_entry.text()
        self.fine=0
        
        if not self.issueID:
            messagebox.showerror("Error","Please Enter self.issueID")
            return
        
        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()

        cursor.execute("Select member_id,book_id,due_date from issue where issue_id=?",(self.issueID,))
        row=cursor.fetchone()

        if not row:
            messagebox.showerror("Error","Invalid Issue ID")
            return
        self.memberID,self.bookID,self.dueDate_str=row

        self.today=date.today()
        dueDate=datetime.strptime(self.dueDate_str,"%Y-%m-%d").date()

        if self.today > dueDate:
            overdue_days=(self.today-dueDate).days
            self.fine=overdue_days*10
            self.fine_label.setText(f"Overdue by {overdue_days} days : Fine - ₹{self.fine}")
            self.confirm_button.show()
        else:
            self.fine_label.setText("No Fine, Returning Before Due Date")
            self.confirm_button.show()

        connect.commit()
        connect.close()
        
    def insert_data(self):
        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()

        cursor.execute("Insert into return (issue_id,return_date,fine_paid) values (?,?,?)",
                       (self.issueID,self.today,self.fine))
        
        cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE book_id = ?",
                        (self.bookID,))

        cursor.execute("UPDATE members SET currently_issued_count = currently_issued_count - 1 WHERE member_id = ?",
                        (self.memberID,))
        
        messagebox.showinfo("Success","Book Returned Successfully")

        connect.commit()
        connect.close()
