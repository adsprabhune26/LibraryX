from PyQt5 import QtWidgets, uic
from tkinter import messagebox
import sqlite3

class AddMemberModule(QtWidgets.QDialog):
    def __init__(self):
        super().__init__() 

    def add_member(self):
        name=self.member_name_entry.text()
        address=self.member_address_entry.text()
        contact=self.member_contact_entry.text()
        email=self.member_email_entry.text()
        
        if not name or not address or not contact or not email:
            messagebox.showerror("Error","All Fields Are Mandatory")
            return
        
        if not contact.isdigit() or len(contact) != 10:
            messagebox.showerror("Error", "Contact number must be exactly 10 digits")
            return

        if not ("@" in email and (email.endswith("@gmail.com") or email.endswith("@yahoo.com"))):
            messagebox.showerror("Error", "Enter a valid email ID")
            return

        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()

        cursor.execute("Insert into members (name,phone,address,email) values (?,?,?,?)",
                       (name,contact,address,email))
        connect.commit()
        connect.close()
        messagebox.showinfo("Success","Member Added Sucessfully")

    def add_member_ui(self):
        uic.loadUi("add_member_ui.ui",self)
        self.add_member_button.clicked.connect(self.add_member)
        self.exec_()

class ViewMemberModule(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

    def view_member_ui(self):
        uic.loadUi("view_member_ui.ui",self)
        self.member_data_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.get_member_data()
        self.search_entry.textChanged.connect(self.search_member)
        self.exec_()

    def get_member_data(self):
        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()
        cursor.execute("Select * from members")
        data=cursor.fetchall()
        connect.close()

        self.member_data_table.setRowCount(len(data))
        self.member_data_table.setColumnCount(6)
        headers = ["Member ID", "Name", "Contact", "Address", "Issue Count", "Email"]
        self.member_data_table.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                self.member_data_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))

    def search_member(self):
        text=self.search_entry.text().strip()

        connect=sqlite3.connect("library.db")
        cursor= connect.cursor()

        if text=="":
            cursor.execute("Select * from members")
        else:
            cursor.execute("Select * from members where member_id like ? or name LIKE ? or phone like ? or address like ? or email like ?", (f"%{text}%",f"%{text}%",f"%{text}%",f"%{text}%",f"%{text}%"))

        data = cursor.fetchall()
        connect.close()

        self.member_data_table.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                self.member_data_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))

class UpdateMemberModule(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

    def update_member_ui(self):
        uic.loadUi("update_delete_member_ui.ui",self)
        self.update_member_button.clicked.connect(self.update_member)
        self.delete_member_button.clicked.connect(self.delete_member)
        self.exec_()

    def update_member(self):
        memberID = self.update_member_id_entry.text()

        if not memberID:
            messagebox.showerror("Error","Please Enter Member ID")
            return

        connect = sqlite3.connect("library.db")
        cursor = connect.cursor()

        cursor.execute("SELECT 1 FROM members WHERE member_id=?", (memberID,))
        exist = cursor.fetchone()

        if not exist:
            messagebox.showerror("Error", "Member does not exist")
            connect.close()
            return

        category = self.category_combobox.currentText()
        new_val = self.update_value_entry.text()

        if not category:
            messagebox.showerror("Error","Please Select The Column You Want To Update")
            connect.close()
            return

        if not new_val:
            messagebox.showerror("Error","Please Enter The Value You Want To Update")
            connect.close()
            return

        if category == "phone":
            if not new_val.isdigit() or len(new_val) != 10:
                messagebox.showerror("Error", "Contact number must be exactly 10 digits")
                connect.close()
                return

        if category == "email":
            if not ("@" in new_val and (new_val.endswith("@gmail.com") or new_val.endswith("@yahoo.com"))):
                messagebox.showerror("Error", "Enter a valid email ID")
                connect.close()
                return

        cursor.execute(
            f"UPDATE members SET {category}=? WHERE member_id=?",
            (new_val, memberID))

        connect.commit()
        connect.close()

        messagebox.showinfo("Success","Member Updated Successfully")
        
    def delete_member(self):
        member_id=self.delete_member_id_entry.text()

        if not member_id:
            messagebox.showerror("Error","Please Enter Member ID")
            return

        connect=sqlite3.connect("library.db")
        cursor= connect.cursor()

        cursor.execute("Select 1 from members where member_id=?",(member_id,))
        exist=cursor.fetchone()

        if not exist:
            messagebox.showerror("Error", "Member does not exist")
            connect.close()
            return
        
        cursor.execute("Delete from members where member_id=?",(member_id,))
        
        connect.commit()
        connect.close()

        messagebox.showinfo("Success","Member Deleted successfully")