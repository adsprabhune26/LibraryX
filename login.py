from PyQt5 import QtWidgets, uic
import sys
import sqlite3
from tkinter import messagebox
from main import MainScreen
from PyQt5.QtCore import Qt

class LibraryApp(QtWidgets.QMainWindow):
        
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.showMaximized()
        self.login_button.clicked.connect(self.login)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.login_button.click()

    def login(self):
        username=self.username_entry.text()
        password=self.password_entry.text()

        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()

        cursor.execute("Select * from admin where username=? and password=?", (username, password))
        result=cursor.fetchone()
        
        if result:
            self.main_screen = MainScreen(self)
            self.main_screen.show()
            self.hide()
        else:
            messagebox.showerror("Fail","Enter Valid Username And Password")
        
app = QtWidgets.QApplication(sys.argv)
window = LibraryApp()
window.show()
app.exec_()