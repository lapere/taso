from math import *

def lev():
    for g in globals():
        if g[0] == "c":
            print g
    return 100 

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
    
