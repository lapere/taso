from utils import *

def kaari(center, start, angle):
    """center point, startpoint and angle to tuples"""
    
    l = line_dist(center[0], center[1], start[0], start[1])
    start_angle = line_angle(center[0], center[1], start[0], start[1])
    
    #print "\nARC",start_angle,angle,l

    arg = []
    
    start_angle += 360
    jaa = float(angle % 20)
    osat = floor(angle / 20)
    if osat:
        step = int(20 + round(jaa / osat))
    else:
        return ((0,0),(0,0))
    
    it = range(int(start_angle), int(start_angle + angle + step), step)
    it[0] = int(start_angle)
    it[-1] = int(start_angle + angle)

    for a in it:
        rad = radians(a)
        arg.append((cos(rad)*l+center[0], sin(rad)*l+center[1]))
            
    #print arg
    return tuple(arg)

