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

def  solve_circle_circle(x0, y0, r0, x1, y1 r1):

  #dx and dy are the vertical and horizontal distances between
  #the circle centers.

  dx = x1 - x0;
  dy = y1 - y0;

  #Determine the straight-line distance between the centers. */
  #d = sqrt((dy*dy) + (dx*dx));
  d = hypot(dx,dy); # Suggested by Keith Briggs

  # Check for solvability. */
  if (d > (r0 + r1)):
      # no solution. circles do not intersect. */
      return 0;
  
  if (d < fabs(r0 - r1)):
      #/* no solution. one circle is contained in the other */
      return 0;

  #/* 'point 2' is the point where the line through the circle
  # * intersection points crosses the line between the circle
  # * centers.  
  # */

  #/* Determine the distance from point 0 to point 2. */
  a = ((r0*r0) - (r1*r1) + (d*d)) / (2.0 * d) ;

  #/* Determine the coordinates of point 2. */
  x2 = x0 + (dx * a/d);
  y2 = y0 + (dy * a/d);

  #/* Determine the distance from point 2 to either of the
  # * intersection points.
  h = sqrt((r0*r0) - (a*a));

  #/* Now determine the offsets of the intersection points from
  # * point 2.
  rx = -dy * (h/d);
  ry = dx * (h/d);

  #/* Determine the absolute intersection points. */
  xi = x2 + rx;
  xi_prime = x2 - rx;
  yi = y2 + ry;
  yi_prime = y2 - ry;

  return (xi,yi),(xi_prime,yi_prime)

"""
/*
   Calculate the intersection of a ray and a sphere
   The line segment is defined from p1 to p2
   The sphere is of radius r and centered at sc
   There are potentially two points of intersection given by
   p = p1 + mu1 (p2 - p1)
   p = p1 + mu2 (p2 - p1)
   Return FALSE if the ray doesn't intersect the sphere.
*/
"""

def ray_circle(x0, y0, x1, y1, x2, y2, r):

   a = (x1 - x0)**2 + (y1 - y0)**2
   
   b = 2 * ((x1 - x0) * (x0 - x2) + (y1 - y0) * (y0 - y2))

   c = x2**2 + y2**2 + x0**2 + y0**2 - 2 * (x2 * x0 + y2 * y0) - r**2
   
   bb4ac = float(b * b - 4 * a * c)

   #if (abs(a) < EPS || bb4ac < 0):
   #   return None

   mu1 = (-b + sqrt(bb4ac)) / (2 * a)
   mu2 = (-b - sqrt(bb4ac)) / (2 * a)

   x = x0 + mu1*(x1 - x0)
   y = y0 + mu1*(y1 - y0)
   return x,y


def rc(a, c):
    pass
    
       
def xypo(a,b):
    try:
        return sqrt(a**2 - b**2)
    except:
        return None

if __name__ == '__main__':
    print ray_circle(300, 300, 3, 3, 150, 150, 100)
