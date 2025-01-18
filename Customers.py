from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class Customers :
    def __init__(self, root) :
        self.root = root
        self.root.geometry("1120x530+210+130")
        self.root.resizable(0, 0)
        self.root.config(bg = "#88cffa")
        self.root.title("Customers")
        self.root.focus_force()

        self.var_searchBy = StringVar()
        self.var_search_txt = StringVar()

        self.var_customer_id = StringVar()
        self.var_customer_name = StringVar()
        self.var_customer_contact_no = StringVar()
        self.var_customer_gender = StringVar()

        con = sqlite3.connect(database = r"sms.db")
        cur = con.cursor()

#==================================Shortcut Keys=========================================================

        self.root.bind("<Control-s>", lambda e, cur = cur, con = con  : self.add(con, cur, e))
        self.root.bind("<Control-u>", lambda e, cur = cur, con = con : self.update(con, cur, e))
        self.root.bind("<Control-d>", lambda e, cur = cur, con = con : self.delete(con, cur, e))
        self.root.bind("<Control-k>", lambda e, cur = cur, con = con : self.clear(cur, e))

#========================================================================================================

        SearchFrame = LabelFrame(
                                 self.root,
                                 text = "Search Customers",
                                 font = ("goundy old style", 10, "bold"),
                                 bg = "#88cffa",
                                 bd = 2,
                                 relief = RIDGE
                                )
        SearchFrame.place(x = 250, y = 20, width = 600, height = 60)

        cmd_search = ttk.Combobox(SearchFrame,
                                  textvariable = self.var_searchBy,
                                  values = ("Search by", "Name", "Contact", "CID"),
                                  state = "readonly",
                                  font = ("goundy old style", 10),
                                  justify = CENTER
                                  )
        cmd_search.place(x = 10, y = 10, width = 180)
        cmd_search.current(0)

        txt_search = Entry(SearchFrame,
                           textvariable = self.var_search_txt,
                           font = ("goundy old style", 12),
                           bg = "lightyellow"
                           )
        txt_search.bind("<Return>", lambda ev, cur = cur : self.search(cur, ev))
        txt_search.place(x = 210, y = 10)

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
        search_btn.place(x = 430, y = 5, width = 100, height = 25)

        detail_lbl = Label(self.root,
                           text = "Customer Details",
                           bg = "#0f4d7d",
                           fg = "white",
                           font = ("goundy old style", 15, "bold")
                           ).place(x = 0, y = 100, relwidth = 1)

        customer_id = Label(self.root,
                           text = "Customer ID",
                           bg = "#88cffa",
                           font = ("goundy old style", 12, "bold")
                           ).place(x = 50, y = 150)

        customer_name = Label(self.root,
                           text = "Name",
                           bg = "#88cffa",
                           font = ("goundy old style", 12, "bold")
                           ).place(x = 380, y = 150)

        customer_contact_no = Label(self.root,
                           text = "Conatact No",
                           bg = "#88cffa",
                           font = ("goundy old style", 12, "bold")
                           ).place(x = 750, y = 150)

        customer_id_txt = Entry(self.root,
                           textvariable = self.var_customer_id,
                           bg = "lightyellow",
                           font = ("goundy old style", 10)
                           ).place(x = 170, y = 150, width = 180, height = 25)

        customer_name_txt = Entry(self.root,
                           textvariable = self.var_customer_name,
                           bg = "lightyellow",
                           font = ("goundy old style", 10)
                           ).place(x = 470, y = 150, width = 200, height = 25)

        customer_contact_no_txt = Entry(self.root,
                           textvariable = self.var_customer_contact_no,
                           bg = "lightyellow",
                           font = ("goundy old style", 10)
                           ).place(x = 870, y = 150, width = 180, height = 25)


        customer_gender = Label(self.root,
                           text = "Gender",
                           bg = "#88cffa",
                           font = ("goundy old style", 12, "bold")
                           ).place(x = 50, y = 230)

        customer_address = Label(self.root,
                           text = "Address",
                           bg = "#88cffa",
                           font = ("goundy old style", 12, "bold")
                           ).place(x = 380, y = 230)

        customer_gender_txt = ttk.Combobox(self.root,
                           textvariable = self.var_customer_gender,
                           font = ("goundy old style", 10),
                           state = "readonly",
                           values = ("Select", "Male", "Female", "Other")
                           )
        customer_gender_txt.place(x = 170, y = 230, width = 180, height = 25)
        customer_gender_txt.current(0)


        self.customer_address_txt = Text(self.root,
                           bg = "#FFFFED",
                           font = ("goundy old style", 10)
                           )
        self.customer_address_txt.place(x = 470, y = 230, width = 200, height = 50)        

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
        save_btn.place(x = 650, y = 300, width = 100, height = 25)

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
        update_btn.place(x = 770, y = 300, width = 100, height = 25)

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
        delete_btn.place(x = 890, y = 300, width = 100, height = 25)

        clear_btn = Button(self.root,
                            text = "Clear",
                            font = ("goundy old style", 10, "bold"),
                            bg = "grey",
                            bd = 2,
                            command = lambda : self.clear(cur, ev = 1),
                            fg = "white",
                            cursor = "hand2",
                            relief = RIDGE
                            )
        clear_btn.place(x = 1010, y = 300, width = 100, height = 25)

        Customer_Frame = Frame(self.root,
                               bg = "white",
                               bd = 3,
                               relief = RIDGE
                               )
        Customer_Frame.place(x = 0, y = 330, relwidth = 1, height = 200)
        
        scrolly = Scrollbar(Customer_Frame,
                           orient = VERTICAL
                           )
        
        scrollx = Scrollbar(Customer_Frame,
                           orient = HORIZONTAL
                           )

        self.customer_table = ttk.Treeview(
                                     Customer_Frame,
                                     columns = ("cid", "name", "gender", "contact", "address"),                             
                                     yscrollcommand = scrolly.set,
                                     xscrollcommand = scrollx.set 
                                      )
        scrollx.pack(side = BOTTOM, fill = X)
        scrolly.pack(side = RIGHT, fill = Y)

        scrollx.config(command = self.customer_table.xview)
        scrolly.config(command = self.customer_table.yview)

        self.customer_table.heading("cid", text = "CID")
        self.customer_table.heading("name", text = "Name")
        self.customer_table.heading("gender", text = "Gender")
        self.customer_table.heading("contact", text = "Contact No")
        self.customer_table.heading("address", text = "Address")

        self.customer_table["show"] = "headings"

        self.customer_table.column("cid",width = 10, anchor = CENTER)
        self.customer_table.column("name",width = 10, anchor = CENTER)
        self.customer_table.column("gender",width = 10, anchor = CENTER)
        self.customer_table.column("contact",width = 10, anchor = CENTER)
        self.customer_table.column("address",width = 10, anchor = CENTER)

        self.customer_table.pack(fill = BOTH, expand = 1)
        self.customer_table.bind("<ButtonRelease-1>", self.get_data)
        self.show(cur)

