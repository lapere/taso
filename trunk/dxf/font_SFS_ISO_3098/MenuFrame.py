from Tkinter import *

class MenuButton(Menubutton):
    def __init__(self, master = None,**kw):

            Menubutton.__init__(self, master, kw)
            self.menus = Menu(self)
            self["menu"] = self.menus
            
class MenuFrame(Frame):

    def __init__(self, master):                        
            Frame.__init__(self, master)
            self.mb = dict()
            c = 0;
           
    def addCommand(self, menu_name, command, command_name):
        if not self.mb.has_key(menu_name):
            self.mb[menu_name] = MenuButton(self, text=menu_name, underline=0)
            self.mb[menu_name].pack(side=LEFT)

        self.mb[menu_name].menus.add_command(label=command_name, underline=0, command=command)

if __name__ == '__main__':
    root = Tk()
    frame = MenuFrame(root)
    frame.pack(fill=X)
    def hi():
        print "hi!"
    frame.addCommand("Fie", hi, "hi!")
    frame.addCommand("File", hi, "hou!")
    root.mainloop()
