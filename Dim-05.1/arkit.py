
class Arkki:
    def __init__(self, canvas, size, orient="portrait"):
        self.size = size
        self.sizes = dict(A0 = (841, 1189),
                          A1 = (1189 / 2, 841),
                          A2 = (841 / 2, 1189 / 2),
                          A3 = (1189 / 4, 841 / 2),
                          A4 = (210, 297))
        self.orientation = orient
        if orient == "landscape":
            self.landscape()

        x,y = self.size_mm()
        canvas.config(width=x, height=y)

    def size_pix(self):
        return self.sizes[self.size]

    def size_mm(self):
        x,y = self.sizes[self.size]
        return str(x) + "m", str(y) + "m"
    
    def landscape(self):
        for a in self.sizes:
            x,y =  self.sizes[a]
            self.sizes[a] = ((max(y,x),min(y,x)))
        self.orientation == "landscape"

    def portrait(self):
        for a in self.sizes:
            x,y =  self.sizes[a]
            self.sizes[a] = ((min(y,x),max(y,x)))
        self.orientation == "portrait"


#a = Arkki("A2")
#print a.size_mm()
