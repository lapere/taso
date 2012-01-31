#!/usr/bin/python
from Tkinter import *
from math import *
from plauta import *


class ScrolledCanvas(Canvas):
    
    def __init__(self, parent=None):
        Canvas.__init__(self, parent, bg="#9a9")
        self.canv = PLauta(self, closeenough=4.0, bg="white")
        self.canv.config(width=800, height=600)                
        self.config(scrollregion=(-800, -600, 800*2, 600*2))

        self.canv.create_line(1, 1, 800, 1)
        self.canv.create_line(1, 1, 1, 600)
        self.canv.create_line(800, 600, 800, 0)
        self.canv.create_line(800, 600, 0, 600)
        self.rec = self.canv.create_rectangle(0,0,800, 600,fill="")

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

        tag = self.create_window(0, 0, anchor=NW, window=self.canv)
        
        self.bind_all('<Button-2>', self.mark)
        self.canv.bind('<Button-4>', self.zoom_in)
        self.canv.bind('<Button-5>', self.zoom_out)
        self.bind_all('<ButtonRelease-2>', self.leave_pan)
        self.bind_all('<B2-Motion>', self.move)
        
    

    def mark(self, event):
        x = event.x_root
        y = event.y_root
        self.scan_mark(x, y)
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
        x = event.x_root
        y = event.y_root
        self.scan_dragto(x, y, gain=1)
            
    def repaint(self, event, scale):
        
        x = int(self.canvasx(event.x))
        y = int(self.canvasy(event.y))
        
        w = int(800 * self._scale)
        h = int(600 * self._scale)
       
        self.canv.scale("all", 0, 0, scale, scale)

        box = self.canv.bbox("all")
        
        w = box[2] + box[0]
        h = box[3] + box[1] 

        self.canv.config(width=w, height=h)
        self.config(scrollregion=(-w, -h, w*2, h*2))

        self.scan_mark(int(event.x * scale), int(event.y * scale))
        self.scan_dragto(event.x, event.y, gain=1)
        
        
if __name__ == '__main__':
    root = Tk()
    c = ScrolledCanvas(root)
    c.pack(expand=YES, fill=BOTH)
    
    for i in range(10):
            c.canv.create_line(0, 0, 100, 50+i*10, tags="all")

    Button(root, command=root.quit).pack()
    root.mainloop()
    root.destroy()

