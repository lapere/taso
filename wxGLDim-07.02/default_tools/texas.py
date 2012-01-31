#! /usr/bin/python


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLE import *
from math import *
import sys

lastx = 0
lasty = 0
angle = 360
class wash:

        def __init__(self):
                points = ((0.0, 0.0), (1.0, 0.0), (1.0, 10.0), (0.0, 10.0), (0.0,0.0))
                self.twist = []
                self.curve = []
                tspine = []
                flat_a = radians(358*(4.0/5.0))

                for i in range(360+95):
                        a = radians(i*(4.0/5.0))

                        if i < 361:
                                tw = degrees(cos(a*(5.0/4.0)))-57
                                tspine.append((sin(a) * 5, cos(a) * 5, cos(a*(5.0/4.0)) * 5))
                                self.twist.append(tw*0.725)
                                
                        else:
                                tspine.append((sin(a) * 5, cos(a) * 5, flat_a))
                                self.twist.append(0.0)
                        
                self.stroke = 5
                self.tspine = tuple(tspine)
                self.section = map(lambda x: (x[0], x[1]), points[1:])

                
                self.normal = []

                for i in range(1, len(points)):
                        ax = points[i][0] - points[i-1][0]
                        ay = points[i][1] - points[i-1][1]
                        alen = sqrt (ax*ax + ay*ay)
                        self.normal.append((-ay / alen, ax / alen))
                        
                self.normal.insert(0, self.normal[-1])

        def displace(self, a):
                a = a % 360
                if a < 288:
                        return cos(radians(a)*(5.0/4.0)) * 5
                else:
                        return 5.0

        def repaint(self, angle):
                glPushMatrix()
                # set up some matrices so that the object spins with the mouse
                gleSetJoinStyle(TUBE_NORM_FACET | TUBE_JN_ANGLE | TUBE_CONTOUR_CLOSED | TUBE_JN_CAP)
                #glTranslatef (0.0, 0.0, -100.0)
                glRotatef (angle, 0.0, 0.0, 1.0)
                glColor3f(0.1, 0.66, 0.6)
                gleTwistExtrusion(self.section, self.normal, None, self.tspine, None, self.twist)
                glTranslatef (0.0, 0.0, -5.0)
                gluCylinder(gluNewQuadric(), 7.5, 7.5, 10, 64, 64)
                gluCylinder(gluNewQuadric(), 2.0, 2.0, 10, 64, 64)
                gluDisk(gluNewQuadric(), 2.0, 7.5, 64, 8)
                glTranslatef (0.0, 0.0, 10.0)
                gluDisk(gluNewQuadric(), 2.0, 7.5, 64, 8)                
                glPopMatrix()        
                

w = wash()

def cylinder_hot():
        glPushMatrix ()
        glColor4f(0.77, 0.1, 0.1, 0.5)
        h = hypot(5.0,5.0)
        glTranslatef (h, h, 20.0)
        gluCylinder(gluNewQuadric(), 9.0, 9.0, 15, 64, 64)
        glPopMatrix()

def cylinder_cold():
        glPushMatrix ()
        glColor4f(0.1, 0.6, 0.66, 0.5)
        h = hypot(5.0,5.0)
        glRotatef ((360/5) * 2, 0.0, 0.0, 1.0)
        glTranslatef (h, h, 5.0)
        gluCylinder(gluNewQuadric(), 9.0, 9.0, 15, 64, 64)
        glPopMatrix ()

def piston_hot(angle):
        glPushMatrix ()
        glColor3f(0.9, 0.6, 0.1)
        h = hypot(5.0,5.0)
        glTranslatef (h, h, w.displace(angle + 72))
        gluCylinder(gluNewQuadric(), 1.0, 1.0, 25.0, 64, 64)
        glTranslatef (0.0, 0.0,  25.0)
        gluCylinder(gluNewQuadric(), 8.9, 8.9, 5.0, 64, 64)
        glTranslatef (0.0, 0.0, 5.0)
        gluDisk(gluNewQuadric(), 0.0, 8.9, 64, 8)                
        glPopMatrix()

def piston_cold(angle):
        glPushMatrix ()
        glColor3f(0.1, 0.6, 0.9)
        h = hypot(5.0,5.0)
        glRotatef ((360/5) * 2, 0.0, 0.0, 1.0)
        glTranslatef (h, h, w.displace(angle-72))
        gluCylinder(gluNewQuadric(), 1.0, 1.0,  15.0, 64, 64)
        glTranslatef (0.0, 0.0, 10)
        gluCylinder(gluNewQuadric(), 8.9, 8.9, 5.0, 64, 64)
        glTranslatef (0.0, 0.0, 5.0)
        gluDisk(gluNewQuadric(), 0.0, 8.9, 64, 8)                
        glPopMatrix()


def DrawStuff(a = None):
        global w, angle
	glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	# set up some matrices so that the object spins with the mouse
        a = angle
	glPushMatrix ()
	glTranslatef (20.0, 0.0, -200.0)
	glRotatef (lastx, 0.0, 1.0, 0.0)
	glRotatef (90, 0.0, 0.0, 1.0)
        w.repaint(a)
        piston_cold(a)
        piston_hot(a)
        cylinder_cold()
        cylinder_hot()
        
	glPopMatrix ()
	glutSwapBuffers()




# get notified of mouse motions
def MouseMotion (x, y):
	global lastx, lasty
	lastx = x
	lasty = y
	glutPostRedisplay ()


def JoinStyle (msg):
	sys.exit(0)


# set up a light 

lightOnePosition = (4000.0, 400, 1000.0, 0.0)
lightOneColor = (0.99, 0.99, 0.99, 1.0)

lightTwoPosition = (-40.0, 40, 100.0, 0.0)
lightTwoColor = (0.99, 0.99, 0.99, 1.0)

def play():
        global angle
        angle += 1
        if angle > 360:
                angle = 0
        glutPostRedisplay()
