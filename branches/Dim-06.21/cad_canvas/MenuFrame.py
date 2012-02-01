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
            self.addCommand("File", "None", self.no)
           
    def addCommand(self, menu_name, command_name, command=None):
    
        if not self.mb.has_key(menu_name):
            self.mb[menu_name] = MenuButton(self, text=menu_name, underline=0)
            self.mb[menu_name].pack(side=LEFT)

        if command_name == 'separator':
            self.mb[menu_name].menus.add(command_name)
        else:
            self.mb[menu_name].menus.add_command(label=command_name, underline=0, command=command)

    def no(self):
        pass
    
if __name__ == '__main__':
    root = Tk()
    frame = MenuFrame(root)
    frame.pack(fill=X)

    def hi():
        print "hi!"

    for s in "slkdjfsjdfjklsdkfjklsdjfjskdfjsdlkfjjsdklfksdjlkjlkjkl":
        frame.addCommand("Fie", s, hi)
    frame.addCommand("File", "hou!", hi)
    frame.addCommand("File", 'separator')
    frame.addCommand("File", "sdfkj", hi)
    root.mainloop()
