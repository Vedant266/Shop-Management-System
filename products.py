from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class Products :
    def __init__(self, root) :
        self.root = root
        self.root.geometry("1120x530+210+130")
        self.root.config(bg = "yellow")
        self.root.resizable(0, 0)
        self.root.title("Products")
        self.root.focus_force()
        
        self.cat_list = []
        
        self.var_searchBy = StringVar()
        self.var_search_txt = StringVar()
        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_price = StringVar()
        self.var_name = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        
        con = sqlite3.connect(database = r"sms.db")
        cur = con.cursor()

#==================================Shortcut Keys=========================================================

        self.root.bind("<Control-s>", lambda e, cur = cur, con = con  : self.add(con, cur, e))
        self.root.bind("<Control-u>", lambda e, cur = cur, con = con : self.update(con, cur, e))
        self.root.bind("<Control-d>", lambda e, cur = cur, con = con : self.delete(con, cur, e))
        self.root.bind("<Control-k>", lambda e, cur = cur, con = con : self.clear(cur, e))

#========================================================================================================

        product_frame = Frame(
                              self.root,
                              bd = 2,
                              bg = "yellow",
                              relief = RIDGE
                              )
        product_frame.place(x = 10, y = 10, width = 480, height = 500)

        lbl_title = Label(
                          product_frame,
                          text = "Product Details",
                          font = ("goundy old style", 20, "bold"),
                          bg = "#0f4d7d",
                          fg = "white"
                           ).pack(side = TOP, fill = X)

        lbl_id = Label(
                          product_frame,
                          text = "Product ID",
                          bg = "yellow",
                          font = ("goundy old style", 15, "bold"),
                           ).place(x = 20, y = 70)
        
        lbl_cat = Label(
                          product_frame,
                          text = "Category",
                          bg = "yellow",
                          font = ("goundy old style", 15, "bold"),
                           ).place(x = 20, y = 130)
        
        lbl_Name = Label(
                          product_frame,
                          text = "Name",
                          bg = "yellow",
                          font = ("goundy old style", 15, "bold"),
                           ).place(x = 20, y = 190)
        
        lbl_price = Label(
                          product_frame,
                          bg = "yellow",
                          text = "Price",
                          font = ("goundy old style", 15, "bold"),
                           ).place(x = 20, y = 250)

        lbl_qty = Label(
                          product_frame,
                          text = "Quantity",
                          bg = "yellow",
                          font = ("goundy old style", 15, "bold"),
                           ).place(x = 20, y = 310)
        
        lbl_status = Label(
                          product_frame,
                          text = "Status",
                          bg = "yellow",
                          font = ("goundy old style", 15, "bold"),
                           ).place(x = 20, y = 370)
        
        self.pid_txt = Entry(
                         product_frame,
                         textvariable = self.var_pid,
                         font = ("goundy old style", 12),
                         bg = "lightyellow"
                         )
        self.pid_txt.place(x = 170, y = 75, width = 180)
        

        self.cat_txt = ttk.Combobox(
                           product_frame,
                           textvariable = self.var_cat,
                           values = self.cat_list,
                           state = "readonly",
                           font = ("goundy old style", 12),
                           justify = CENTER
                           )
        self.cat_txt.place(x = 170, y = 135, width = 180)
        self.cat_txt.set("Select")

        name_txt = Entry(
                         product_frame,
                         textvariable = self.var_name,
                         font = ("goundy old style", 12),
                         bg = "lightyellow"
                         ).place(x = 170, y = 195, width = 180)
        
        price_txt = Entry(
                         product_frame,
                         textvariable = self.var_price,
                         font = ("goundy old style", 12),
                         bg = "lightyellow"
                         ).place(x = 170, y = 255, width = 180)
        
        quantity_txt = Entry(
                         product_frame,
                         textvariable = self.var_qty,
                         font = ("goundy old style", 12),
                         bg = "lightyellow"
                         ).place(x = 170, y = 315, width = 180)
        
        status_txt = ttk.Combobox(
                           product_frame,
                           textvariable = self.var_status,
                           values = ("Active", "Inactive"),
                           state = "readonly",
                           font = ("goundy old style", 12),
                           justify = CENTER
                           )
        status_txt.place(x = 170, y = 365, width = 180)
        status_txt.current(0)

        save_btn = Button(self.root,
                            text = "Save",
                            font = ("goundy old style", 10, "bold"),
                            bg = "green",
                            bd = 2,
                            fg = "white",
                            command = lambda: self.add(con, cur, ev = 1),
                            cursor = "hand2",
                            relief = RIDGE
                            )
        save_btn.place(x = 20, y = 450, width = 100, height = 25)

        update_btn = Button(self.root,
                            text = "Update",
                            font = ("goundy old style", 10, "bold"),
                            bg = "blue",
                            command = lambda: self.update(con, cur, ev = 1),
                            fg = "white",
                            bd = 2,
                            cursor = "hand2",
                            relief = RIDGE
                            )
        update_btn.place(x = 140, y = 450, width = 100, height = 25)

        delete_btn = Button(self.root,
                            text = "Delete",
                            font = ("goundy old style", 10, "bold"),
                            bg = "red",
                            bd = 2,
                            fg = "white",
                            command = lambda : self.delete(con, cur, ev = 1),
                            cursor = "hand2",
                            relief = RIDGE
                            )
        delete_btn.place(x = 260, y = 450, width = 100, height = 25)

        clear_btn = Button(self.root,
                            text = "Clear",
                            font = ("goundy old style", 10, "bold"),
                            bg = "grey",
                            bd = 2,
                            command = lambda : self.clear(cur, ev=None),
                            fg = "white",
                            cursor = "hand2",
                            relief = RIDGE
                            )
        clear_btn.place(x = 380, y = 450, width = 100, height = 25)

        SearchFrame = LabelFrame(
                                 self.root,
                                 text = "Search Products",
                                 font = ("goundy old style", 10, "bold"),
                                 bg = "yellow",
                                 bd = 2,
                                 relief = RIDGE
                                )
        SearchFrame.place(x = 520, y = 20, width = 570, height = 60)

        cmd_search = ttk.Combobox(SearchFrame,
                                  textvariable = self.var_searchBy,
                                  values = ("Search by", "PID", "Category", "Name", "Status"),
                                  state = "readonly",
                                  font = ("goundy old style", 12),
                                  justify = CENTER
                                  )
        cmd_search.place(x = 30, y = 8, width = 150)
        cmd_search.current(0)

        txt_search = Entry(SearchFrame,
                           textvariable = self.var_search_txt,
                           font = ("goundy old style", 13),
                           bg = "lightyellow"
                           )
        txt_search.bind("<Return>", lambda ev, cur = cur : self.search(cur, ev))
        txt_search.place(x = 200, y = 8)

        search_btn = Button(SearchFrame,
                            text = "Search",
                            command = lambda : self.search(cur, ev = 1), 
                            font = ("goundy old style", 10, "bold"),
                            bg = "green",
                            bd = 2,
                            fg = "white",
                            cursor = "hand2",
                            relief = RIDGE
                            )
        search_btn.place(x = 410, y = 3, width = 100, height = 30)
         
        show_Frame = Frame(self.root,
                               bg = "white",
                               bd = 3,
                               relief = RIDGE
                               )
        show_Frame.place(x = 520, y = 100, width = 570, height = 400)

        scrolly = Scrollbar(show_Frame,
                           orient = VERTICAL
                           )
        
        scrollx = Scrollbar(show_Frame,
                           orient = HORIZONTAL
                           )


        self.product_table = ttk.Treeview(
                                     show_Frame,
                                     columns = ("pid",  "category", "name", "price", "quantity", "status"),                             
                                     yscrollcommand = scrolly.set,
                                     xscrollcommand = scrollx.set 
                                      )
        scrollx.pack(side = BOTTOM, fill = X)
        scrolly.pack(side = RIGHT, fill = Y)

        scrollx.config(command = self.product_table.xview)
        scrolly.config(command = self.product_table.yview)

        self.product_table.heading("pid", text = "PID")
        self.product_table.heading("category", text = "Category")
        self.product_table.heading("name", text = "Name")
        self.product_table.heading("price", text = "Price")
        self.product_table.heading("quantity", text = "Quantity")
        self.product_table.heading("status", text = "Status")

        self.product_table["show"] = "headings"

        self.product_table.column("pid", width = 10, anchor = CENTER)
        self.product_table.column("category", width = 30, anchor = CENTER)
        self.product_table.column("name", width = 70, anchor = CENTER)
        self.product_table.column("price", width = 10, anchor = CENTER)
        self.product_table.column("quantity", width = 10, anchor = CENTER)
        self.product_table.column("status", width = 10, anchor = CENTER)

        self.product_table.pack(fill = BOTH, expand = 1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.get_cat(cur)
        self.show(cur)

#=================================================================================================================================

    def get_cat(self, cur):
        
        try:
            cur.execute("SELECT name FROM category")
            cat = cur.fetchall()

            for i in cat:
                self.cat_list.append(i[0])

            self.cat_txt["values"] = self.cat_list
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)


    def add(self, con, cur, ev):

        try:
            if self.var_cat.get() == "Select" or self.var_name.get() == "" or self.var_price.get() == "" or self.var_qty.get() == "":
                messagebox.showerror("Error", "All fields should be filled", parent = self.root)

            else:
                cur.execute("SELECT * FROM products where name = ?", (self.var_name.get().upper(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This Product is already Added!", parent = self.root)

                else:
                    cur.execute("INSERT INTO products (pid, category, name, price, quantity, status) values(?, ?, ?, ?, ?, ?)",(
                                self.var_pid.get(),
                                self.var_cat.get().capitalize(),
                                self.var_name.get().capitalize(),
                                self.var_price.get(),
                                self.var_qty.get(),
                                self.var_status.get(),
                                ))
                    
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent = self.root)
                    self.show(cur)

                    self.clear(cur, ev)

        except Exception as ex:
            messagebox.showerror("Error", f"Product ID Already Exists!", parent = self.root)

    def show(self, cur):

        try:
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()

            self.product_table.delete(*self.product_table.get_children())

            for row in rows:
                self.product_table.insert("", END, values = row)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def get_data(self, ev):
        data = self.product_table.focus()
        content = (self.product_table.item(data))
        row = content["values"]

        self.var_pid.set(row[0])
        self.var_cat.set(row[1]),
        self.var_name.set(row[2]),
        self.var_price.set(row[3]),
        self.var_qty.set(row[4]),
        self.var_status.set(row[5]),
        self.pid_txt["state"] = "disabled"

    def update(self, con, cur, ev):

        try:
            if self.var_cat.get() == "Select" or self.var_name.get() == "" or self.var_price.get() == "" or self.var_qty.get() == "":
                messagebox.showerror("Error", "All fields should be filled", parent = self.root)

            else:
                cur.execute("SELECT * FROM products where pid = ?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "No Product Found", parent = self.root)

                else:
                    cur.execute("UPDATE products set name = ?,category = ?, price = ?, quantity = ?, status = ? where pid = ?",(
                                self.var_name.get().capitalize(),
                                self.var_cat.get().capitalize(),
                                self.var_price.get(),
                                self.var_qty.get(),
                                self.var_status.get(),
                                self.var_pid.get()
                                ))
                    
                    con.commit()
                    messagebox.showinfo("Success", "Product Info Updated Successfully", parent = self.root)
                    self.show(cur)

                    self.clear(cur, ev)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def delete(self, con, cur, ev):
        
        try :
            cur.execute("SELECT * FROM products where pid = ?", (self.var_pid.get(),))
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Invalid Product", parent = self.root)

            else:
                yesno = messagebox.askyesno("Confirmation", f"Are you sure want to delete {self.var_name.get().capitalize()}", parent = self.root)

                if yesno == True:
                    cur.execute("DELETE from products where pid = ?", (self.var_pid.get(),))
                    con.commit()

                    messagebox.showinfo("Success", f"Successfully Deleted {self.var_name.get()}", parent = self.root)
                    self.show(cur)

                    self.clear(cur, ev)
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def clear(self, cur, ev):
        self.pid_txt["state"] = "normal"
        self.var_pid.set(""),
        self.var_name.set(""),
        self.var_cat.set("Select"),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_search_txt.set("")
        self.var_searchBy.set("Search by")

        self.show(cur)

    def search(self, cur, ev):

        if self.var_searchBy.get() == "Search by":
            messagebox.showerror("Error", "Select Search by Option", parent = self.root)

        elif self.var_search_txt.get() == "":
            messagebox.showerror("Error", f"Please Enter {self.var_searchBy.get()}", parent = self.root)

        else:

            try :
                cur.execute(f"SELECT * FROM products where {self.var_searchBy.get()} LIKE '%{self.var_search_txt.get().capitalize()}%'")
                rows = cur.fetchall()

                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())

                    for row in rows:
                        self.product_table.insert("", END, values = row)

                else:
                    messagebox.showerror("Error", "No Record Found!", parent = self.root)
            
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)
            

if __name__ == "__main__" :
    root = Tk()
    ob1 = Products(root)
    root.mainloop()