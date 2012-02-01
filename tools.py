from math import *


def solvey(self, other):
    
    nim = self.A() * other.B() - other.A() * self.B()
    
    if not nim:
        return 0, 0
        
    x_os = -self.C() *  other.B() - -other.C() *  self.B()
    y_os =  self.A() * -other.C() - other.A() * -self.C()

    x = float(x_os) / nim
    y = float(y_os) / nim

    return y
    
def solvex(self, other):
    
    nim = self.A() * other.B() - other.A() * self.B()
    
    if not nim:
        return 0, 0
        
    x_os = -self.C() *  other.B() - -other.C() *  self.B()
    y_os =  self.A() * -other.C() - other.A() * -self.C()

    x = float(x_os) / nim
    y = float(y_os) / nim

    return x

def radp(x,y,x0,y0):
        
        if (x0-x):
            alfa = atan(float(y0-y)/(x0-x))
        elif x0 > x:
            alfa = pi / 2
	else:
            alfa = -pi / 2
        
        if y0 > y:
            if x0 > x:
                    alfa = alfa
            else:
                    alfa = pi + alfa
        else:
            if x0 < x:
                    alfa = alfa - pi
            else:
                    alfa = alfa    
                    
        return -alfa    
