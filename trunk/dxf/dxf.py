#svn test
import sys
import group_code
from Tkinter import *
import tkFileDialog
from fun import *
strings = []
floats = []
ints = []

strings += range(0, 10)     #String (255 characters maximum; less for Unicode strings)
floats += range(10, 60)     #Double precision 3D point
ints += range(60, 80)       #16-bit integer value
ints += range(90,100)       #32-bit integer value
strings += [100]            #String (255 characters maximum; less for Unicode strings)
strings += [102]            #String (255 characters maximum; less for Unicode strings
strings += [105]            #String representing hexadecimal (hex) handle value
floats += range(140, 148)   #Double precision scalar floating-point value
ints += range(170, 176)     #16-bit integer value
ints += range(280, 290)     #8-bit integer value
strings += range(300, 310)  #Arbitrary text string
strings += range(310, 320)  #String representing hex value of binary chunk
strings += range(320, 330)  #String representing hex handle value
strings += range(330, 369)  #String representing hex object IDs
strings += [999]            #Comment (string)
strings += range(1000, 1010)#String (255 characters maximum; less for Unicode strings)
floats += range(1010, 1060) #Floating-point value
ints += range(1060, 1071)   #16-bit integer value
ints += [1071]              #32-bit integer value

def read_int(data):
    return int(data)

def read_float(data):
    return float(data)

def read_string(data):
    return str(data)

def read_none(data):
    return None


funs = []

for i in range(0,1072):
    funs.append(read_none)

for i in strings:
    funs[i] = read_string

for i in floats:
    funs[i] = read_float

for i in ints:
    funs[i] = read_int

def read_dxf_file(name, data):
        
    fd = file(name)
    Skip = True

    for line in fd:
        group_code = int(line)
        
        value = fd.next().replace('\r', '')
        value = value.replace('\n', '')
        value = value.lstrip(' ')
        value = value.rstrip(' ')
        value = funs[group_code](value)
        if (value != "SECTION") and Skip:
            continue
        else:
            Skip = False
        data.append((group_code, value))

    fd.close()




data = []
read_dxf_file(sys.argv[1], data)

data = iter(data)

g_code, value = None, None

sections = dict()

class Header:

    def __init__(self):
        self.variables = dict()
        self.last_var = None

    def new_var(self, kw):
        self.variables.update({kw: dict()})
        self.last_var = self.variables[kw]
        
    def new_val(self, val):
        self.last_var.update({ str(val[0]) : val[1] })

class Entity:
    
    def __init__(self, _type):
        self.type = _type
        self.data = dict()

    def update(self, value):

        key = str(value[0])
        val = value[1]

        if self.data.has_key(key):
            if type(self.data[key]) != list:
                self.data[key] = [self.data[key]]
            self.data[key].append(val)
        else:
            self.data.update({key:val})
        

class Entities:

    def __init__(self):
        self.entities = []
        self.last = None

    def new_entity(self, _type):
        e = Entity(_type)
        self.entities.append(e)
        self.last = e
    
    def update(self, value):
        self.last.update(value)


class Block:

    def __init__(self, master):
        self.master = master
        self.data = dict()
        self.entities = []
        self.le = None

    def new_entity(self, value):
        self.le = Entity(value)
        self.entities.append(self.le)

    def update(self, value):
        if self.le == None:
            val = str(value[0])
            self.data.update({val:value[1]})
            if val == "2":
                self.master.blocks[value[1]] = self
        else:
            self.le.update(value)


class Blocks:

    def __init__(self):
        self.blocks = dict()
        self.last_var = None

    def new_block(self):
        b = Block(self)
        #self.blocks.append(b)
        self.last_block = b
        self.last_var = b
        
    def new_entity(self, value):
        self.last_block.new_entity(value)

    def update(self, value):
        self.last_block.update(value)

while value != "EOF":

    g_code, value = data.next()

    if value == "SECTION":
        g_code, value = data.next()
        sections[value] = []

        while value != "ENDSEC":
            
            if value == "HEADER":
                he = Header()
                while True:
                    g_code, value = data.next()
                    if value == "ENDSEC":
                        break
                    elif g_code == 9:
                        he.new_var(value)
                    else:
                        he.new_val((g_code, value))

            elif value == "BLOCKS":
                bl = Blocks()
                while True:
                    g_code, value = data.next()
                    if value == "ENDSEC":
                        break
                    elif value == "ENDBLK":
                        continue
                    elif value == "BLOCK":
                        bl.new_block()
                    elif g_code == 0 and value != "BLOCK":
                        bl.new_entity(value)
                    else:
                        bl.update((g_code, value))

            elif value == "ENTITIES":
                en = Entities()
                while True:
                    g_code, value = data.next()
                    if value == "ENDSEC":
                        break
                    elif g_code == 0 and value != "ENDSEC":
                        en.new_entity(value)
                    else:
                        en.update((g_code, value))
                
                
                
            g_code, value = data.next()
            
        
        


