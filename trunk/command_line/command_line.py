from Tkinter import *
from code import *
import sys
import os

class CmdText(Text, InteractiveInterpreter):

    def __init__(self, root):
        from cad_canvas import cad_canvas
        Text.__init__(self, root, font=("Fixed", "14", "bold"), height=5, bg = "white")
        InteractiveInterpreter.__init__(self)
        self.canvas = cad_canvas(root, bg="white", width=800, height=600,
                                 closeenough=5.0)
        self.canvas.items.ic = self
        self.canvas.ic = self
        #self.ret = self.runsource("import tol")
        self.ret = self.runsource("from tools import *")
        self.locals["canvas"] = self.canvas
        #self.ret = self.runsource("tol.canvas = canvas")
        self.cmd = ""
        sys.stdout = self
        #print dir(sys.stdout)
        #sys.stdout.write = self.write 
        #sys.stderr = os.tmpfile()
        self.keywords = ["and", "del", "for", "is", "raise",    
                         "assert", "elif", "from", "lambda", "return",
                         "break", "else", "global", "not", "try",
                         "class", "except", "if", "or", "while",
                         "continue", "exec", "import", "pass", "yield",
                         "def", "finally", "in", "print"]


        self.bind("<KeyRelease-Return>", self.entre)
        self.bind("<KeyRelease>", self.key_press)

    def entre(self, event=None):
        self.cmd = self.cmd + self.get_last_line()[0]
        self.ret = self.runsource(self.cmd)
         
        if not self.ret:
            self.cmd = ""
        else:
            pass
            #self['height'] = int(self['height']) + 1

    def key_press(self, event):
        line = self.get_current_line()
        self.tag_remove("kw", line[1] + ".0", line[1] + ".end")
        
        def find_hit(line):
            for kw in self.keywords:
                hit = line[0].find(kw)
                if hit != -1:
                    i_1 = line[1] + "." + str(hit)
                    i_2 = line[1] + "." + str(hit + len(kw))
                    self.tag_add("kw", i_1, i_2)
                    self.tag_config("kw", foreground="orange")

        find_hit(line)
        
    def get_last_line(self):
        line = int(self.index(INSERT).split(".")[0]) - 1
        line = str(line)
        return self.get(line+".0", line+".end") + "\n", line

    def get_current_line(self):
        line = int(self.index(INSERT).split(".")[0])
        line = str(line)
        return self.get(line+".0", line+".end") + "\n", line

    def write(self, data):
        self.insert(INSERT, data)

    def destroy(self, event=None):
        self.quit()

if __name__ == '__main__':
    root = Tk()
    txt = CmdText(root)
    txt.pack()
    root.mainloop()


