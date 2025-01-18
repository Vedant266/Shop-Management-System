from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile

class NewBill :
    def __init__(self, root) :
        self.root = root
        self.root.geometry("1360x700+0+0")
        self.root.title("Shop Management System | Developed by Vedant")
        
        self.root.icon_image = PhotoImage(file = "images/logo1.png")
#===========================================================================================================
        
        self.con = sqlite3.connect(database = r"sms.db")
        self.cur = self.con.cursor()
        self.chk_print = 0

        self.cart_list = []
        self.var_discount = StringVar()
        self.var_name = StringVar()
        self.var_contact_no = StringVar()
        self.var_pname = StringVar()
        self.var_stock = StringVar()
        self.var_cname = StringVar()

        self.var_pqty = StringVar()
        self.var_balance = IntVar()
        self.var_recieved = StringVar()
        self.var_change = IntVar()

#===========================================================================================================
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
                                self.root,
                                text = "\t\t\tWelcome to Shop Management System\t\t\t\tDate : DD/MM/YYYY\t\t\t\tTime : HH : MM : SS",
                                bg = "grey",
                                fg = "white",
                                anchor = "w",
                                font = ("times of now", 10),                                
                                )
        self.label_clock.place(x = 0, y = 70, relwidth = 1, height = 30)
        
        main_product_frame = Frame(
                                    self.root,
                                    bd = 4,
                                    relief = RIDGE,
                                    width = 400,
                                    bg = "white"    
                                   )
        main_product_frame.place(x = 6, y = 110, width = 410, height = 550)

        title_products = Label(
                                main_product_frame,
                                text = "All Products",
                                font = ("goundy old style", 20, "bold"),
                                bg = "#262626",
                                fg = "white"
                               ).pack(side = TOP, fill = X)
                
        SearchFrame = Frame(
                            main_product_frame,
                            bd = 2,
                            relief = RIDGE,
                            bg = "white",
                            )
        SearchFrame.place(x = 2, y = 42, width = 398, height = 90)

        lbl_search_title = Label(
                                SearchFrame,
                                text = "Search Product | By Name",
                                font = ("goundy old style", 15, "bold"),
                                fg = "green",
                                bg = "white"
                                 ).place(x = 0, y = 5)
        
        lbl_name = Label(
                        SearchFrame,
                        text = "Product Name",
                        font = ("goundy old style", 13),
                        bg = "white"
                        ).place(x = 0, y = 50)
        
        name_txt = Entry(
                         SearchFrame,
                         textvariable = self.var_name,
                         font = ("goundy old style", 12),
                         bg = "lightyellow"
                        )
        name_txt.bind("<Return>", self.search)
        name_txt.place(x = 115, y = 52)

        search_btn = Button(
                            SearchFrame,
                            text = "Search",
                            command = lambda :self.search(ev = 1),
                            font = ("timesnewroman 12"),
                            bg = "green",
                            fg = "white",
                            cursor = "hand2"
                            ).place(x = 310, y = 52, height = 25)
        
        show_all_btn = Button(
                            SearchFrame,
                            text = "Show All",
                            command = self.show,
                            font = ("timesnewroman 12"),
                            bg = "black",
                            fg = "white",
                            cursor = "hand2"
                            ).place(x = 310, y = 12, height = 25)


        product_frame = Frame(
                              main_product_frame,
                              bd = 2,
                              relief = RIDGE,
                              bg = "white",
                              )
        product_frame.place(x = 2, y = 140, width = 398, height = 390)
        
        
        scrolly = Scrollbar(product_frame,
                           orient = VERTICAL
                           )
        
        scrollx = Scrollbar(product_frame,
                           orient = HORIZONTAL
                           )

        self.product_table = ttk.Treeview(
                                product_frame,
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

        self.product_table.column("pid", width = 25, anchor = CENTER)
        self.product_table.column("category", width = 90, anchor = CENTER)
        self.product_table.column("name", width = 150, anchor = CENTER)
        self.product_table.column("price", width = 100, anchor = CENTER)
        self.product_table.column("quantity", width = 100, anchor = CENTER)
        self.product_table.column("status", width = 100, anchor = CENTER)

        self.product_table.pack(fill = BOTH, expand = 1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        cart_frame = Frame(
                        self.root,
                        bd = 2,
                        relief = RIDGE,
                        bg = "white",
                        )
        cart_frame.place(x = 425, y = 110, width = 450, height = 550)

        detail_lbl = Label(
                           cart_frame,
                           text = "Customer Details",
                           bg = "skyblue",
                           font = ("timesnewroman 20 bold"),
                           ).pack(side = TOP, fill = X)

        detail_frame = Frame(
                cart_frame,
                bd = 2,
                relief = RIDGE,
                bg = "white",
                 )
        detail_frame.place(x = 2, y = 42, width = 440, height = 90)

        lbl_cname = Label(
                          detail_frame,
                          text = "Name",
                          font = ("timesnewroman 13"),
                          bg = "white" 
                           ).place(x = 10, y = 20)
        
        lbl_contact_no = Label(
                          detail_frame,
                          text = "Contact No",
                          font = ("timesnewroman 13"),
                          bg = "white" 
                           ).place(x = 10, y = 50)
        
        cname_txt = Entry(
                        detail_frame,
                        textvariable = self.var_cname,
                        font = ("goundy old style", 12),
                        bg = "lightyellow"
                        )
        cname_txt.place(x = 110, y = 20)

        cno_txt = Entry(
                        detail_frame,
                        textvariable = self.var_contact_no,
                        font = ("goundy old style", 12),
                        bg = "lightyellow"
                        )
        cno_txt.place(x = 110, y = 50)

        cart = Frame(
                cart_frame,
                bd = 2,
                relief = RIDGE,
                bg = "white",
                )
        cart.place(x = 2, y = 135, width = 440, height = 300)

        self.cart_table = ttk.Treeview(
                                cart,
                                columns = ("name", "price_qty", "quantity", "price"),                             
                                )

        self.cart_table.heading("name", text = "Name")
        self.cart_table.heading("price_qty", text = "Price per Unit")
        self.cart_table.heading("quantity", text = "Quantity")
        self.cart_table.heading("price", text = "Total Price")

        self.cart_table["show"] = "headings"

        self.cart_table.column("name", width = 70, anchor = CENTER)
        self.cart_table.column("price_qty", width = 10, anchor = CENTER)
        self.cart_table.column("price", width = 10, anchor = CENTER)
        self.cart_table.column("quantity", width = 10, anchor = CENTER)
        self.cart_table.bind("<ButtonRelease - 1>", self.get_data_for_cart)
        self.cart_table.pack(fill = BOTH, expand = 1)


        add_to_cart_btn = Button(
                            cart_frame,
                            text = "Add | Update Cart",
                            command = lambda : self.add_to_cart(ev = None),
                            font = ("timesnewroman 12"),
                            bg = "orange",
                            fg = "white",
                            cursor = "hand2"
                            ).place(x = 140, y = 500, height = 30, width = 140)

        add_to_cart_btn = Button(
                            cart_frame,
                            text = "Clear",
                            command = self.clear,
                            font = ("timesnewroman 12"),
                            bg = "grey",
                            fg = "white",
                            cursor = "hand2"
                            ).place(x = 300, y = 500, height = 30, width = 140)        


        lbl_pname = Label(
                          cart_frame,
                          text = "Product",
                          font = ("timesnewroman 12"),
                          bg = "white" 
                           ).place(x = 7, y = 450)
        

        pname_txt = Entry(
                        cart_frame,
                        textvariable = self.var_pname,
                        font = ("goundy old style", 12),
                        bg = "lightyellow"
                        )
        pname_txt.place(x = 80, y = 450)

        lbl_qty = Label(
                          cart_frame,
                          text = "Qty",
                          font = ("timesnewroman 12"),
                          bg = "white" 
                           ).place(x = 270, y = 450)
        

        self.qty_frame = Frame(
                        cart_frame,
                        bd = 2,
                        relief = RIDGE, 
                        bg = "lightyellow"
                        )
        self.qty_frame.place(x = 310, y = 450, height = 30, width = 120)

        lbl_stock = Label(
                          cart_frame,
                          text = "In Stock : ",
                          font = ("timesnewroman 12"),
                          bg = "white" 
                           ).place(x = 7, y = 500)
        
        self.stock_txt = Entry(
                        cart_frame,
                        bd = 0,
                        state = "readonly",
                        textvariable = self.var_stock,
                        font = ("goundy old style", 12),
                        bg = "lightyellow",
                        justify = CENTER
                        )
        self.stock_txt.place(x = 80, y = 502, width = 30)

        add_btn = Button(
                        self.qty_frame,
                        text = "+",
                        command = self.add_qty,
                        font = ("timesnewroman 15"),
                        ).pack(side = RIGHT, fill = Y)
        
        substract_btn = Button(
                        self.qty_frame,
                        command = self.sub_qty,
                        text = "-",
                        font = ("timesnewroman 15"),
                        ).pack(side = LEFT, fill = Y)
        
        self.add_txt = Entry(
                        self.qty_frame,
                        textvariable = self.var_pqty,
                        font = ("timesnewroman 12"),
                        bd = 1,
                        relief = RIDGE,
                        justify = CENTER
                        )
        self.add_txt.bind("<Return>", self.add_to_cart)
        self.add_txt.place(x = 25, y = 0, height = 28, width = 60)

#============================================Payment Frame===============================================================
        
        self.payment_frame = Frame(
                        self.root,
                        bd = 2,
                        relief = RIDGE,
                        bg = "white",
                        )
        self.payment_frame.place(x = 885, y = 110, width = 450, height = 350)
        
        lbl_ptitle = Label(
                            self.payment_frame,
                            text = "Bill",
                            bg = "yellow",
                            font = ("timesnewroman 20 bold"),
                            ).pack(side = TOP, fill = X)

        self.lbl_changne = Label(
                            self.payment_frame,
                            text = "",
                            bg = "white",
                            font = ("timesnewroman 15 bold"),
                            )
        self.lbl_changne.place(x = 15, y = 210)

        discount_btn = ttk.Combobox(
                        self.payment_frame,
                        textvariable = self.var_discount,
                        values = ("Discount %", "5", "10", "15", "20"),
                        font = ("timesnewroman 13"),
                        state = "readonly",
                        justify = CENTER
                        )
        discount_btn.place(x = 20, y = 300, width = 120, height = 30)
        discount_btn.current(0)

        self.lbl_balance = Label(
                                self.payment_frame,
                                text = "",
                                bg = "white",
                                font = ("timesnewroman 15 bold"),
                                )
        self.lbl_balance.place(x = 15, y = 70)
        
        self.lbl_recieved = Label(
                            self.payment_frame,
                            text = "",
                            bg = "white",
                            font = ("timesnewroman 15 bold"),
                            )
        self.lbl_recieved.place(x = 15, y = 140)

        calculate_btn = Button(
                        self.payment_frame,
                        command = self.calculate_bill,
                        bg = "blue",
                        fg = "white",
                        cursor = "hand2",
                        text = "Calculate Bill",
                        font = ("timesnewroman 13"),
                        ).place(x = 160, y = 300, width = 120, height = 30)
            
        print_btn = Button(
                        self.payment_frame,
                        command = self.print_bill,
                        bg = "green",
                        fg = "white",
                        cursor = "hand2",
                        text = "Print Bill",
                        font = ("timesnewroman 13"),
                        ).place(x = 300, y = 300, width = 120, height = 30)

        lbl_note = Label(
                      self.root,
                      text = "Note : Enter Zero Quantity to Remove Product From the Cart",
                      font = ("times of now", 11, "bold"),
                      fg = "red"
                      ).place(x = 890, y = 500)
        

        self.show()
        self.update_date_and_time()

#========================================================================================================================================================

    def update_date_and_time(self):
        date_ = time.strftime("%d-%m-%Y")
        time_ = time.strftime("%I : %M : %S  %p")
        
        self.label_clock.config(
                                text = f"\t\t\tWelcome to Shop Management System\t\t\t\tDate : {str(date_)}\t\t\t\t\tTime : {str(time_)}",
                                )

        self.label_clock.after(1000, self.update_date_and_time)

    def show(self):

        try:
            self.cur.execute("SELECT * FROM products")
            rows = self.cur.fetchall()

            self.product_table.delete(*self.product_table.get_children())

            for row in rows:
                if row[5] == "Active":
                    self.product_table.insert("", END, values = row)
            
            self.var_name.set("")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def add_qty(self):

        try:
            self.var_pqty.set(int(self.var_pqty.get()) + 1)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)


    def sub_qty(self):

        try:
            if int(self.var_pqty.get()) > 0:
                self.var_pqty.set(int(self.var_pqty.get()) - 1)

            else : 
                messagebox.showerror("Error", "Quantity cannot be Negative", parent = self.root)

        except Exception as ex:
            messagebox.showerror("Error", "Please Enter Valid Quantity", parent = self.root)


    def calulate_change(self, ev):
        
        try:

            if self.var_balance.get() <= int(self.var_recieved.get()):

                self.var_change.set(int(self.var_recieved.get()) - self.var_balance.get())
                self.lbl_changne.config(text = f"Change Due : {self.var_change.get()}")

                self.generete_bill()
                self.update_qty()
                self.show() 
                self.clear()

            else : 
                messagebox.showerror("Error", "Recieved Amount is Less than Balance!", parent = self.root)


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def update_qty(self):
        for i in self.cart_list:

            if int(i[2]) != int(i[4]):
                status = "Active"
            
            else:
                status = "Inactive"

            self.cur.execute("UPDATE products SET quantity = ?, status = ? where name = ?", (
                int(i[4]) - int(i[2]),
                status,
                i[0]
            ))
            self.con.commit()

    def get_data(self, ev):
        data = self.product_table.focus()
        content = (self.product_table.item(data))
        row = content["values"]

        self.var_stock.set(row[4])
        self.var_pname.set(row[2])
        self.var_pqty.set("1")

    def get_data_for_cart(self, ev):
        data = self.cart_table.focus()
        content = (self.cart_table.item(data))
        row = content["values"]

        data_ = self.product_table.focus()
        content_ = (self.product_table.item(data))
        row_ = content_["values"]

        self.var_stock.set(row_[4])
        self.var_pname.set(row[0])
        self.var_pqty.set(row[2])

    def add_to_cart(self, ev):

        try:
            
            if self.var_pname.get() == "":
                messagebox.showerror("Error", "Please Enter Product Name", parent = self.root)
            
            else : 
                self.cur.execute("SELECT price, quantity FROM products where name = ?", (self.var_pname.get().capitalize(),))
                data = self.cur.fetchone()
                self.price = data[0]
                self.stock = data[1]

                if len(self.price) == 0:
                    messagebox.showerror("Error", "Invalid Product!", parent = self.root)

                else:
                    if int(self.var_pqty.get()) > int(self.stock):
                        messagebox.showerror("Error", "Insuffficient Quantity !", parent = self.root)
                    
                    else:
                        cart_data = [self.var_pname.get().capitalize(), float(self.price), str(self.var_pqty.get()), float(int(self.var_pqty.get()) * int(self.price)), self.var_stock.get()]
                        
                        present = "no"
                        index_ = 0

                        for row in self.cart_list:
                            if self.var_pname.get() == row[0]:
                                present = "yes"
                                break
                            index_ += 1

                        if present == 'yes':
                            response = messagebox.askyesno("Confirm", "Product Already Added Do you want to Update/Remove it?", parent = self.root)
                            
                            if response == True:
                                if self.var_pqty.get() == "0":
                                    self.cart_list.pop(index_)
                                    
                                else:    
                                    self.update_cart(index_)

                        else: 
                            self.cart_list.append(cart_data)
                            self.var_pname.set("")
                            self.var_pqty.set("0")
                            self.var_name.set("")
                            self.var_stock.set("")

                        self.show_cart()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def calculate_bill(self):

        if self.var_cname.get() == "" and self.var_contact_no.get() == "":
            messagebox.showerror("Error", "Please Enter Customer Details!", parent = self.root)

        else:
            if len(self.cart_list) != 0:
                self.bill_amt = 0
                net_pay = 0

                for i in self.cart_list:
                    self.bill_amt += float(i[3])

                if self.var_discount.get() != "Discount %":
                    self.discount = (self.bill_amt * int(self.var_discount.get())) / 100
                    net_pay = self.bill_amt - self.discount

                    self.var_balance.set(float(net_pay))

                else : 
                    self.var_balance.set(float(self.bill_amt))
                

                self.lbl_balance.config(text = f"Balance Due : {self.var_balance.get()}")
                self.lbl_recieved.config(text = "Amt Recieved : ")

                self.recieved_txt = Entry(
                                self.payment_frame,
                                textvariable = self.var_recieved,
                                font = ("times new roman", 15),
                                bg = "lightyellow"
                                )
                self.recieved_txt.bind("<Return>", self.calulate_change)
                self.recieved_txt.place(x = 180, y = 140)
                self.var_recieved.set("")

            else :
                messagebox.showerror("Error", "Pleas Add Products to the Cart!", parent = self.root)

    def show_cart(self):        
        
        self.cart_table.delete(*self.cart_table.get_children())

        for row in self.cart_list:                        
            self.cart_table.insert("", END, values = row)

    def update_cart(self, index_):
        self.cart_list[index_][2] = self.var_pqty.get()
        self.cart_list[index_][3] = float(self.var_pqty.get() * int(self.price))

        self.var_pname.set("")
        self.var_pqty.set("0")
        self.var_name.set("")
        self.var_stock.set("")

    def search(self, ev):

        if self.var_name.get() == "":
            messagebox.showerror("Error", "Please Enter Name", parent = self.root)

        else:

            try :
                self.cur.execute(f"SELECT * FROM products where name LIKE '%{self.var_name.get().capitalize()}%'")
                rows = self.cur.fetchall()

                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())

                    for row in rows:
                        self.product_table.insert("", END, values = row)

                else:
                    messagebox.showerror("Error", "No Record Found!", parent = self.root)
            
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def clear(self):
        res = messagebox.askyesno("Confirm", "Are you sure you want to Clear All Data ?", parent = self.root)

        if res == True:
            self.cart_list.clear()
            self.var_cname.set("")
            self.var_contact_no.set("")            
            self.var_name.set("")            
            self.var_pname.set("")            
            self.var_pqty.set("0")            
            self.var_stock.set("")
            self.var_name.set("")
            self.var_discount.set("Discount %")

            self.recieved_txt.config(text = "")
            self.lbl_balance.config(text = "")
            self.lbl_changne.destroy()
            self.recieved_txt.destroy()
            self.lbl_recieved.config(text = "")

            self.show()
            self.show_cart()            

    def generete_bill(self):
        self.bill_top()
        self.bill_middle()
        self.bill_bottom()

        messagebox.showinfo("Success", "Bill has been saved in backend!", parent = self.root)
        self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_template = f'''
\t\t\t\t\t\t  Vedant Super Market
\t\t\t\t  Phone No. : 9892222900, Pune-412105
{str("="*70)}
Customer Name : {self.var_cname.get()}
Phone No. : {self.var_contact_no.get()}
Bill No. : {str(self.invoice)}\t\t\t\t\t\t\t\tDate : {str(time.strftime("%d/%m/%Y"))}
{str("="*70)}
 Product Name\t\t\tPrice Per Unit\t\tQty\t\t\tTotal Price
{str("="*70)}
                            '''
        self.file = open(f"D:/Python Projects/Shop Management System/Bills/{self.invoice}.txt", "w")
        self.file.write(bill_top_template)

    def bill_middle(self):
        for row in self.cart_list:
            name = row[0]
            name = name.split(" ")
            if len(name) > 2:
                self.file.write(f"\n {name[0]} {name[1]}\t\t\tRs. {row[1]}\t\t\t{row[2]}\t\t\tRs. {row[3]}\n")

                for i in range(2, (len(name))):
                    self.file.write(f" {name[i]}\n")

            else:
                self.file.write(f" \n {row[0]}\t\t\t\t\tRs. {row[1]}\t\t\t{row[2]}\t\t\tRs. {row[3]}\n")
        

    def bill_bottom(self):
        if self.var_discount.get() != "Discount %":
            bill_bottom_template = f'''
{str("=" * 70)}
Balance Due\t\t\t\t\t\t\t\t\t\t\t\tRs. {float(self.bill_amt)}
Discount\t\t\t\t\t\t\t\t\t\t\t\tRs. {float(self.discount)}
{str("=" * 70)}
Final Total\t\t\t\t\t\t\t\t\t\t\t\tRs. {float(self.var_balance.get())}
{str("=" * 70)}
                        Thank You! Visit Again!							
                                '''

        else:
            bill_bottom_template = f'''
{str("=" * 70)}
Balance Due\t\t\t\t\t\t\t\t\t\t\t\tRs. {float(self.bill_amt)}
{str("=" * 70)}
                        Thank You! Visit Again!							
                                '''

        self.file.write(bill_bottom_template)
        self.file.close()

    def print_bill(self):
        if(self.chk_print == 1):
            os.startfile(f"D:/Python Projects/Shop Management System/Bills/{self.invoice}.txt", 'print')

        else:
            messagebox.showerror("Error", "Please Calculate the bill First!", parent = self.root)


if __name__ == "__main__" :
    root = Tk()
    ob1 = NewBill(root)
    root.mainloop()