#n he.variables["$EXTMAX"]

#print bl.blocks[-1].entities[-2].data


class canvas:
    pass

root = Tk()
root.title("DXF Viewer by lapere")

w, h = root.maxsize()
h -= 50
w -= 50

canvas.h = h
canvas.w = w

if he.variables.has_key("$EXTMAX"):
    x_max = he.variables["$EXTMAX"]["10"]
    y_max = he.variables["$EXTMAX"]["20"]
    x_min = he.variables["$EXTMIN"]["10"]
    y_min = he.variables["$EXTMIN"]["20"]

    x_scale = float(w) / (x_max - x_min)
    y_scale = float(h) / (y_max - y_min)

    canvas.scale = min(x_scale, y_scale)
else:
    canvas.scale = 1

canvas.scale = 1
root.geometry("%dx%d" % (h, w))

canvas.c = Canvas(root, bg="white")
canvas.c.pack(fill=BOTH, expand=1)

xcnt = 0
print "ENTITIES"
for e in en.entities:
    print e.type
    print "\tx=", e.data["10"]
    print "\thandle=", e.data["5"]
    xcnt += 1
print "BLOCKS"
canvas.blocks = bl.blocks
for b in canvas.blocks:
    print canvas.blocks[b].data["3"]
    for e in canvas.blocks[b].entities:
        print "\t", e.type
        print "\tx=", e.data["10"]
        print "\thandle=", e.data["5"]
        if e.type == "INSERT":
            b_name = e.data["2"]
            print "\t\t", b_name
            block = canvas.blocks[b_name]
            for e2 in block.entities:
                print "\t\t\t", e2.type
                print "\t\t\tx=", e.data["10"]
                print "\t\t\thandle=", e.data["5"]
                xcnt += 1
        else:
            xcnt += 1
            
print "total=", xcnt


cnt = 0


    


#print "MIN=", he.variables["$EXTMIN"]

for e in en.entities:
    f = funit[e.type]
    f(canvas, e)
"""
for e in  bl.blocks['HP26012'].entities:
    print e.type
    for kw in e.data:
        print "\t", kw, e.data[kw]
"""

#for kw in funit:
#    print kw,funit[kw].cnt


def resize_canvas(event):
    pass
    #canvas.h = canvas.c.winfo_height()
    #canvas.w = canvas.c.winfo_width()

canvas.font_scale = 1.0
all = canvas.c.find_all()

def _mouseZoomIn(event):

    all = canvas.c.find_all()
    canvas.font_scale *= 1.1
    for i in all:
        canvas.c.scale(i, event.x, event.y, 1.1, 1.1)
        if canvas.c.type(i) == "text":
            h = int(canvas.c.gettags(i)[0])
            h *= canvas.font_scale
            if h > 1:
                canvas.c.itemconfigure(i, fill = "black", font = ("Helvetica", str(int(h))))
            else:
                canvas.c.itemconfigure(i, fill = "")
    canvas.c.update_idletasks()

    
def _mouseZoomOut(event):
    
    canvas.font_scale *= 0.9
    for i in all:
        canvas.c.scale(i, event.x, event.y, 0.9, 0.9)
        if canvas.c.type(i) == "text":
            h = int(canvas.c.gettags(i)[0])   
            h *= canvas.font_scale
            if h > 1:
                canvas.c.itemconfigure(i, fill = "black", font = ("Helvetica", str(int(h))))
            else:
                canvas.c.itemconfigure(i, fill = "")
    canvas.c.update_idletasks()

class self:
    panx = 0
    panx = 0
    lastx = 0
    lasty = 0
    
def mousePanStart(event):
        self.panx = event.x
        self.pany = event.y


def mousePan(event):
        dx = event.x-self.panx
        dy = event.y-self.pany
        for i in all:
            canvas.c.move(i, dx, dy)

        self.lastx = self.lastx + dx
        self.lasty = self.lasty + dy
        self.panx = event.x
        self.pany = event.y
  
def plot(event):
        fn = tkFileDialog.asksaveasfilename(filetypes=[('Postscript files', '*.ps')])
        canvas.c.focus_set()
        canvas.c.update_idletasks()
        canvas.c.postscript(colormode="gray", file=fn,
                            rotate = True,
                            height = y_max * canvas.scale,
                            width = x_max * canvas.scale,
                            y = -y_max * canvas.scale + canvas.h)


canvas.c.bind("<Button-3>", plot)
canvas.c.bind("<Button-4>", _mouseZoomIn)
canvas.c.bind("<Button-5>", _mouseZoomOut)
canvas.c.bind("<Configure>", resize_canvas)
canvas.c.bind("<2>", mousePanStart)
canvas.c.bind("<B2-Motion>", mousePan)

root.mainloop()

