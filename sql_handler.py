import sqlite3
import datetime
from pathlib import Path
from os import remove
import pandas as pd
import csv
import random

def create_db():
    ### Creates DB from scratch! Will overwrite everything, so be careful
    ### If 'extra users' (ie. sublets, X-beboere etc.) have been added, these should be added manually again, after this function has been called.
    ### Use the appropriate function for this.

    # TODO: Implement category in products

    if Path('beer_db.db').is_file():
        print('DB File already exists. Deleting old one and creating new.\nIf this was not intended, you are fucked.')
        remove('beer_db.db')
    else:
        print("DB File not found. Creating new one.")


    # connect to db
    conn = sqlite3.connect('beer_db.db')


    """
    Query
    CREATE TABLE Users (
    Room VARCHAR(10) PRIMARY KEY,
    Barcode VARCHAR(64) UNIQUE
    )
    """
    
    # Create user table
    conn.execute("CREATE TABLE Users ( Room VARCHAR(10) PRIMARY KEY, Barcode VARCHAR(64) UNIQUE)")

    # insert users into table
    
    rooms = list(range(425, 437)) + list(range(439, 447))
    for i in rooms:
        conn.execute("INSERT INTO Users (Room, Barcode) VALUES (?,?)", (i, i))


    conn.commit()

    # TODO: Format nicely in comment
    sql = "CREATE TABLE Transactions (Room VARCHAR(10), ProductName VARCHAR(100) , Multiplier INT(100), Bought_at VARCHAR(30), FOREIGN KEY(Room) REFERENCES Users(Room))"
    conn.execute(sql)
    conn.commit()


    conn.execute("CREATE TABLE Products (Barcode VARCHAR(64) PRIMARY KEY, Name VARCHAR(100), Price INT(1000), Category VARCHAR(100))")



    # close connection to ensure all is flushed
    conn.close()

def transaction(user_barcode, product_barcode, multiplier):
    # adds a transaction to the db

    # Maageordning: On average, every 'chance' purchases should give a ordning

    # connect to db
    conn = sqlite3.connect('beer_db.db')
    chance = 50
    if random.randrange(51) == 1:
        print('MAAGEORDNING!!!!')
        # TODO: Find a way to play sound.
    
    # get timestamp - requires that system knows what time it is. unsure of offline stability.
    # may also change based on system, but Debian based Linux should be ok.
    curr_time = datetime.datetime.now().isoformat(' ')
    # Get room in case the barcode isn't just the room number
    sql_room = "SELECT Room FROM Users WHERE Barcode=?"
    curr_room = list(conn.execute(sql_room, (user_barcode, )))
    if len(curr_room) == 0:
        print('User not found. Transaction ignored.')
        return
    curr_room = curr_room[0][0]
    
    sql_prodname = "SELECT Name FROM Products WHERE Barcode=?"
    
   
    curr_prod = list(conn.execute(sql_prodname, (product_barcode, )))
    if len(curr_prod) == 0: 
        print('Product not found. Transaction ignored!')
        return
    curr_prod = curr_prod[0][0]
    # insert in db
    sql = 'INSERT INTO Transactions (Room, ProductName, Multiplier, Bought_at) VALUES (?,?,?,?)'
    conn.execute(sql, (curr_room, curr_prod, multiplier, curr_time))
    conn.commit()
    conn.close()


def add_product_to_db(product_name, barcode, price, category):
    # Adds a product to the DB
    conn = sqlite3.connect('beer_db.db')

    sql = "INSERT INTO Products (Barcode, Name, Price, Category) VALUES (?, ?, ?, ?)"

    conn.execute(sql, (barcode, product_name, price, category))
    conn.commit()

    conn.close()

def change_product(**kwargs):
    # Check if product exists
    # Change in DB
    pass


def remove_product_from_db(barcode):
    # Removes product from DB - probably not used very much
    # TODO: Implement removal by name
    conn = sqlite3.connect('beer_db.db')

    sql = "DELETE FROM Products WHERE Barcode=?"

    conn.execute(sql, (barcode, ))
    conn.commit()
    conn.close()


def generate_bill():
    # Generates bill and resets transaction table.
    # Note that this will overwrite old bill if done twice per day.
    
    today = datetime.date.today()

    conn = sqlite3.connect('beer_db.db')
    # get rooms
    rooms = [x[0] for x in conn.execute("SELECT Room FROM Users").fetchall()]

    # get transactions - this is a generator
    transactions = conn.execute("SELECT * FROM Transactions")
    
    
    # This is **extremely** convenient, but requires that the entire table fits in memory. Shouldn't normally
    # be an issue... i hope
    df = pd.read_sql_query("SELECT * FROM Transactions", conn)

    # save table to csv to have it for future reference
    df.to_csv('transactions_%s.csv' % str(today))
    del df

    bills = {x : 0 for x in rooms}
    for t in transactions:
        curr_room = t[0]
        curr_prod = t[1]
        curr_mp = t[2]

        # get price of current product
        curr_price = conn.execute("SELECT Price FROM Products WHERE Name=(?)", (curr_prod,)).fetchone()
        if len(curr_price) != 1:
            print("Something went wrong. Perhaps product doesn't exist or something.....")
            return
        price = curr_price[0]

        # add to bill
        bills[curr_room] += price*curr_mp

    # write bill to csv
    with open('bill_%s.csv' % str(today), 'w') as csv_file:
        writer = csv.writer(csv_file)
        for k,v in bills.items():
            writer.writerow([k,v])


    # remove records
    print("Removing existing records from transactions.")
    conn.execute("DELETE FROM Transactions")
    conn.commit()
    print("Done.")

    conn.close()

def add_user_to_db(name, barcode):
    # add a user to the DB
    conn = sqlite3.connect('beer_db.db')
    sql = "INSERT INTO Users (Room, Barcode) VALUES (?,?)"

    conn.execute(sql, (name, barcode))
    conn.commit()
    conn.close()


#create_db()
"""
add_product_to_db('Testprd', 123, 5, 'Beer')
remove_product_from_db(123)
add_product_to_db('Testprd', 123, 5.3, 'Beer'   )
transaction(433, 123, 10)
transaction(432, 123, 4)
add_user_to_db('X10', 'X10')
generate_bill()
"""