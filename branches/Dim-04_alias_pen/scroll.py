#!/usr/bin/python
from Tkinter import *
from math import *
from plauta import *
from tools import *

class ScrolledCanvas(Canvas):
    
    def __init__(self, parent=None):
        Canvas.__init__(self, parent,width=800, height=600, bg="#9a9")
        self.canv = PLauta(self, closeenough=4.0, bg="white")
        self.canv.config(width=800, height=600)                
        self.canv.config(scrollregion=(0,0,800, 600))

        self._scale = 1.0
        self.org_cursor = None
        
        ybar = Scrollbar(self, orient=VERTICAL)
        xbar = Scrollbar(self, orient=HORIZONTAL)
        ybar.config(command=self.canv.yview)
        xbar.config(command=self.canv.xview)                   
        self.canv.config(yscrollcommand=ybar.set)
        self.canv.config(xscrollcommand=xbar.set)              

        ybar.pack(side=RIGHT, fill=Y)
        xbar.pack(side=BOTTOM, fill=X)                     
        self.canv.pack(side=BOTTOM)#expand=YES, fill=BOTH)
        
        self.canv.bind('<Button-2>', self.mark)
        self.canv.bind('<Button-4>', self.zoom_in)
        self.canv.bind('<Button-5>', self.zoom_out)
        self.canv.bind('<ButtonRelease-2>', self.leave_pan)
        self.canv.bind('<B2-Motion>', self.move)
        
    

    def mark(self, event):
        
        print "\nevent.x", event.x
        """
        print "event.x_root", event.x_root
        print "event.width", event.width
        print "req", self.canv.winfo_reqwidth()
        print "pointerx",self.canv.winfo_pointerx()
        print "rootx", self.canv.winfo_rootx()
        print "screen", self.canv.winfo_screenwidth()
        print "vroot", self.canv.winfo_vrootwidth()
        print "vrootx", self.canv.winfo_vrootx()
        
        print "bbox", self.canv.bbox("all")
        print "canvasx", self.canv.canvasx(event.x)
        print self.canv['width']
        """
        self.canv.scan_mark(event.x, event.y)
        self.org_cursor = self.canv["cursor"]
        self.canv["cursor"] = "fleur"

    def leave_pan(self, event):
        self.canv["cursor"] = self.org_cursor
        for p in self.canv.pens.pen:
            p.repaint()
            
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
        for p in self.canv.pens.pen:
            p.repaint()
            
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

        for p in self.canv.pens.pen:
            p.repaint()    

if __name__ == '__main__':
    root = Tk()
    c = ScrolledCanvas(root)
    c.pack(expand=YES, fill=BOTH)
    
    for i in range(10):
            c.canv.create_line(0, 0, 100, 50+i*10, tags="all")

    c.canv.create_line(500, 10, 500, 490, tags="all")
    root.mainloop()

