from math import *

def rotate_points(x, y, angle):
        alfa = radians(float(angle))
        x_tmp = x * cos(alfa) + y * sin(alfa)
        y_tmp = x * sin(alfa) - y * cos(alfa)   
        return x_tmp, y_tmp

def rotate(canvas, tag, angle):
    pnts = canvas.coords(tag)
    rotated = [tag]
    for x,y in zip(pnts[0:len(pnts):2], pnts[1:len(pnts):2]):
        x,y = rotate_points(x, y, angle)
        rotated.append(x)
        rotated.append(y)
    canvas.coords(*rotated)
    
