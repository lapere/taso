from math import *

def rotate_points(x, y, angle):
        alfa = radians(float(angle))
        x = x * cos(alfa) - y * sin(alfa)
        y = x * sin(alfa) + y * cos(alfa)   
        return x,y
