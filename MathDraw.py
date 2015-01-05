import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ThreeDObject import ThreeDObject
from ThreeDObject import saveMatrices,popMatrices
from math import sqrt,cos,pi,sin,acos

class PlaneEnviron:
    def __init__(self,left,bottom,right,top):
        self.left = left
        self.bottom = bottom
        self.right = right 
        self.top = top 
        self.strings = []
        self.drawing = []
    
    def setLeft(self,value):
        self.left = value

    def setRight(self,value):
        self.right = value

    def setBottom(self,value):
        self.bottom = value
        
    def setTop(self,value):
        self.top = value
    
    def draw(self,x0,y0,w,h):
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        left,right,bottom,top = self.left, self.right, self.bottom, self.top
        if (w <= h):
            gluOrtho2D(left, right, bottom * float(h) / float(w),\
                top * float(h) / float(w))
        else:
            gluOrtho2D(left * float(w) / float(h),\
                right * float(w) / float(h), bottom, top)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(x0, y0, w, h)

        for s in self.strings:
            glColor3fv(s[2])
            glRasterPos2f(s[0][0],s[0][1])
            n = 0
            for c in s[1]:
                if c != "\n":
                    glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24,ord(c))
                else:
                    n += 1
                    glRasterPos2f(s[0][0],s[0][1]-n*(self.top-self.bottom)/32)

        for d in self.drawing:
            eval(d)