#===========================================================================================================================

    

    def add(self, con, cur, ev):
    
        try:
            if self.var_customer_id.get() == "" or self.var_customer_gender.get() == "Select" or self.var_customer_contact_no.get() == "" or self.var_customer_name.get() == "":
                messagebox.showerror("Error", "All fields should be filled", parent = self.root)

            else:
                cur.execute("SELECT * FROM customers where cid = ?", (self.var_customer_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This Customer ID is already assighned", parent = self.root)

                else:
                    cur.execute("INSERT INTO customers (cid, name, gender, contact, address) values(?, ?, ?, ?, ?)",(
                                self.var_customer_id.get(),
                                self.var_customer_name.get(),
                                self.var_customer_gender.get(),
                                self.var_customer_contact_no.get(),
                                self.customer_address_txt.get("1.0", END)
                                ))
                    
                    con.commit()
                    messagebox.showinfo("Success", "Customer Added Successfully", parent = self.root)
                    self.show(cur)

                    self.clear(cur, ev = 1)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def show(self, cur):

        try:
            cur.execute("SELECT * FROM customers")
            rows = cur.fetchall()

            self.customer_table.delete(*self.customer_table.get_children())

            for row in rows:
                self.customer_table.insert("", END, values = row)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def get_data(self, ev):
        data = self.customer_table.focus()
        content = (self.customer_table.item(data))
        row = content["values"]

        self.var_customer_id.set(row[0]),
        self.var_customer_name.set(row[1]),
        self.var_customer_gender.set(row[2]),
        self.var_customer_contact_no.set(row[3]),
        self.customer_address_txt.delete("1.0", END)
        self.customer_address_txt.insert(END, row[4])

    def update(self, con, cur, ev):

        try:
            if self.var_customer_id.get() == "" or self.var_customer_gender.get() == "Select" or self.var_customer_contact_no.get() == "" or self.var_customer_name.get() == "":
                messagebox.showerror("Error", "All fields should be filled", parent = self.root)

            else:
                cur.execute("SELECT * FROM customers where cid = ?", (self.var_customer_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Customer ID", parent = self.root)

                else:
                    cur.execute("UPDATE customers set name = ?, gender = ?, contact = ?, address = ? where cid = ?",(
                                self.var_customer_name.get(),
                                self.var_customer_gender.get(),
                                self.var_customer_contact_no.get(),
                                self.customer_address_txt.get("1.0", END),
                                self.var_customer_id.get()
                                ))
                    
                    con.commit()
                    messagebox.showinfo("Success", "Customer Info Updated Successfully", parent = self.root)
                    self.show(cur)

                    self.clear(cur, ev = 1)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def delete(self, con, cur, ev):
        
        try :
            cur.execute("SELECT * FROM customers where cid = ?", (self.var_customer_id.get(),))
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Invalid Customer ID", parent = self.root)

            else:
                yesno = messagebox.askyesno("Confirmation", f"Are you sure want to delete {self.var_customer_name.get()}", parent = self.root)

                if yesno == True:
                    cur.execute("DELETE from customers where cid = ?", (self.var_customer_id.get(),))
                    con.commit()

                    messagebox.showinfo("Success", f"Successfully Deleted {self.var_customer_name.get()}", parent = self.root)
                    self.show(cur)

                    self.clear(cur, ev = 1)
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def clear(self, cur, ev):
        self.var_customer_id.set(""),
        self.var_customer_name.set(""),
        self.var_customer_gender.set("Select"),
        self.var_customer_contact_no.set(""),
        self.customer_address_txt.delete("1.0", END)
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
                cur.execute(f"SELECT * FROM customers where {self.var_searchBy.get()} LIKE '%{self.var_search_txt.get()}%'")
                rows = cur.fetchall()

                if len(rows) != 0:
                    self.customer_table.delete(*self.customer_table.get_children())

                    for row in rows:
                        self.customer_table.insert("", END, values = row)

                else:
                    messagebox.showerror("Error", "No Record Found!", parent = self.root)
            
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)
            
if __name__ == "__main__" :
    root = Tk()
    ob1 = Customers(root)
    root.mainloop()