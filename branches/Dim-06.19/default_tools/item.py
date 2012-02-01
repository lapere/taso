from cad_kernel.db import Item
import vp

class VisualItem(Item):

    def __init__(self, canvas, base_tag, formula):
        Item.__init__(self, canvas.items, base_tag, str(formula))
        self.visuals = []

    def new_visual(self, visual):
        visual.value = self
        visual.addtag(self.tag)

        visual.entry_set = self.entry_set
        visual.entry_get = self.entry_get
        visual.e_copy = self.e_copy
        
        self.visuals.append(visual)    

    def e_copy(self):
        self.canvas.cmd.set(self.canvas.cmd.get() + self.tag)

    def entry_set(self):
        self.canvas.cmd.set(self.formula)

    def entry_get(self):
        self.new_formula(self.canvas.cmd.get())

    def repaint(self):
        for i in self.visuals:
            i.repaint()
        
class Xelement(VisualItem):

    def __init__(self, canvas, formula):
        VisualItem.__init__(self, canvas, "X", str(formula))
        self.canvas = canvas

    def A(self):
        return 1.0

    def B(self):
        return 0.0

    def C(self):
	x = float(self)
        return float(-self.A() * x - self.B())

class Yelement(VisualItem):

    def __init__(self, canvas, formula):
        Item.__init__(self, canvas.items, "Y", str(formula))
        self.canvas = canvas
            
    def A(self):
        return 0.0

    def B(self):
        return 1.0

    def C(self):
	y = float(self)
        return float(-self.A() - self.B() * y)            


class Zelement(VisualItem):

    def __init__(self, canvas, formula):
        Item.__init__(self, canvas.items, "Z", str(formula))
        self.canvas = canvas

    def A(self):
        return 0.0

    def B(self):
        return 1.0

    def C(self):
	y = float(self)
        return float(-self.A() - self.B() * y)           

class Aelement(VisualItem):
    
    def A(self):
        y0 = float(self.point.y)     #self.canvas.coords(self.id)[1]
        y1 = y0 - sin(float(self))  #self.canvas.coords(self.id)[3]
        return float(-(y0 - y1))

    def B(self):
        x0 = float(self.point.x)	#self.canvas.coords(self.id)[0]
        x1 = cos(float(self)) + x0	#self.canvas.coords(self.id)[2]
        return float((x0 - x1))

    def C(self):
        x = float(self.point.x)	#self.canvas.coords(self.id)[0]
        y = float(self.point.y)	#self.canvas.coords(self.id)[1]
        return float(-self.A() * x - self.B() * y)

class Point(VisualItem):
    
    def __init__(self, canvas, base_tag, x, y, z):
        VisualItem.__init__(self, canvas.items, base_tag, None)
        self.canvas = canvas
        self.x = x
        self.y = y
        self.z = z
        x.fellows.update({self.tag:self})
        y.fellows.update({self.tag:self})
        z.fellows.update({self.tag:self})
