from PyQt5 import QtWidgets, uic
from datetime import datetime,date
from tkinter import messagebox
import sqlite3

class ViewIssuedBooks(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

    def view_issued_book_ui(self):
        uic.loadUi("view_issued_book_ui.ui",self)
        self.issued_book_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.get_issued_book_data()
        self.search_entry.textChanged.connect(self.search_issued_book)
        self.exec_()

    def get_issued_book_data(self):
        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()
        cursor.execute("Select * from issue")
        data=cursor.fetchall()
        connect.close()

        self.issued_book_table.setRowCount(len(data))
        self.issued_book_table.setColumnCount(5)
        headers = ["Issue ID", "Member ID", "Book ID", "Issue Date", "Due Date"]
        self.issued_book_table.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                self.issued_book_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))

    def search_issued_book(self):
        text=self.search_entry.text().strip()

        connect=sqlite3.connect("library.db")
        cursor= connect.cursor()

        if text=="":
            cursor.execute("Select * from issue")
        else:
            cursor.execute("Select * from issue where issue_id like ? or member_id LIKE ? or book_id like ? or issue_date like ? or due_date like ?", (f"%{text}%",f"%{text}%",f"%{text}%",f"%{text}%",f"%{text}%"))

        data = cursor.fetchall()
        connect.close()

        self.issued_book_table.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                self.issued_book_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))

class ViewReturnedBooks(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
    
    def view_returned_book_ui(self):
        uic.loadUi("view_returned_book_ui.ui",self)
        self.returned_book_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.get_returned_book_data()
        self.search_entry.textChanged.connect(self.search_returned_book)
        self.exec_()

    def get_returned_book_data(self):
        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()
        cursor.execute("Select * from return")
        data=cursor.fetchall()
        connect.close()

        self.returned_book_table.setRowCount(len(data))
        self.returned_book_table.setColumnCount(4)
        headers = ["Return ID", "Issue ID", "Return Date", "Fine Paid"]
        self.returned_book_table.setHorizontalHeaderLabels(headers)
        
        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                self.returned_book_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))

    def search_returned_book(self):
        text=self.search_entry.text().strip()

        connect=sqlite3.connect("library.db")
        cursor= connect.cursor()

        if text=="":
            cursor.execute("Select * from return")
        else:
            cursor.execute("Select * from return where return_id like ? or issue_id LIKE ? or return_date like ? or fine_paid like ?", (f"%{text}%",f"%{text}%",f"%{text}%",f"%{text}%"))

        data = cursor.fetchall()
        connect.close()

        self.returned_book_table.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                self.returned_book_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))

class ViewOverdueBooks(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

    def view_overdue_book_ui(self):
        uic.loadUi("view_overdue_book_ui.ui",self)
        self.overdue_book_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.get_overdue_book_data()
        self.exec_()

    def get_overdue_book_data(self):
        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()
        cursor.execute("Select * from issue where issue_id not in (Select issue_id from return) and DATE(due_date)<DATE('now')")
        data=cursor.fetchall()
        connect.close()

        if not data:
            messagebox.showinfo("Info","No Overdue Books")
            return
        self.overdue_book_table.setRowCount(len(data))
        self.overdue_book_table.setColumnCount(6)
        headers=["Issue ID","Member ID","Book ID","Issue Date","Due Date","Overdue Days"]
        self.overdue_book_table.setHorizontalHeaderLabels(headers)
        
        for row_index,row_data in enumerate(data):
            issue_id,member_id,book_id,issue_date,due_date=row_data

            due=datetime.strptime(due_date,"%Y-%m-%d").date()
            overdue_days=(date.today()-due).days

            values=list(row_data)+[overdue_days]

        for col_index,value in enumerate(values):
            self.overdue_book_table.setItem(
                row_index,col_index,QtWidgets.QTableWidgetItem(str(value))
            )

class ViewFineHistory(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

    def view_fine_history_ui(self):
        uic.loadUi("view_fine_history_ui.ui",self)
        self.fine_history_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.get_fine_history_data()
        self.exec_()

    def get_fine_history_data(self):
        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()
        cursor.execute("""Select return.return_id,return.issue_id,issue.member_id,issue.book_id,issue.due_date,return.return_date,return.fine_paid
        from return JOIN issue ON return.issue_id=issue.issue_id
        where return.fine_paid>0;""")
        data=cursor.fetchall()
        connect.close()

        self.fine_history_table.setRowCount(len(data))
        self.fine_history_table.setColumnCount(7)
        headers = ["Return ID","Issue ID","Member ID","Book ID","Due Date","Return Date","Fine Paid"]
        self.fine_history_table.setHorizontalHeaderLabels(headers)
        
        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                self.fine_history_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))