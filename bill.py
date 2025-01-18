from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import os
from New_billing import NewBill

class Bills :
    
    def __init__(self, root) :
        self.root = root
        self.root.geometry("1120x530+210+130")
        self.root.resizable(0, 0)
        self.root.config(bg = "white")
        self.root.title("My Bills")
        self.root.focus_force()

#===============================================================================

        self.var_invoice = StringVar()
        self.bill_name = []

#===============================================================================


        lbl_title = Label(
                          self.root,
                          text = "My Bills",
                          font = ("goundy old style", 30, "bold"),
                          bg = "#0f4d7d",
                          fg = "white",
                          ).pack(side = TOP, fill = X)
        
        lbl_invoice = Label(
                          self.root,
                          bg = "white",
                          text = "Invoice No.",
                          font = ("times new roman", 15),
                          ).place(x = 350, y = 70)

        invoice_txt = Entry(self.root,
                           textvariable = self.var_invoice,
                           bg = "lightyellow",
                           font = ("goundy old style", 13)
                           )
        invoice_txt.bind("<Return>", lambda ev : self.search(ev))
        invoice_txt.place(x = 460, y = 72)

# ======================Buttons===============================

        search_btn = Button(self.root,
                            text = "Search",
                            command = lambda : self.search(ev = 1),
                            font = ("goundy old style", 10, "bold"),
                            bg = "green",
                            bd = 2,
                            fg = "white",
                            cursor = "hand2",
                            relief = RIDGE
                            )
        search_btn.place(x = 660, y = 70, width = 100, height = 25)

        clear_btn = Button(self.root,
                            text = "Clear",
                            font = ("goundy old style", 10, "bold"),
                            bg = "gray",
                            command = self.clear,
                            fg = "white",
                            bd = 2,
                            cursor = "hand2",
                            relief = RIDGE
                            )
        clear_btn.place(x = 780, y = 70, width = 100, height = 25)

        New_Bill_btn = Button(self.root,
                            text = "New Bill",
                            command = self.new_bill,
                            font = ("goundy old style", 12, "bold"),
                            bg = "blue",
                            bd = 2,
                            fg = "white",
                            cursor = "hand2",
                            relief = RIDGE
                            )
        New_Bill_btn.place(x = 950, y = 90, width = 150, height = 35)

#============================================Frames=============================================
        
        print_Frame = Frame(self.root,
                            bg = "white",
                            bd = 3,
                            relief = RIDGE
                            )
        print_Frame.place(x = 130, y = 150, height = 300, width = 900)

        yscrollbill = Scrollbar(
                            print_Frame,
                            orient = VERTICAL
                            )
        xscrollbill = Scrollbar(
                                print_Frame,
                                orient = HORIZONTAL
                                )

        bill_lbl = Label(
                         print_Frame,
                         text = "Customer Bill",
                         font = ("goundy old style", 20),
                         bg = "orange"
                         ).pack(side = TOP, fill = X)

        self.bill = Text(
                        print_Frame,
                        state = "disabled",
                        bg = "white",
                        yscrollcommand = yscrollbill.set,
                        xscrollcommand = xscrollbill.set
                        )
        yscrollbill.pack(fill = Y, side = RIGHT)
        xscrollbill.pack(fill = X, side = BOTTOM)
        yscrollbill.config(command = self.bill.yview)
        xscrollbill.config(command = self.bill.xview)
        self.bill.pack(fill = BOTH, expand = 1)
        
        self.show()

#===============================================================================================================================

    def show(self):
        del self.bill_name[:]

        for i in os.listdir("Bills"):
            if i.split(".")[-1] == "txt":
                self.bill_name.append(i.split(".")[0])

    def get_bill(self, ev):
        file_index = self.bill_list.curselection()
        file_name = self.bill_list.get(file_index)
        file_data = open(f"D:/Python Projects/Shop Management System/Bills/{file_name}", "r")
        data = file_data.read()

        self.bill["state"] = "normal"

        self.bill.delete("1.0", END)

        self.bill.insert(END, data)

        self.bill["state"] = "disabled"
        
        file_data.close()

    def search(self, ev):

        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Please Enter Invoice No.", parent = self.root)
        
        else:
            if self.var_invoice.get() in self.bill_name:
                file_data = open(f"D:/Python Projects/Shop Management System/Bills/{self.var_invoice.get()}.txt", "r")

                self.bill["state"] = "normal"

                self.bill.delete("1.0", END)

                for i in file_data:
                        self.bill.insert(END, i)

                self.bill["state"] = "disabled"
                
                file_data.close()

            else:
                messagebox.showerror("Error", "Invalid Invoice No.", parent = self.root)

    def clear(self):
        self.show()
        self.bill["state"] = "normal"

        self.bill.delete("1.0", END)
        self.var_invoice.set("")

        self.bill["state"] = "disabled"

    def new_bill(self) :
        self.new_win = Toplevel(self.root)
        self.new_obj = NewBill(self.new_win)


if __name__ == "__main__" :
    root = Tk()
    ob1 = Bills(root)
    root.mainloop()