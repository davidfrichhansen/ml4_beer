from appJar import gui, appjar
import sql_handler as K


def admin_window():
    main.showSubWindow("login")

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
            main.hideSubWindow("login")


main = gui()
main.setTitle("Mellemste 4. Ølsystem!")
# set fullscreen
root = appjar.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()
main.setSize(width, height)
main.setResizable(canResize=False)
main.setBg("LightCyan")
main.setLabelFont(size=20, family="Verdana")


# add admin button
main.addButton("Admin", admin_window)
main.setButtonFont(size=14, family="Comic Sans")

## begin subwindow
main.startSubWindow(name="login", title="Login to Admin tools", modal=True)
main.setBg("LightCyan")
main.setFg("Black")
main.setSize(800, 600)
main.addLabel("Admin login")
main.addSecretLabelEntry("Password")
main.addButtons(names=["Reset", "Cancel", "Submit"], funcs=handle_pass)
main.stopSubWindow()
## end subwindow

## begin subwindow
main.startSubWindow(name="admin_tools", title="Admin tools")
main.setBg("LightCyan")
main.setFg("Black")
main.setSize(800, 600)
main.addLabel("Welcome to admin tools!")
#main.addButtons(["Create DB", "Add product","Remove product"], funcs=[])
#main.addButtons(["Generate bill", "Add user"])

main.stopSubWindow()
## end subwindow

main.go()


