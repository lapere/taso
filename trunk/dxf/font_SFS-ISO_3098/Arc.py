# -*- coding: utf-8 -*-

from math import *
from Tkinter import *
from kaari import *
from utils import *

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
 
           
    
def is_clockw(startp, midp, endp):

        l = suoranABC(startp, midp)
        try:
            y_pullahdus = (-l['A']*endp[0] - l['C']) / l['B']  

            if startp[0] < midp[0]:
                if y_pullahdus < endp[1]:
                    return True
                else:
                    return False
            else:
                if y_pullahdus > endp[1]:
                    return True
                else:
                    return False
        except:
            return True

def cp_startenddir(startp, endp, dire):

        d0 = dire + pi / 2
        a0 = RadBetweenTwoPoint(startp[0], startp[1], endp[0], endp[1])

        ##print "dire=", dire, "a0=",a0
        
        if a0 > dire:
            direction = False
        else:
            direction = True
            
        a0 = a0 + pi / 2
        
        
        l1 = suoranABC(startp, rad = d0)
        l2 = line_center_normal(startp, endp)
    
        center = solve2l(l1, l2)
        #print "center"+str(center)
        dx, dy = cos(dire), sin(dire)
   
        direp1 = startp[0] + dx, startp[1] + dy
        
        direction = is_clockw(startp, direp1, endp)
        
	return direction, center

def cp_startendangl(startp, endp, angle):
        
	a0 = RadBetweenTwoPoint(startp[0], startp[1], endp[0], endp[1])
	dire = a0 + angle / 2
	##print a0, dire
        return cp_startenddir(startp, endp, -dire) 
	
def cp_startendradius(startp, endp, radius):
    
        l = DistBetweenTwoPoint(startp[0], startp[1], endp[0], endp[1])
        l = l / 2.0
        a = asin(l / radius)
        a = (a * 360) / pi

        center = cp_startendangl(startp, endp, a)[1]

        return True, center	

def cp_3p(startp, midp, endp):
    
        l1 = suoranABC(startp, midp)
        l2 = suoranABC(midp, endp)
       
        l1_c = keski_piste(startp[0], startp[1], midp[0], midp[1])
        l2_c = keski_piste(midp[0], midp[1], endp[0], endp[1])

        if l1['A']:
            l1['A'] = (-l1['B'] * l1['B']) / l1['A']
        else:
            l1['A'] = -l1['B'] * l1['B']
        if l2['A']:
            l2['A'] = (-l2['B'] * l2['B']) / l2['A']
        else:
            l2['A'] = -l2['B'] * l2['B']
  
	l1['C'] = -l1['A'] * l1_c[0] - l1['B'] * l1_c[1]
	l2['C'] = -l2['A'] * l2_c[0] - l2['B'] * l2_c[1]

	center = solve2l(l1, l2)

	direction = is_clockw(startp, midp, endp)
    
	return direction, center
	
     
def _arc(self, startp=None, midp=None, endp=None, center=None, direction=None, radius=None, angle=None, length=None, astart=None, clockw=True):

        if startp == None:
                if astart and radius and center:
                        x = center[0] + radius * cos(radians(astart)) 
                        y = center[1] + radius * sin(radians(astart))
                        startp = (x,y)

	if center == None:
		if direction != None:
			clockw, center = cp_startenddir(startp, endp, direction)
		elif angle != None:
			clockw, center = cp_startendangl(startp, endp, angle)
		elif radius != None:
			clockw, center = cp_startendradius(startp, endp, radius)
		elif midp != None:
			clockw, center = cp_3p(startp, midp, endp)
			
	if radius == None:
		radius = DistBetweenTwoPoint(center[0], center[1], startp[0], startp[1])

	if astart == None:
		astart = AngleBetweenTwoPoint(center[0], center[1], startp[0], startp[1])
                
 	if angle == None:
		if length != None:
            		angle = asin(length/(2*radius))*2
            		angle = (angle / pi) * 180
		elif endp != None:
			aend = AngleBetweenTwoPoint(center[0], center[1], endp[0], endp[1])
         
                        if astart > aend:
                                angle = astart - aend
                        else:
                                angle = 360 - aend + astart
     
                if not clockw:
                        astart = aend
                        angle = 360 - angle
        else:
                pass
                #angle = (angle / pi) * 180.0

        print center, startp, angle
        line = kaari(center, startp, angle)
        arg = []
        #tag = str(self)
        for point in line:
                x = round(point[0], 2)
                y = round(point[1], 2) 
                arg.append(x)
                arg.append(y)
                    
        tag = self.create_line(arg, capstyle="round")

        return tag

        
                          
if __name__ == '__main__':
    root = Tk()
    c = Canvas(root)
    
    _arc(c, startp=(100, 100), center=(200,200), endp=(200, 100))
    #_arc(c, startp=(100, 100), angle=pi/2, endp=(200, 200))
    #_arc(c, startp=(100, 100), angle=pi/2, endp=(200, 100))
    #_arc(c, startp=(100,100+i), center=(200, 200+i), angle=i)
    #arc(c, startp=(100,100), endp=(200, 100), direction=45)
    #b = Button(root)
    #b.pack()
    c.pack(fill=BOTH, expand=1)
    #app.master.title("CAD_GUI")
    root.mainloop()
