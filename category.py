from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class Category :
    def __init__(self, root) :
        self.root = root
        self.root.geometry("1120x530+210+130")
        self.root.config(bg = "gold")
        self.root.resizable(0, 0)
        self.root.title("Categories")
        self.root.focus_force()

        #==============Variables===============#

        self.var_cat_id = StringVar()
        self.var_cat_name = StringVar()

        self.con = sqlite3.connect(database = r"sms.db")
        self.cur = self.con.cursor()


#==================================Shortcut Keys=========================================================

        self.root.bind("<Control-s>",   self.add)
        self.root.bind("<Control-d>",  self.delete)

#========================================================================================================

        #===============title===============#

        lbl_title = Label(
                          self.root,
                          text = "Manage Product Categories",
                          font = ("goundy old style", 30),
                          bg = "#184a45",
                          fg = "white",
                          bd = 3,
                          relief = RIDGE
                          ).pack(side = TOP, fill = X, padx = 10, pady = 20)
        
        lbl_cname = Label(
                          self.root,
                          text = "Enter Category Name",
                          bg = "gold",
                          font = ("goundy old style", 15, "bold"),
                          ).place(x = 50, y = 150)

        lbl_cid = Label(
                          self.root,
                          bg = "gold",
                          text = "Enter Category ID",
                          font = ("goundy old style", 15, "bold"),
                          ).place(x = 50, y = 100)
        
        lbl_cname_txt = Entry(
                          self.root,
                          textvariable = self.var_cat_name,
                          font = ("goundy old style", 10),
                          bg = "lightyellow",
                          bd = 2,
                          relief = RIDGE
                          )
        lbl_cname_txt.bind("<Return>", lambda ev : self.search(ev))
        lbl_cname_txt.place(x = 300, y = 150, width = 150, height = 30)

        lbl_cid_txt = Entry(
                          self.root,
                          textvariable = self.var_cat_id,
                          font = ("goundy old style", 10),
                          bg = "lightyellow",
                          bd = 2,
                          relief = RIDGE
                          )
        lbl_cid_txt.bind("<Return>", lambda ev : self.search(ev))
        lbl_cid_txt.place(x = 300, y = 100, width = 150, height = 30)
        
        add_btn = Button(
                          self.root,
                          font = ("goundy old style", 12, "bold"),
                          bg = "green",
                          text = "Add",
                          command = lambda : self.add(ev = 1),
                          fg = "white",
                          bd = 2,
                          cursor = "hand2",
                          relief = RIDGE
                          ).place(x = 340, y = 200, width = 100, height = 30)
        
        delete_btn = Button(
                          self.root,
                          font = ("goundy old style", 12, "bold"),
                          bg = "red",
                          text = "Delete",
                          fg = "white",
                          command = lambda : self.delete(ev = 1),
                          bd = 2,
                          cursor = "hand2",
                          relief = RIDGE
                          ).place(x = 460, y = 200, width = 100, height = 30)
        
        search_btn = Button(
                          self.root,
                          font = ("goundy old style", 12, "bold"),
                          bg = "blue",
                          text = "Search",
                          fg = "white",
                          command = lambda : self.search(ev = 1),
                          bd = 2,
                          cursor = "hand2",
                          relief = RIDGE
                          ).place(x = 220, y = 200, width = 100, height = 30)
        

        Category_Frame = Frame(self.root,
                               bg = "white",
                               bd = 3,
                               relief = RIDGE
                               )
        Category_Frame.place(x = 0, y = 330, relwidth = 1, height = 200)
        
        scrolly = Scrollbar(Category_Frame,
                           orient = VERTICAL
                           )
        
        scrollx = Scrollbar(Category_Frame,
                           orient = HORIZONTAL
                           )

        self.Category_table = ttk.Treeview(
                                     Category_Frame,
                                     columns = ("cat_id", "name"),                             
                                     yscrollcommand = scrolly.set,
                                     xscrollcommand = scrollx.set 
                                      )
        scrollx.pack(side = BOTTOM, fill = X)
        scrolly.pack(side = RIGHT, fill = Y)

        scrollx.config(command = self.Category_table.xview)
        scrolly.config(command = self.Category_table.yview)

        self.Category_table.heading("cat_id", text = "Cat ID")
        self.Category_table.heading("name", text = "Name")

        self.Category_table["show"] = "headings"

        self.Category_table.column("cat_id",width = 10, anchor = CENTER)
        self.Category_table.column("name",width = 10, anchor = CENTER)

        self.Category_table.bind("<ButtonRelease-1>", self.get_data)

        self.Category_table.pack(fill = BOTH, expand = 1)

        self.img = Image.open("images/cat.jpg")
        self.img = self.img.resize((500, 200), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)

        self.img_lbl = Label(self.root,
                        image = self.img,
                        relief = RAISED
                        ).place(x = 600, y = 100)

        self.show()

