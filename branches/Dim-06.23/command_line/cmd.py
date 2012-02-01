from Tkinter import *
from code import *
import sys
import os

import code
import readline
import atexit
import os

class HistoryConsole(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>",
                 histfile=os.path.expanduser("~/console-history")):
        code.InteractiveConsole.__init__(self)
        self.init_history(histfile)
        interact()

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.write_history_file(histfile)
        

class CmdText(Text, InteractiveConsole):

    def __init__(self, root):
        Text.__init__(self, root, font=("Fixed", "14", "bold"), height=5, bg = "white")
        InteractiveConsole.__init__(self)
        
        sys.stdout = self
        sys.stdin = self
        #sys.stderr = self
        
        self.bind("<KeyRelease-Return>", self.enter)    
        
    def enter(self, event):
        line = self.get_current_line()
        self.runsource(line)
        
    def write(self, data):
        self.insert(END, data)

    def readline(self):
        return self.get_current_line()
    
    def destroy(self, event=None):
        self.quit()
        
    def get_current_line(self):
        line = int(self.index(INSERT).split(".")[0]) - 1
        line = str(line)
        return self.get(line+".0", line+".end")
  
if __name__ == '__main__':
    #h = HistoryConsole()
    
    root = Tk()
    txt = CmdText(root)
    txt.pack()
    root.mainloop()


