from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

contours = dict()
        
class Point:
    cnt = 0
    def __init__(self, x, y):
        Point.cnt += 1
        self.x = x
        self.y = y
        self.name = Point.cnt
        self.color = [0.2, 0.2, 0.2]
        self.create_visibles()
        

    def create_visibles(self):
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        glVertex2fv((self.x, self.y, 100))
        glEnd()
        glFinish()
        
    def repaint(self, mode=None):
        if mode == GL_SELECT:
            glLoadName(self.name)
        self.create_visibles()

    def move(self, x, y):
        vp = glGetIntegerv (GL_VIEWPORT)
        self.x = x
        self.y = vp[3] - y
        glClear( GL_COLOR_BUFFER_BIT )
        for i in contours:
            contours[i].repaint()
        glFinish()

    def active(self):
        self.color = [1.0, 0.0, 0.0]
        
    def passive(self):
        self.color = [0.2, 0.2, 0.2]

        
def left_down(x, y):
    vp = glGetIntegerv (GL_VIEWPORT)
    p = Point(x, vp[3] - y)
    contours.update({p.name:p})
   

def middle_down(x, y):

    glSelectBuffer(1000) 
    glRenderMode(GL_SELECT)

    glInitNames()
    glPushName(0)
    
    glMatrixMode (GL_PROJECTION)   
    glPushMatrix()
    glLoadIdentity()
    y = 400 - y
    gluOrtho2D(x-5, x+5, y-5, y+5)
    display(mode=GL_SELECT)
    glMatrixMode (GL_PROJECTION)
    glPopMatrix()

    b = glRenderMode(GL_RENDER)

    for hit_record in b:
        h = hit_record[2][0]
        return contours[h]
        
        
    
def mouse_move(x, y):
    hit = middle_down(x,y)
    if hit:
        hit.active()
        hit.repaint()
    else:
        for i in contours:
            contours[i].passive()
            contours[i].repaint()
    
def mouse_clicked(button, state, x, y):
    #print button, state, x ,y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN: 
            left_down(x, y)

    elif button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN: 
            hit = middle_down( x, y )
            print hit.move
            glutMotionFunc(hit.move)
        elif state == GLUT_UP:
            glutMotionFunc(None)



def display(mode=None):
    
    glClear( GL_COLOR_BUFFER_BIT )
    for i in contours:
        contours[i].repaint(mode)
    glFinish()


def clear():
    global contours
    contours = dict()



def menu_selected(entry):

    if entry == 1:
        print "clear"
        clear()
    elif entry == 2:
        pass
    glutPostRedisplay()




def myinit():

   """ clear background to gray """
   glClearColor( 0.91, 0.90, 0.89, 0.0 )
   
   glPointSize(6)

   menu = glutCreateMenu( menu_selected )

   glutAddMenuEntry( "clear", 1)
   glutAddMenuEntry( "quit", 2)

   glutAttachMenu( GLUT_RIGHT_BUTTON )

   glutMouseFunc(mouse_clicked)
   glutPassiveMotionFunc(mouse_move)


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, w, 0.0, h)


def main():
    
    import sys
    
    glutInit( sys.argv )
    glutInitDisplayMode( GLUT_SINGLE | GLUT_RGB )
    glutInitWindowPosition(0, 0)
    glutInitWindowSize( 400, 400 )
    glutCreateWindow("Huju")

    myinit()

    glutDisplayFunc( display )
    glutReshapeFunc( reshape )
    
    glutMainLoop()

main()

