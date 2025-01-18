from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from Customers import Customers
from category import Category
from products import Products
from bill import Bills
import time
import sqlite3
import os

class SMS :
    def __init__(self, root) :
        self.root = root
        self.root.geometry("1360x700+0+0")
        self.root.config(bg = "palegreen")
        self.root.title("Shop Management System | Developed by Vedant")
        
        self.root.icon_image = PhotoImage(file = "images/logo1.png")

        self.con = sqlite3.connect(database = r"sms.db")
        self.cur = self.con.cursor()

        title = Label(
                      self.root,
                      text = "Shop Management System",
                      font = ("times of now", 20, "bold"),
                      fg = "White",
                      bg = "darkBlue",
                      pady = 20,
                      image = self.root.icon_image,
                      padx = 20,
                      compound = LEFT,
                      anchor = "w"
                      ).place(x = 0, y = 0, relwidth = 1, height = 70)

        self.label_clock = Label(
                                text = "\t\t\tWelcome to Shop Management System\t\t\t\tDate : DD/MM/YYYY\t\t\t\tTime : HH : MM : SS",
                                bg = "grey",
                                fg = "white",
                                anchor = "w",
                                font = ("times of now", 10),                                
                                )
        self.label_clock.place(x = 0, y = 70, relwidth = 1, height = 30)
        
        LeftMenu = Frame(
                        self.root,
                         bg = "white",
                         bd = 2,
                         relief = RIDGE
                         )
        LeftMenu.place(x = 0, y = 100, width = 200, height = 535)

        self.menu_icon = Image.open("images/menu_im.png")
        self.menu_icon = self.menu_icon.resize((200, 300))
        self.menu_icon = ImageTk.PhotoImage(self.menu_icon)

        lbl_menu_icon = Label(
                              LeftMenu,
                              image = self.menu_icon
                              )
        lbl_menu_icon.pack(side = TOP, fill = X)

        Menu = Label(
                     LeftMenu,
                     text = "Menu",
                     font = ("times of now", 15, "bold"),
                     bg = "darkBlue",
                     fg = "white"
                     ).pack(side = TOP, fill = X)

        self.btn_logo = PhotoImage(file = "images/side.png")

        Customer_btn = Button(
                              LeftMenu,
                              text = "Customers",
                              bg = "white",
                              image = self.btn_logo,
                              font = ("times of now", 15, "bold"),
                              bd = 2,
                              command = self.Customers,
                              padx = 5,
                              anchor = "w",
                              relief = RIDGE,
                              compound = LEFT,
                              cursor = "hand2",
                              width = 250
                              ).pack()

        Products_btn = Button(
                              LeftMenu,
                              text = "Products",
                              bg = "white",
                              command = self.products,
                              image = self.btn_logo,
                              font = ("times of now", 15, "bold"),
                              bd = 2,
                              relief = RIDGE,
                              cursor = "hand2",
                              width = 250,
                              padx = 5,
                              anchor = "w",
                              compound = LEFT,
                              ).pack()
        
        catogry_btn = Button(
                              LeftMenu,
                              text = "Category",
                              bg = "white",
                              command = self.category,
                              image = self.btn_logo,
                              font = ("times of now", 15, "bold"),
                              bd = 2,
                              compound = LEFT,
                              relief = RIDGE,
                              cursor = "hand2",
                              padx = 5,
                              anchor = "w",
                              width = 250
                              ).pack()

        bill_btn = Button(
                              LeftMenu,
                              text = "My Bills",
                              bg = "white",
                              image = self.btn_logo,
                              compound = LEFT,
                              font = ("times of now", 15, "bold"),
                              bd = 2,
                              width = 250,
                              command = self.Bills,
                              relief = RIDGE,
                              padx = 5,
                              anchor = "w",
                              cursor = "hand2"
                              ).pack()

        exit_btn = Button(
                              LeftMenu,
                              text = "Exit",
                              bg = "white",
                              image = self.btn_logo,
                              font = ("times of now", 15, "bold"),
                              bd = 2,
                              padx = 5,
                              anchor = "w",
                              command = self.exit,
                              relief = RIDGE,
                              compound = LEFT,
                              cursor = "hand2",
                              width = 250
                              ).pack()

        footer = Label(
                       self.root,
                       text = "Shop Mangement System | Developed by Vedant\nFor any Technical Queries Contact :- 9209474097",
                       bg = "gray"
                       ).pack(side = BOTTOM, fill = X)
        
        self.Total_CS = Label(
                        self.root,
                        text = "Total Customers\n[ 0 ]",
                        bg = "orange",
                        fg = "white",
                        width = 15,
                        bd = 2,
                        relief = RIDGE,                        
                        height = 5,
                        font = ("goundy old style", 15)
                        )
        self.Total_CS.place(x = 300, y = 170)

        self.Products = Label(
                        self.root,
                        text = "Products\n[ 0 ]",
                        bg = "#FF007F",
                        fg = "white",
                        width = 15,
                        height = 5,
                        bd = 2,
                        relief = RIDGE,
                        font = ("goundy old style", 15)
                        )
        self.Products.place(x = 900, y = 170)

        self.MyBill = Label(
                        self.root,
                        text = "My Bills\n[ 0 ]",
                        bg = "blue",
                        fg = "white",
                        width = 15,
                        height = 5,
                        bd = 2,
                        relief = RIDGE,
                        font = ("goundy old style", 15)
                        )
        self.MyBill.place(x = 300, y = 470)

        self.category = Label(
                        self.root,
                        text = "Category\n[ 0 ]",
                        bg = "red",
                        fg = "white",
                        width = 15,
                        height = 5,
                        bd = 2,
                        relief = RIDGE,
                        font = ("goundy old style", 15)
                        )
        self.category.place(x = 900, y = 470)

        self.update_content()

#===========================================================================================================================================================

    def Customers(self) :
        self.new_win = Toplevel(self.root)
        self.new_obj = Customers(self.new_win)

    def category(self) :
        self.new_win = Toplevel(self.root)
        self.new_obj = Category(self.new_win)

    def products(self) :
        self.new_win = Toplevel(self.root)
        self.new_obj = Products(self.new_win)

    def Bills(self) :
        self.new_win = Toplevel(self.root)
        self.new_obj = Bills(self.new_win)

    def exit(self):
        response = messagebox.askyesno("Exit", "Exit App?", parent = self.root)
        if response == True:
            self.root.destroy()

    def update_content(self):

        date_ = time.strftime("%d-%m-%Y")
        time_ = time.strftime("%I : %M : %S  %p")
        
        self.label_clock.config(
                                text = f"\t\t\tWelcome to Shop Management System\t\t\t\tDate : {str(date_)}\t\t\t\t\tTime : {str(time_)}",
                                )
        
        self.cur.execute("SELECT * FROM customers")
        customers = self.cur.fetchall()
        
        self.cur.execute("SELECT * FROM products")
        products = self.cur.fetchall()        

        self.cur.execute("SELECT * FROM category")
        category = self.cur.fetchall()

        bills = os.listdir("D:/Python Projects/Shop Management System/Bills")

        self.Total_CS.config(text = f"Total Customers\n[ {len(customers)} ]")
        self.Products.config(text = f"Total Products\n[ {len(products)} ]")
        self.MyBill.config(text = f"Total Bills\n[ {len(bills)} ]")
        self.category.config(text = f"Total Categories\n[ {len(category)} ]")

        self.label_clock.after(1000, self.update_content)
        
if __name__ == "__main__" :
    root = Tk()
    ob1 = SMS(root)
    root.mainloop()