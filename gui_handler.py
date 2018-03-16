from appJar import gui
import sql_handler as K
import sqlite3


def admin_window():
    main.showSubWindow("login")
    main.setFocus("Password")
def close_admin():
    main.hideSubWindow("admin_tools")

def handle_pass(name):
    if name == "Cancel":
        main.hideSubWindow(title="login")
    elif name == "Reset":
        main.clearEntry("Password")
        main.setFocus("Password")
    else:
        password = main.getEntry("Password")
        if password == 'ehp433':
            main.hideSubWindow("login")
            main.clearEntry("Password")
            main.showSubWindow(title="admin_tools")

        else:
            main.errorBox(title="Error!", message="Wrong password")
            main.clearEntry("Password")
            main.setFocus("Password")
            main.hideSubWindow("login")


def add_transaction():
    # get first scan - room
    room = main.getEntry("barcode_field")
    # todo:error handling
    main.clearEntry("barcode_field")
    main.setFocus("barcode_field")
    # get second scan - multiplier
    mp = main.getEntry("barcode_field")
    main.clearEntry("barcode_field")
    main.setFocus("barcode_field")
    # get third scan - product
    prod = main.getEntry("barcode_field")
    main.clearEntry("barcode_field")
    main.setFocus("barcode_field")
    tmp = room + mp + prod
    print(tmp)


def show_add_user_sw():
    main.showSubWindow("add_user_sw")

def show_add_prod_sw():
    main.showSubWindow("add_prod_sw")

def show_rem_prod_sw():
    main.showSubWindow("rem_prod_sw")

def rem_prod_button_press(name):
    if name == 'rem_prod_cancel':
        main.hideSubWindow("rem_prod_sw")
    elif name == 'rem_prod_submit':
        barcode = main.getEntry("rem_prod_barcode_entry")
        K.remove_product_from_db(barcode)
        main.infoBox("Product with barcode %s removed from DB." % barcode)
        main.hideSubWindow("rem_prod_sw")
        main.showSubWindow("admin_tools")

def add_user_button_press(name):
    if name == 'add_user_cancel':
        main.hideSubWindow(title="add_user_sw")
    elif name == 'add_user_submit':
        name = main.getEntry("add_user_username_entry")
        barcode = main.getEntry("add_user_barcode_entry")
        if not name or not barcode:
            main.errorBox("Error!", "Error: field empty!")
            main.hideSubWindow(title="add_user_sw")
            main.showSubWindow(title="admin_tools")
            return

        # call sql backend
        try:
            K.add_user_to_db(name, barcode)
            # TODO: Maybe do some error handling, try catch and throw exception in sql handler
            main.infoBox(title="Succesfully added user", message="Succesfully added user %s to DB!" % name)
            main.hideSubWindow("add_user_sw")
            main.showSubWindow("admin_tools")
        except sqlite3.IntegrityError:
            main.errorBox("Error!", "User not unique. Not added!")
            main.clearEntry("add_user_username_entry", setFocus=False)
            main.clearEntry("add_user_barcode_entry", setFocus=False)
            main.hideSubWindow("add_user_sw")
            main.showSubWindow("admin_tools")

def generate_bill_press():
    K.generate_bill()
    main.infoBox(title="Bill", message="Bill generated.")
    main.showSubWindow("admin_tools")

def add_prod_button_press(name):
    if name == 'add_prod_cancel':
        main.hideSubWindow("add_prod_sw")
    elif name == 'add_prod_submit':
        prod_name = main.getEntry("add_prod_name_entry")
        prod_barcode = main.getEntry("add_prod_barcode_entry")
        prod_price = main.getEntry("add_prod_price_entry")
        prod_cat = main.getOptionBox("Product Type")
        if not prod_name or not prod_barcode or not prod_price:
            main.errorBox("Error!", "Error: field empty!")
            main.hideSubWindow(title="add_prod_sw")
            main.showSubWindow(title="admin_tools")

        try:
            K.add_product_to_db(prod_name, prod_barcode, prod_price, prod_cat)
            main.infoBox("Sucessfully added product", message="Succesfully added product %s to DB!" % prod_name)
            main.hideSubWindow("add_prod_sw")
            main.showSubWindow("admin_tools")
        except sqlite3.IntegrityError:
            main.errorBox("Error!", "Product barcode not unique. Not added!")
            main.clearAllEntries()
            main.hideSubWindow("add_prod_sw")
            main.showSubWindow("admin_tools")

main = gui()
main.setTitle("Mellemste 4. Oelsystem!")
main.setIcon("maribo.gif")
# set fullscreen
main.setSize(1920, 1080)
main.setResizable(canResize=False)
main.setBg("LightCyan")
main.setLabelFont(size=20, family="Verdana")


