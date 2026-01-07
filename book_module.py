from PyQt5 import QtWidgets, uic
from tkinter import messagebox
import sqlite3

class AddBookModule(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()  

    def add_book(self):
        book_id=self.book_id_entry.text()
        title=self.book_title_entry.text()
        author=self.book_author_entry.text()
        category=self.category_combobox.currentText()
        quantity=self.book_quantity_entry.text()

        if not book_id or not title or not author or not category or not quantity:
            messagebox.showerror("Error","All Fields Are Mandatory")
            return
        
        try:
            quantity=int(quantity)
        except:
            messagebox.showerror("Error","Quantity Must Be A Number")
            return
        
        available_copies=quantity

        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()

        cursor.execute("Insert into books (book_id,title,author,category,quantity,available_copies) values (?,?,?,?,?,?)",
                       (book_id,title,author,category,quantity,available_copies))
        connect.commit()
        connect.close()
        messagebox.showinfo("Success","Book Added Successfully")

    def add_book_ui(self):
        uic.loadUi("add_book_ui.ui",self)
        self.add_book_button.clicked.connect(self.add_book)
        self.exec_()

class ViewBookModule(QtWidgets.QDialog):

    def __init__(self):
        super().__init__() 

    def view_book_ui(self):
        uic.loadUi("view_book_ui.ui",self)
        self.book_data_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.get_book_data()
        self.search_entry.textChanged.connect(self.search_books)
        self.exec_()

    def get_book_data(self):
        connect=sqlite3.connect("library.db")
        cursor=connect.cursor()
        cursor.execute("Select * from books")
        data=cursor.fetchall()
        connect.close()

        self.book_data_table.setRowCount(len(data))
        self.book_data_table.setColumnCount(6)
        headers = ["Book ID", "Title", "Author", "Category", "Quantity", "Available"]
        self.book_data_table.setHorizontalHeaderLabels(headers)
        
        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                self.book_data_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))

    def search_books(self):
        text=self.search_entry.text().strip()

        connect=sqlite3.connect("library.db")
        cursor= connect.cursor()

        if text=="":
            cursor.execute("Select *from books")
        else:
            cursor.execute("Select * from books where book_id like ? or title LIKE ? or author like ? or category like ?", (f"%{text}%", f"%{text}%", f"%{text}%", f"%{text}%"))

        data = cursor.fetchall()
        connect.close()

        self.book_data_table.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                self.book_data_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(value)))


class UpdateBookModule(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

    def update_book_ui(self):
        uic.loadUi("update_delete_book_ui.ui",self)
        self.update_book_button.clicked.connect(self.update_book)
        self.delete_book_button.clicked.connect(self.delete_book)
        self.exec_()

    def update_book(self):
        bookID = self.update_book_id_entry.text()

        if not bookID:
            messagebox.showerror("Error","Please Enter Book ID")
            return

        connect = sqlite3.connect("library.db")
        cursor = connect.cursor()

        cursor.execute("SELECT 1 FROM books WHERE book_id=?", (bookID,))
        exist = cursor.fetchone()

        if not exist:
            messagebox.showerror("Error", "Book does not exist")
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

        if category == "quantity" and not new_val.isdigit():
            messagebox.showerror("Error","Quantity must be a number")
            connect.close()
            return

        if category == "quantity":
            cursor.execute(
                "UPDATE books SET quantity=?, available_copies=? WHERE book_id=?",
                (new_val, new_val, bookID)
            )
        else:
            cursor.execute(
                f"UPDATE books SET {category}=? WHERE book_id=?",
                (new_val, bookID)
            )

        connect.commit()
        connect.close()

        messagebox.showinfo("Success","Book Updated Successfully")

        
    def delete_book(self):
        book_id=self.delete_book_id_entry.text()

        if not book_id:
            messagebox.showerror("Error","Please Enter Book ID")
            return

        connect=sqlite3.connect("library.db")
        cursor= connect.cursor()

        cursor.execute("Select 1 from books where book_id=?",(book_id,))
        exist=cursor.fetchone()

        if not exist:
            messagebox.showerror("Error", "Book does not exist")
            connect.close()
            return
        
        cursor.execute("Delete from books where book_id=?",(book_id,))
        
        connect.commit()
        connect.close()

        messagebox.showinfo("Success","Book Deleted successfully")