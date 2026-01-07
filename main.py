from PyQt5 import QtWidgets, uic
import sqlite3
from book_module import *
from member_module import *
from issue_return import *
from history_module import *
from settings import *

class MainScreen(QtWidgets.QWidget):
    
    def __init__(self,login_window):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.showMaximized()
        self.dashboard_counts()
        self.login_window=login_window
        self.add_book.clicked.connect(self.open_add_book)
        self.view_book.clicked.connect(self.open_view_book)
        self.update_book.clicked.connect(self.open_update_book)
        self.add_member.clicked.connect(self.open_add_member)
        self.view_member.clicked.connect(self.open_view_member)
        self.update_member.clicked.connect(self.open_update_member)
        self.issue_book.clicked.connect(self.open_issue_book)
        self.return_book.clicked.connect(self.open_return_book)
        self.view_issued_book.clicked.connect(self.open_viewissuedbook)
        self.view_returned_book.clicked.connect(self.open_viewreturnedbook)
        self.view_overdue_book.clicked.connect(self.open_viewoverduebook)
        self.view_fine_history_button.clicked.connect(self.open_fine_history)
        self.change_password_button.clicked.connect(self.change_password)
        self.logout_button.clicked.connect(self.logout)

    def open_add_book(self):
        self.book_screen=AddBookModule()
        self.book_screen.add_book_ui()  
        self.dashboard_counts() 

    def open_view_book(self):
        self.book_screen=ViewBookModule()
        self.book_screen.view_book_ui()

    def open_update_book(self):
        self.book_screen=UpdateBookModule()
        self.book_screen.update_book_ui()
        self.dashboard_counts()

    def open_add_member(self):
        self.member_screen=AddMemberModule()
        self.member_screen.add_member_ui()
        self.dashboard_counts()

    def open_view_member(self):
        self.member_screen=ViewMemberModule()
        self.member_screen.view_member_ui()

    def open_update_member(self):
        self.member_screen=UpdateMemberModule()
        self.member_screen.update_member_ui()
        self.dashboard_counts()

    def open_issue_book(self):
        self.issue_screen=IssueModule()
        self.issue_screen.issue_book_ui()
        self.dashboard_counts()

    def open_return_book(self):
        self.return_screen=ReturnModule()
        self.return_screen.return_book_ui()
        self.dashboard_counts()

    def open_viewissuedbook(self):
        self.history_screen=ViewIssuedBooks()
        self.history_screen.view_issued_book_ui()

    def open_viewreturnedbook(self):
        self.history_screen=ViewReturnedBooks()
        self.history_screen.view_returned_book_ui()

    def open_viewoverduebook(self):
        self.history_screen=ViewOverdueBooks()
        self.history_screen.view_overdue_book_ui()

    def open_fine_history(self):
        self.history_screen=ViewFineHistory()
        self.history_screen.view_fine_history_ui()

    def change_password(self):
        self.settings_screen=ChangePassword()
        self.settings_screen.change_password_ui()

    def logout(self):
        self.close()
        self.login_window.username_entry.clear()
        self.login_window.password_entry.clear()
        self.login_window.show()

    def dashboard_counts(self):
        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()

        cursor.execute("Select sum(quantity) from books")
        total_books=cursor.fetchone()[0]
        if total_books is None:
            total_books=0
        self.total_book_count.setText(str(total_books))

        cursor.execute("Select sum(available_copies) from books")
        available_books=cursor.fetchone()[0]
        if available_books is None:
            available_books=0
        self.available_book_count.setText(str(available_books))

        cursor.execute("Select count(*) from issue where issue_id not in (Select issue_id from return)")
        issued_books=cursor.fetchone()[0]
        if issued_books is None:
            issued_books=0
        self.issued_book_count.setText(str(issued_books))

        cursor.execute("Select count(member_id) from members")
        total_members=cursor.fetchone()[0]
        if total_members is None:
            total_members=0
        self.total_member_count.setText(str(total_members))

        cursor.execute("Select count(*) from issue where issue_id not in (Select issue_id from return) and DATE(due_date)<DATE('now')")
        overdue_books=cursor.fetchone()[0]
        if overdue_books is None:
            overdue_books=0
        self.overdue_book_count.setText(str(overdue_books))