# latest transactions table
main.addLabel("latest_transactions_label", text="Latest transactions", row=0, column=0, rowspan=10)
main.addListBox("latest_transactions_table", [] , 1, 0, colspan=5)



# input field
main.addEntry("barcode_field", column=10, row=main.getRow())

# todo: some hacky shit here. doesn't work because it reenters the function on each enter press

#main.enableEnter(add_transaction)

# scoreboard
# TODO: Consider adding graph instead...

# add admin button
main.setButtonFont(size=14, family="Times")
main.addButton("Admin", admin_window, column=10, row=main.getRow())








"""
Subwindows below here.
Behold, the AppJar shitshow has barely begun. Fear, mortals.
"""
## begin subwindow
main.startSubWindow(name="login", title="Login to Admin tools", modal=True)
main.setBg("LightCyan")
main.setFg("Black")
main.setSize(800, 600)
main.addLabel("Admin login")
main.addSecretLabelEntry("Password")
main.addButtons(names=["Reset", "Cancel", "Submit"], funcs=handle_pass)
main.setFocus("Password")
main.enableEnter(handle_pass)
main.stopSubWindow()
## end subwindow

## begin subwindow
main.startSubWindow(name="add_user_sw", title="Add user", modal=True)
main.setBg("LightCyan")
main.setFg("Black")
main.setSize(532, 400)
main.setFont(size=14, family="Verdana")
main.addLabel("Add user to DB")
main.addLabel("add_user_username", "Room:", 1,0)
main.addLabel("add_user_barcode", "Barcode:",2,0)
main.addEntry("add_user_username_entry", 1, 1)
main.addEntry("add_user_barcode_entry", 2,1)
main.setFocus("add_user_username_entry")
main.addNamedButton(title="add_user_cancel", name="Cancel", func=add_user_button_press, row=3, column=0)
main.addNamedButton(title="add_user_submit", name="Submit", func=add_user_button_press, row=3, column=1)
main.enableEnter(add_user_button_press)


main.stopSubWindow()
## end subwindow


## start subwindow
main.startSubWindow(name="add_prod_sw", title="Add product", modal=True)
main.setBg("LightCyan")
main.setFg("Black")
main.setSize(800, 600)
main.setFont(size=14, family="Verdana")
main.addLabel("Add product to DB")
main.addLabel("add_prod_name", "Product name:", 1,0)
main.addEntry("add_prod_name_entry", 1, 1)
main.addLabel("add_prod_barcode", "Barcode:",2,0)
main.addEntry("add_prod_barcode_entry", 2,1)
main.addLabel("add_prod_price", "Product price:", 3,0)
main.addEntry("add_prod_price_entry", 3,1)
main.addLabelOptionBox("Product Type", ["Beer", "Gold Beer", "Soda", "Other"],4,0)
main.setFocus("add_prod_name_entry")


main.addNamedButton(title="add_prod_cancel", name="Cancel", func=add_prod_button_press, row=5, column=0)
main.addNamedButton(title="add_prod_submit", name="Submit", func=add_prod_button_press, row=5, column=1)
main.enableEnter(add_prod_button_press)


main.stopSubWindow()
## end subwindow

## start subwindow
main.startSubWindow(name="rem_prod_sw", title="Remove product", modal=True)
main.setBg("LightCyan")
main.setFg("Black")
main.setSize(800, 600)
main.setFont(size=14, family="Verdana")
main.addLabel("Remove product from DB. Removal by name is not yet implemented", row=0, column=0, colspan=10)
main.addLabel(title="rem_prod_barcode", text="Barcode of product to remove:", row=1, column=0)
main.addEntry("rem_prod_barcode_entry", 1, 1)
main.setFocus("rem_prod_barcode_entry")

main.addNamedButton(title="rem_prod_cancel", name="Cancel", func=rem_prod_button_press, row=2, column=0)
main.addNamedButton(title="rem_prod_submit", name="Submit", func=rem_prod_button_press, row=2, column=1)
main.enableEnter(rem_prod_button_press)
main.stopSubWindow()


## end subwindow

## begin subwindow
main.startSubWindow(name="admin_tools", title="Admin tools", modal=False)
main.setBg("LightCyan")
main.setFg("Black")
main.setSize(800, 600)
main.addLabel("Welcome to admin tools!")
main.addButtons(["Leave Admin","Generate bill", "Add user", "Add product", "Delete Product"],
                funcs=[close_admin, generate_bill_press, show_add_user_sw, show_add_prod_sw, show_rem_prod_sw],
                row=1)

main.stopSubWindow()
## end subwindow


main.go()