#==================================================================================================================================

    def add(self, ev):
        try:
            if self.var_cat_name.get() == "" or self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Please Enter Category Details!", parent = self.root)
            
            else:         
                self.cur.execute("SELECT * FROM category where cat_id = ?", (self.var_cat_id.get(),))
                row = self.cur.fetchone()

                if row != None:
                    messagebox.showerror("Error", "Category already exists!", parent = self.root)

                else:
                    self.cur.execute("INSERT INTO category (cat_id, name) values(?, ?)", (self.var_cat_id.get(), self.var_cat_name.get().capitalize(),))
                    self.con.commit()

                    messagebox.showinfo("Success", "Category Successfully Added!", parent = self.root)

                    self.show()
                    self.var_cat_id.set(int(self.var_cat_id.get()) + 1)
                    self.var_cat_name.set("")
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error Due to {str(ex)}", parent = self.root)

    
    def show(self):
        try:
            self.cur.execute("SELECT * FROM category")
            rows = self.cur.fetchall()

            self.Category_table.delete(*self.Category_table.get_children())

            for row in rows:
                self.Category_table.insert("", END, values = row)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def get_data(self, ev):
        data = self.Category_table.focus()
        content = (self.Category_table.item(data))
        row = content["values"]

        self.var_cat_id.set(row[0]),
        self.var_cat_name.set(row[1])

    def delete(self, ev):
        
        if self.var_cat_id.get() == "":
            messagebox.showerror("Error", "Please Enter Category ID!", parent = self.root)

        else:
            try :
                self.cur.execute("SELECT * FROM category where cat_id = ?", (self.var_cat_id.get(),))
                row = self.cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Category", parent = self.root)

                else:
                    yesno = messagebox.askyesno("Confirmation", "Are you sure want to delete ?", parent = self.root)

                    if yesno == True:
                        self.cur.execute("DELETE from category where cat_id = ?", (self.var_cat_id.get(),))
                        self.con.commit()

                        messagebox.showinfo("Success", "Successfully Deleted !", parent = self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_cat_name.set("")
            
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)

    def search(self, ev):

        if self.var_cat_id.get() == "" and self.var_cat_name.get() == "":
            messagebox.showerror("Error", "Please Enter Cat id or Name", parent = self.root)

        else:
            try : 
                if self.var_cat_name.get() == "":    
                    self.cur.execute(f"SELECT * FROM category where cat_id LIKE '%{self.var_cat_id.get()}%'")
                    rows = self.cur.fetchall()

                    if len(rows) != 0:
                        self.Category_table.delete(*self.Category_table.get_children())

                        for row in rows:
                            self.Category_table.insert("", END, values = row)

                        self.var_cat_id.set("")
                        self.var_cat_name.set("")

                    else:
                        messagebox.showerror("Error", "No Record Found!", parent = self.root)

                elif self.var_cat_id.get() == "":
                       
                    self.cur.execute(f"SELECT * FROM category where name LIKE '%{str(self.var_cat_name.get().capitalize())}%'")
                    rows = self.cur.fetchall()

                    if len(rows) != 0:
                        self.Category_table.delete(*self.Category_table.get_children())

                        for row in rows:
                            self.Category_table.insert("", END, values = row)

                        self.var_cat_id.set("")
                        self.var_cat_name.set("")

                    else:
                        messagebox.showerror("Error", "No Record Found!", parent = self.root)


            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent = self.root)
    

if __name__ == "__main__" :
    root = Tk()
    ob1 = Category(root)
    root.mainloop()