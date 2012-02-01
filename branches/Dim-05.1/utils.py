# -*- coding: utf-8 -*-
from math import *
from Tkinter import *

def line_center_normal(startp0, endp0):
    
        l1 = suoranABC(startp0, endp0)
       
        l1_c = keski_piste(startp0[0], startp0[1], endp0[0], endp0[1])
        
        a0 = RadBetweenTwoPoint(startp0[0], startp0[1], endp0[0], endp0[1])
        a0 = a0 + (pi / 2.0)
        #print a0
        l1 = suoranABC(l1_c, rad=-a0)
        
	return l1


def suoranABC(startp, endp=None, rad=None):
    
        if rad != None:
            dx, dy = cos(rad), sin(rad)
            endp = startp[0] + dx, startp[1] + dy

        A = float(-(startp[1] - endp[1]))
        B = float((startp[0] - endp[0]))
        C = float(-A * startp[0] - B * startp[1])

        if A == 0 and B == 0:
            raise "EEEEEEEEERRRR"

        return dict(A=A,B=B,C=C)

def solve2l(l1, l2):
        #print l1,l2

        nim = l1['A'] * l2['B'] - l2['A'] * l1['B']

        if not nim:
            raise ValueError, "Parallel lines"
            
        x_os = -l1['C'] *  l2['B'] - -l2['C'] *  l1['B']
        y_os =  l1['A'] * -l2['C'] - l2['A'] * -l1['C']

        x = float(x_os) / nim
        y = float(y_os) / nim
    
        return x, y
 
def AngleBetweenTwoPoint(x,y,x0,y0):
        
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
                    
        alfa = (alfa * 360) / (2 * pi)

        return -alfa

def RadBetweenTwoPoint(x,y,x0,y0):
        
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

def DistBetweenTwoPoint(x0, y0, x1, y1):

        r = hypot((x0-x1), (y0-y1))

        return r
    
def k_kerroin(x0, y0, x1, y1):
	if x1-x0:
	        return float(y1 - y0)/(x1 - x0)
	else:
	        return None
    
def normaalin_k_kerroin(x0, y0, x1, y1):
	    
	    k = k_kerroin(x0, y0, x1, y1)

            if k == None:
                return 0.0
	    elif k:
                    return float(-1)/k
	    else:
		    return None
		    
def keski_piste(x0, y0, x1, y1):
	x = (x0 + x1) / 2
        y = (y0 + y1) / 2
	return x,y
           
def suorien_leikkauspiste(k0, b0, k1, b1, x0, x1):

        if b0 == None:
            x = x0
            y = k1*x + b1
        elif b1 == None:
            x = x1
            y = k0*x + b0
	elif k0-k1:
	    x = float(b1 - b0)/(k0 - k1)
	    y = k1*x + b1
        else:
            x = None
            y = None
	
	return x,y
	
	
def suoran_vakiotermi(x,y,k):
        if k != None:
            return y - k*x
        else:
            return None

def create_point(self, x, y):
	fred = self.create_rectangle(x - 3, y - 3, x + 3, y + 3,
                outline="blue", fill="blue")
        return fred

 
