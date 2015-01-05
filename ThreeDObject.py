import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sqrt,pi

def saveMatrices():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

def popMatrices():
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def applyTransform(transform):
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(transform[0][0],transform[0][1],transform[0][2])
    glRotatef(transform[1][0]*180/pi,transform[1][1],transform[1][2],\
              transform[1][3])
    glScalef(transform[2][0],transform[2][1],transform[2][2])

class ThreeDObject:
    def __init__(self):
        self.transform = [[0.0,0.0,0.0],[0.0,0.0,0.0,1.0],[1.0,1.0,1.0]]
        self.drawing = []
        self.children = []
    
    def addChild(self,obj):
        self.children.append(obj)
    
    def addDraw(self,drawing):
        self.drawing.append(drawing)
    
    def setLocation(self,location):
        self.transform[0] = location
    
    def move(self,trans):
        self.transform[0][0] += trans[0]
        self.transform[0][1] += trans[1]
        self.transform[0][2] += trans[2]
    
    def setRotation(self,rotation):
        self.transform[1] = rotation

    def rotate(self,rot):
        self.transform[1][0] += rot
    
    def setScaling(self,scaling):
        self.transform[2] = scaling
    
    def scale(self,scl):
        self.transform[2][0] += scl[0]
        self.transform[2][1] += scl[1]
        self.transform[2][2] += scl[2]
    
    def draw(self):
        saveMatrices()
        applyTransform(self.transform)
        for d in self.drawing:
            eval(d)
        for c in self.children:
            saveMatrices()
            applyTransform(c[0])
            c[1].draw()
            popMatrices()
        popMatrices()

def useMaterial(R,G,B,specular,shrininess):
    material = [\
        [0.3*R, 0.3*G, 0.3*B, 1.0],[0.8*R, 0.8*G, 0.8*B, 1.0],\
        [specular, specular, specular, 1.0],shrininess]
    glMaterialfv(GL_FRONT,GL_AMBIENT, material[0]);
    glMaterialfv(GL_FRONT,GL_DIFFUSE, material[1]);
    glMaterialfv(GL_FRONT,GL_SPECULAR,material[2]);
    glMaterialf(GL_FRONT,GL_SHININESS,material[3]);

def projectToXY(p):
    return [p[0],p[1],0]
def projectToXZ(p):
    return [p[0],0,p[2]]
def projectToYZ(p):
    return [0,p[1],p[2]]
def projectToX(p):
    return [p[0],0,0]
def projectToY(p):
    return [0,p[1],0]
def projectToZ(p):
    return [0,0,p[2]]
