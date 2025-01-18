import sqlite3

def create_db():
    con = sqlite3.connect(database = r"sms.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS customers(cid INTEGER PRIMARY KEY AUTOINCREMENT, name text, gender text, contact text, address text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(cat_id INTEGER PRIMARY KEY AUTOINCREMENT, name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS products(pid INTEGER PRIMARY KEY AUTOINCREMENT,  category text, name text, price text, quantity text, status text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS totalcustomers(name text, Paid_Bills text, Unpaid_Bills text, Balance text)")
    con.commit()

create_db()