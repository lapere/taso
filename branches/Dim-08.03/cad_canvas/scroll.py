from Tkinter import *
from math import *

class ScrolledCanvas(Canvas):
    def __init__(self, parent=None, **kw):
        Canvas.__init__(self, **kw)
   
        self.config(scrollregion=(0,0,800, 600))         

        self._scale = 1.0
        self.org_cursor = None
        
        ybar = Scrollbar(self, orient=VERTICAL)
        xbar = Scrollbar(self, orient=HORIZONTAL)
        ybar.config(command=self.yview)
        xbar.config(command=self.xview)                   
        self.config(yscrollcommand=ybar.set)
        self.config(xscrollcommand=xbar.set)              

        ybar.pack(side=RIGHT, fill=Y)
        xbar.pack(side=BOTTOM, fill=X)                     
        #self.canv.pack(expand=YES, fill=BOTH)
        
        self.bind('<Button-2>', self.mark)
        self.bind('<Button-4>', self.zoom_in)
        self.bind('<Button-5>', self.zoom_out)
        self.bind('<ButtonRelease-2>', self.leave_pan)
        self.bind('<B2-Motion>', self.move)
        
    

    def mark(self, event):
        self.scan_mark(event.x, event.y)
        self.org_cursor = self["cursor"]
        self["cursor"] = "fleur"

    def leave_pan(self, event):
        self["cursor"] = self.org_cursor

    def zoom_in(self, event):
        if self._scale < 10000:
            self._scale *= 1.1
            self._repaint(event, 1.1)
        
            
    def zoom_out(self, event):
        if self._scale > 0.01:
            self._scale *= 0.96
            self._repaint(event, 0.96)
        
        
    def move(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

    def _repaint(self, event, scale):
        
        x = int(self.canvasx(event.x))
        y = int(self.canvasy(event.y))
        
        w = int(800 * self._scale)
        h = int(600 * self._scale)

    
        #self.scale("all", 0, 0, scale, scale)
        self.config(width=w, height=h)
        self.config(scrollregion=(0,0,w,h))
        #print event.x, x, scale, self._scale
        self.scan_mark(int(x * scale), int(y * scale))
        self.scan_dragto(x, y, gain=1)
        self.repaint()    

if __name__ == '__main__':
    class Koe(ScrolledCanvas):
        def __init__(self, master, **kw):
            ScrolledCanvas.__init__(self, **kw)

    root = Tk()
    c = Koe(root, bg="blue")
    c.pack(expand=YES, fill=BOTH)
    
    for i in range(10):
            c.create_line(0, 0, 100, 50+i*10, tags="all")

    c.create_line(750, 550, 700, 590, tags="all")
    for ray in range(600):
        c.create_line(400, 300,
                           sin(float(ray)/1000) + 400,
                           cos(float(ray)/1000) + 200, tags="all")

    c.mainloop()

