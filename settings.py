from PyQt5 import QtWidgets, uic
from tkinter import messagebox
import sqlite3

class ChangePassword(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

    def change_password_ui(self):
        uic.loadUi("change_password_ui.ui",self)
        self.change_pass_button.clicked.connect(self.change_password)
        self.exec_()

    def change_password(self):
        current_pass=self.current_pass_entry.text()
        new_pass=self.new_pass_entry.text()
        confirm_pass=self.confirm_pass_entry.text()

        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()

        cursor.execute("select password from admin")
        password=cursor.fetchone()[0]
        
        if current_pass!=password:
            messagebox.showerror("Error","Current Password Is Inavlid")
        elif new_pass!=confirm_pass:
            messagebox.showerror("Error","New Password And Confirm Password Doesnt Match")
        else:
            cursor.execute("update admin set password = ?",(new_pass,))
            messagebox.showinfo("Success","Password Changed Successfully")
        
        connect.commit()
        connect.close()