class ThdEnviron:
    def __init__(self,left,bottom,right,top,near,far):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
        self.near = near
        self.far = far
        self.eyex = 5.0
        self.eyey = 5.0
        self.eyez = 5.0
        self.lightx = 10.0
        self.lighty = 10.0
        self.lightz = 10.0
        self.specular = 0.8
        self.shrininess = 0.8
        self.objects = []
        self.drawing = []
        self.lighting = True
        self.ortho = False

    def setLeft(self,value):
        self.left = value

    def setRight(self,value):
        self.right = value

    def setBottom(self,value):
        self.bottom = value
        
    def setTop(self,value):
        self.top = value

    def setNear(self,value):
        self.near = value
        
    def setFar(self,value):
        self.far = value
    
    def setEyeX(self,value):
        self.eyex = value
    def moveEyeX(self,value):
        self.eyex += value
    def setLightX(self,value):
        self.lightx = value
    def moveLightX(self,value):
        self.lightx += value

    def setEyeY(self,value):
        self.eyey = value
    def moveEyeY(self,value):
        self.eyey += value
    def setLightY(self,value):
        self.lighty = value
    def moveLightY(self,value):
        self.lighty += value

    def setEyeZ(self,value):
        self.eyez = value
    def moveEyeZ(self,value):
        self.eyez += value
    def setLightZ(self,value):
        self.lightz = value
    def moveLightZ(self,value):
        self.lightz += value
    
    def draw(self,x0,y0,w,h):
        # Initialize 3d environment
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        if self.lighting:
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
        left,right,bottom,top,near,far = self.left,self.right,self.bottom,\
                                         self.top,self.near,self.far
        eyex, eyey, eyez = self.eyex, self.eyey, self.eyez
        lightx, lighty, lightz = self.lightx, self.lighty, self.lightz
        if not self.ortho:
            if w <= h:
                glFrustum(left, right, bottom * float(h) / float(w), top *\
                float(h) / float(w), near, far)
            else:
                glFrustum(left * float(w) / float(h), \
                right * float(w) / float(h), bottom, top, near, far)
        else:
            if w <= h:
                glOrtho(left, right, bottom * float(h) / float(w), top *\
                float(h) / float(w), near, far)
            else:
                glOrtho(left * float(w) / float(h), \
                right * float(w) / float(h), bottom, top, near, far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glViewport(x0, y0, w, h)
        if not self.ortho:
            if eyex != 0 or eyey != 0:
                gluLookAt(eyex, eyey, eyez, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
            else:
                gluLookAt(eyex, eyey, eyez, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        else:
            if eyex != 0 or eyey != 0:
                gluLookAt(eyex, eyey, eyez, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
            else:
                gluLookAt(eyex, eyey, eyez, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        light0_pos = [lightx,lighty,lightz,1.0]
        light0_spt = [-lightx,-lighty,-lightz,1.0]
        glLightfv(GL_LIGHT0,GL_POSITION,light0_pos)
        glLightfv(GL_LIGHT0,GL_SPOT_DIRECTION,light0_spt)
        glLightf(GL_LIGHT0,GL_SPOT_CUTOFF,45)

        for d in self.drawing:
            eval(d)
        for o in self.objects:
            o.draw()

class MathDraw:
    def __init__(self,winw,winh):
        self.bgcolor = [0.0,0.0,0.0,0.0]
        self.background = PlaneEnviron(-2.0,-2.0,2.0,2.0)
        self.mainpart = ThdEnviron(-2.0,-2.0,2.0,2.0,1.20,140.0)
        self.foreground = PlaneEnviron(-2.0,-2.0,2.0,2.0)
        self.context = 0
        self.winw = winw
        self.winh = winh
    
    def setBgColor(self,r,g,b,a):
        self.bgcolor = [r,g,b,a]
    
    def setBgLeft(self,value):
        self.background.setLeft(value)

    def setBgRight(self,value):
        self.background.setRight(value)
    
    def setBgBottom(self,value):
        self.background.setBottom(value)

    def setFrTop(self,value):
        self.foreground.setTop(value)

    def setFrLeft(self,value):
        self.foreground.setLeft(value)

    def setFrRight(self,value):
        self.foreground.setRight(value)
    
    def setFrBottom(self,value):
        self.foreground.setBottom(value)

    def setFrTop(self,value):
        self.foreground.setTop(value)

    def setMnLeft(self,value):
        self.mainpart.setLeft(value)

    def setMnRight(self,value):
        self.mainpart.setRight(value)
    
    def setMnBottom(self,value):
        self.mainpart.setBottom(value)

    def setMnTop(self,value):
        self.mainpart.setTop(value)

    def setMnNear(self,value):
        self.mainpart.setNear(value)

    def setMnFar(self,value):
        self.mainpart.setFar(value)
    
    def setEyeX(self,value):
        self.mainpart.eyex = value

    def setEyeY(self,value):
        self.mainpart.eyey = value

    def setEyeZ(self,value):
        self.mainpart.eyez = value

    def moveEyeX(self,value):
        self.mainpart.eyex += value

    def moveEyeY(self,value):
        self.mainpart.eyey += value

    def moveEyeZ(self,value):
        self.mainpart.eyez += value

    def setLightX(self,value):
        self.mainpart.lightx = value
    def moveLightX(self,value):
        self.mainpart.lightx += value

    def setLightY(self,value):
        self.mainpart.lighty = value
    def moveLightY(self,value):
        self.mainpart.lighty += value

    def setLightZ(self,value):
        self.mainpart.lightz = value
    def moveLightZ(self,value):
        self.mainpart.lightz += value
    
    def setWinW(self,value):
        self.winw = value
    
    def setWinH(self,value):
        self.winh = value

    def draw(self,x0,y0,w,h,context=3,clear=True):
        if clear:
            glClearColor(self.bgcolor[0],self.bgcolor[1],\
                         self.bgcolor[2],self.bgcolor[3])
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if context == 0 or context==3: self.background.draw(x0,y0,w,h)
        if context == 1 or context==3: self.mainpart.draw(x0,y0,w,h)
        if context == 2 or context==3: self.foreground.draw(x0,y0,w,h)
        if clear:
            glutSwapBuffers()

    def back(self):
        self.context = 0
    
    def fore(self):
        self.context = 2

    def mainp(self):
        self.context = 1
    
    def addString(self,pos,string,color):
        if self.context == 0:
            self.background.strings.append([pos,string,color])
        elif self.context == 2:
            self.foreground.strings.append([pos,string,color])
    
    def addObject(self,obj):
        if self.context == 1:
            self.mainpart.objects.append(obj)

    def add(self,operation):
        if self.context == 0:
            self.background.drawing.append(operation)
        if self.context == 1:
            self.mainpart.drawing.append(operation)
        if self.context == 2:
            self.foreground.drawing.append(operation)

def drawquad(left,bottom,right,top,color):
    glColor3fv(color)
    glBegin(GL_QUADS)
    glVertex2f(left,bottom)
    glVertex2f(right,bottom)
    glVertex2f(right,top)
    glVertex2f(left,top)
    glEnd()

def drawline3d(p1,p2,color):
    glDisable(GL_LIGHTING)
    glColor3fv(color)
    glBegin(GL_LINES)
    glVertex3fv(p1)
    glVertex3fv(p2)
    glEnd()
    glEnable(GL_LIGHTING)

def normCrossProduct(v1,v2):
    r0 = v1[1]*v2[2]-v1[2]*v2[1]
    r1 = v1[2]*v2[0]-v1[0]*v2[2]
    r2 = v1[0]*v2[1]-v1[1]*v2[0]
    norm = sqrt(r0*r0+r1*r1+r2*r2)
    return [r0/norm,r1/norm,r2/norm]

def angle(v1,v2):
    inner = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
    n1 = sqrt(v1[0]*v1[0]+v1[1]*v1[1]+v1[2]*v1[2])
    n2 = sqrt(v2[0]*v2[0]+v2[1]*v2[1]+v2[2]*v2[2])
    return acos(inner/n1/n2)*180/pi

def useMaterial(R,G,B,specular,shrininess):
    material = [\
        [0.3*R, 0.3*G, 0.3*B, 1.0],[0.8*R, 0.8*G, 0.8*B, 1.0],\
        [specular, specular, specular, 1.0],shrininess]
    glMaterialfv(GL_FRONT,GL_AMBIENT, material[0]);
    glMaterialfv(GL_FRONT,GL_DIFFUSE, material[1]);
    glMaterialfv(GL_FRONT,GL_SPECULAR,material[2]);
    glMaterialf(GL_FRONT,GL_SHININESS,material[3]);

def drawquad3d(p1,p2,p3,p4,color,specular,shrininess):
    glColor3f(1.0,1.0,1.0)
    v1 = [p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]]
    v2 = [p3[0]-p2[0],p3[1]-p2[1],p3[2]-p2[2]]
    normal = normCrossProduct(v1,v2)
    glNormal3fv(normal)
    useMaterial(color[0],color[1],color[2],specular,shrininess)
    glBegin(GL_QUADS)
    glVertex3fv(p1)
    glVertex3fv(p2)
    glVertex3fv(p3)
    glVertex3fv(p4)
    glEnd()

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

def drawCursor(p):
    drawline3d(p,projectToXY(p),[1.0,1.0,1.0])
    drawline3d(p,projectToYZ(p),[1.0,1.0,1.0])
    drawline3d(p,projectToXZ(p),[1.0,1.0,1.0])
    drawline3d(projectToXY(p),projectToX(p),[1.0,1.0,1.0])
    drawline3d(projectToXY(p),projectToY(p),[1.0,1.0,1.0])
    drawline3d(projectToYZ(p),projectToY(p),[1.0,1.0,1.0])
    drawline3d(projectToYZ(p),projectToZ(p),[1.0,1.0,1.0])
    drawline3d(projectToXZ(p),projectToX(p),[1.0,1.0,1.0])
    drawline3d(projectToXZ(p),projectToZ(p),[1.0,1.0,1.0])

def drawcube(p1,p2,p3,p4,p5,p6,p7,p8,colors,specular,shrininess):
    drawquad3d(p4,p3,p2,p1,colors[0],specular,shrininess)
    drawquad3d(p5,p6,p7,p8,colors[1],specular,shrininess)
    drawquad3d(p1,p2,p6,p5,colors[2],specular,shrininess)
    drawquad3d(p2,p3,p7,p6,colors[3],specular,shrininess)
    drawquad3d(p3,p4,p8,p7,colors[4],specular,shrininess)
    drawquad3d(p4,p1,p5,p8,colors[5],specular,shrininess)

def drawArrow(p1,p2,color):
    drawline3d(p1,p2,color)
    saveMatrices()
    glTranslatef(p2[0],p2[1],p2[2])
    useMaterial(color[0],color[1],color[2],0.5,0.5)
    if p1[0] != p2[0] or p1[1] != p2[1]:
        r = [p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]]
        n = normCrossProduct(r,[0,0,1])
        glRotatef(-angle(r,[0,0,1]),n[0],n[1],n[2])
    glutSolidCone(0.1,0.1,10,10)
    popMatrices()
