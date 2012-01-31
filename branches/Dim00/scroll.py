from Tkinter import *
from math import *
from plauta import *

class ScrolledCanvas(Frame):
    
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.canv = PLauta(self, closeenough=4.0, bg="white")
        self.canv.config(width=800, height=600)                
        self.canv.config(scrollregion=(0,0,800, 600))         

        self._scale = 1.0
        self.org_cursor = None
        
        ybar = Scrollbar(self.canv, orient=VERTICAL)
        xbar = Scrollbar(self.canv, orient=HORIZONTAL)
        ybar.config(command=self.canv.yview)
        xbar.config(command=self.canv.xview)                   
        self.canv.config(yscrollcommand=ybar.set)
        self.canv.config(xscrollcommand=xbar.set)              

        ybar.pack(side=RIGHT, fill=Y)
        xbar.pack(side=BOTTOM, fill=X)                     
        self.canv.pack(expand=YES, fill=BOTH)
        
        self.canv.bind('<Button-2>', self.mark)
        self.canv.bind('<Button-4>', self.zoom_in)
        self.canv.bind('<Button-5>', self.zoom_out)
        self.canv.bind('<ButtonRelease-2>', self.leave_pan)
        self.canv.bind('<B2-Motion>', self.move)
        
    

    def mark(self, event):
        self.canv.scan_mark(event.x, event.y)
        self.org_cursor = self.canv["cursor"]
        self.canv["cursor"] = "fleur"

    def leave_pan(self, event):
        self.canv["cursor"] = self.org_cursor

    def zoom_in(self, event):
        if self._scale < 10:
            self._scale *= 1.1
            self.repaint(event, 1.1)
        
            
    def zoom_out(self, event):
        if self._scale > 0.1:
            self._scale *= 0.96
            self.repaint(event, 0.96)
        
        
    def move(self, event):
        self.canv.scan_dragto(event.x, event.y, gain=1)

    def repaint(self, event, scale):
        
        x = int(self.canv.canvasx(event.x))
        y = int(self.canv.canvasy(event.y))
        
        w = int(800 * self._scale)
        h = int(600 * self._scale)

        self.canv.scale("all", 0, 0, scale, scale)
        self.canv.config(width=w, height=h)
        self.canv.config(scrollregion=(0,0,w,h))

        #print event.x, x, scale, self._scale
        self.canv.scan_mark(int(x * scale), int(y * scale))
        self.canv.scan_dragto(x, y, gain=1)
            
if __name__ == '__main__':
    c = ScrolledCanvas()
    c.pack(expand=YES, fill=BOTH)
    
    for i in range(10):
            c.canv.create_line(0, 0, 100, 50+i*10, tags="all")

    c.canv.create_line(750, 550, 700, 590, tags="all")
    for ray in range(600):
        c.canv.create_line(400, 300,
                           sin(float(ray)/1000) + 400,
                           cos(float(ray)/1000) + 200, tags="all")

    c.mainloop()

