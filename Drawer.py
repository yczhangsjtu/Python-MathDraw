import sys
from ThreeDObject import ThreeDObject
from Robot import Robot
from MathDraw import MathDraw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sqrt,cos,pi,sin
from webcolors import name_to_rgb
import re

winw = 1300
winh = 720
class Panel:
    def __init__(self):
        self.eyer = 5.0
        self.eyeh = 3.0
        self.eyet = 0.5
        self.lightr = 5.0
        self.lighth = 3.0
        self.lightt = 0.0
        self.cmdbuf = ""
        self.state = "normal"
        self.cursor = cursor
        self.context = 0
        self.lighting = True
        self.color = [1.0,1.0,1.0]
        self.view = 4
    
    def input(self,c,mathdraw):
        if self.state == "normal":
            if c == "a":
                self.eyet -= 0.1
            elif c == "d":
                self.eyet += 0.1
            elif c == "w":
                self.eyeh += 0.1
            elif c == "s":
                self.eyeh -= 0.1
            elif c == "q":
                self.eyer += 0.1
            elif c == "e":
                self.eyer -= 0.1
            elif c == "h":
                if self.view == 0 or self.view == 4:
                    self.cursor.move([-0.1,0.0,0.0])
                elif self.view == 1:
                    self.cursor.move([0.0,-0.1,0.0])
                elif self.view == 2:
                    self.cursor.move([-0.1,0.0,0.0])
                elif self.view == 3:
                    self.cursor.move([-0.1,0.0,0.0])
            elif c == "j":
                if self.view == 0 or self.view == 4:
                    self.cursor.move([0.0,-0.1,0.0])
                elif self.view == 1:
                    self.cursor.move([0.0,0.0,-0.1])
                elif self.view == 2:
                    self.cursor.move([0.0,0.0,-0.1])
                elif self.view == 3:
                    self.cursor.move([0.0,-0.1,0.0])
            elif c == "k":
                if self.view == 0 or self.view == 4:
                    self.cursor.move([0.0,0.1,0.0])
                elif self.view == 1:
                    self.cursor.move([0.0,0.0,0.1])
                elif self.view == 2:
                    self.cursor.move([0.0,0.0,0.1])
                elif self.view == 3:
                    self.cursor.move([0.0,0.1,0.0])
            elif c == "l":
                if self.view == 0 or self.view == 4:
                    self.cursor.move([0.1,0.0,0.0])
                elif self.view == 1:
                    self.cursor.move([0.0,0.1,0.0])
                elif self.view == 2:
                    self.cursor.move([0.1,0.0,0.0])
                elif self.view == 3:
                    self.cursor.move([0.1,0.0,0.0])
            elif c == "u":
                self.cursor.move([0.0,0.0,0.1])
            elif c == "i":
                self.cursor.move([0.0,0.0,-0.1])
            elif c == ":":
                self.cmdbuf = ":"
                self.state = "command"
            elif c == chr(27): # ESC Key
                self.state = "normal"
                self.cmdbuf = ""
            if self.eyer < 0.0: self.eyer = 0.0
            while self.eyet < 0.0: self.eyet += 2*pi
            while self.eyet > 2*pi: self.eyet -= 2*pi
        elif self.state == "command":
            if c == "\r":
                self.state = "normal"
                self.execute(self.cmdbuf,mathdraw)
            elif c == "\b":
                self.cmdbuf = self.cmdbuf[0:-1]
                if self.cmdbuf == "":
                    self.state = "normal"
            elif c == chr(27): # ESC Key
                self.state = "normal"
                self.cmdbuf = ""
            else:
                self.cmdbuf += c

    def draw(self,mathdraw):
        self.exert(mathdraw,0)
        mathdraw.draw(0,0,winw,winh,0,False)
        if self.view == 4:
            self.exert(mathdraw,0)
            mathdraw.draw(winw/2,winh/2,winw/2,winh/2,1,False)
            self.exert(mathdraw,1)
            mathdraw.draw(0,winh/2,winw/2,winh/2,1,False)
            self.exert(mathdraw,2)
            mathdraw.draw(0,0,winw/2,winh/2,1,False)
            self.exert(mathdraw,3)
            mathdraw.draw(winw/2,0,winw/2,winh/2,1,False)
        elif self.view == 0:
            self.exert(mathdraw,0)
            mathdraw.draw(0,0,winw,winh,1,False)
        elif self.view == 1:
            self.exert(mathdraw,1)
            mathdraw.draw(0,0,winw,winh,1,False)
        elif self.view == 2:
            self.exert(mathdraw,2)
            mathdraw.draw(0,0,winw,winh,1,False)
        elif self.view == 3:
            self.exert(mathdraw,3)
            mathdraw.draw(0,0,winw,winh,1,False)
        mathdraw.draw(0,0,winw,winh,2,False)

    def stateinfo(self):
        info = self.state + ";"
        if self.context == 0:
            info += " " + "background; "
        elif self.context == 1:
            info += " " + "3d; "
        elif self.context == 2:
            info += " " + "foreground; "
        info += "Color: [%.2f,%.2f,%.2f]; "\
        %(self.color[0],self.color[1],self.color[2])
        info += "\n"
        if self.lighting:
            info += "Light: [r:%.2f,h:%.2f,t:%.2f]; "\
            %(self.lightr,self.lighth,self.lightt)
        return info

    def special(self,c,mathdraw):
        pass
    
    def exert(self,mathdraw,dim):
        if dim == 0:
            mathdraw.setEyeX(self.eyer*cos(self.eyet))
            mathdraw.setEyeY(self.eyer*sin(self.eyet))
            mathdraw.setEyeZ(self.eyeh)
            mathdraw.mainpart.ortho = False
        elif dim == 1:
            mathdraw.setEyeX(self.eyer)
            mathdraw.setEyeY(0)
            mathdraw.setEyeZ(0)
            mathdraw.mainpart.ortho = True
        elif dim == 2:
            mathdraw.setEyeX(0)
            mathdraw.setEyeY(-self.eyer)
            mathdraw.setEyeZ(0)
            mathdraw.mainpart.ortho = True
        elif dim == 3:
            mathdraw.setEyeX(0)
            mathdraw.setEyeY(0)
            mathdraw.setEyeZ(self.eyer)
            mathdraw.mainpart.ortho = True
        mathdraw.setLightX(self.lightr*cos(self.lightt))
        mathdraw.setLightY(self.lightr*sin(self.lightt))
        mathdraw.setLightZ(self.lighth)
        mathdraw.foreground.strings[0][1] = self.cmdbuf
        mathdraw.foreground.strings[1][1] = self.stateinfo()
        mathdraw.context = self.context
        mathdraw.mainpart.lighting = self.lighting
    
    def execute(self,cmd,mathdraw):
        results = re.match(r':([A-Za-z]+)(\s+(.*))?',cmd)
        if results != None:
            n = results.lastindex
            name = results.group(1)
            if name == "back" or name == "b":
                self.context = 0
                cmdbuf = ""
            elif name == "main" or name == "m":
                self.context = 1
                cmdbuf = ""
            elif name == "fore" or name == "f":
                self.context = 2
                cmdbuf = ""
            elif name == "quit" or name == "q":
                sys.exit()
            elif name == "cursor" or name == "c":
                if n >= 2:
                    args = re.match(r'\s*((\-)?\d+(\.\d+)?)\s+((\-)?\d+(\.\d+)?)\s+((\-)?\d+(\.\d+)?)',\
                                    results.group(2))
                    if args == None:
                        self.cmdbuf = "Invalid arguments for set cursor."
                        return
                    if args.lastindex == 7:
                        x,y,z = float(args.group(1)),float(args.group(4)),\
                                float(args.group(7))
                        self.cursor.transform[0][0] = x
                        self.cursor.transform[0][1] = y
                        self.cursor.transform[0][2] = z
                        self.cmdbuf = "Successfully set cursor position to\
                        %.2f,%.2f,%.2f"%(x,y,z)
                        return
                    else:
                        self.cmdbuf = "Invalid number of arguments for set\
                        cursor position"
                        return
                elif n == 1:
                    self.cmdbuf = "Cursor position: %.2f,%.2f,%.2f"\
                    %(self.cursor.transform[0][0],self.cursor.transform[0][1],\
                    self.cursor.transform[0][2])
            elif name == "all" or name == "a":
                self.view = 4
            elif name == "td":
                self.view = 0
            elif name == "front" or name == "fr":
                self.view = 1
            elif name == "left" or name == "l":
                self.view = 2
            elif name == "top" or name == "t":
                self.view = 3
            elif name == "setcolor" or name == "sc":
                if n >= 2:
                    args = re.match(r'\s*((\-)?\d+(\.\d+)?)\s+((\-)?\d+(\.\d+)?)\s+((\-)?\d+(\.\d+)?)',\
                                    results.group(2))
                    if args == None:
                        args = re.match(r'\s*([A-Za-z]+)',results.group(2))
                        if args == None:
                            self.cmdbuf = "Invalid arguments for set color."
                        else:
                            self.color = name_to_frgb(args.group(1))
                            self.cmdbuf = ""
                        return
                    if args.lastindex == 7:
                        r,g,b = float(args.group(1)),float(args.group(4)),\
                                float(args.group(7))
                        self.color = [r,g,b]
                        self.cmdbuf = ""
                        return
                    else:
                        self.cmdbuf = "Invalid number of arguments for set\
                        color"
                        return
                else:
                    self.cmdbuf = "Invalid number of arguments for set color"
                    return
            elif name == "setnolight" or name == "snl":
                self.lighting = False
                self.cmdbuf = "Successfully turn off light."
                return
            elif name == "setlight" or name == "sl":
                if n >= 2:
                    args = re.match(r'\s*((\-)?\d+(\.\d+)?)\s+((\-)?\d+(\.\d+)?)\s+((\-)?\d+(\.\d+)?)\s*',\
                                    results.group(2))
                    if args == None:
                        self.cmdbuf = "Invalid arguments for set light."
                        return
                    if args.lastindex == 7:
                        r,h,t = float(args.group(1)),float(args.group(4)),\
                                float(args.group(7))
                        self.lightr = r
                        self.lighth = h
                        self.lightt = t
                        self.cmdbuf = "Successfully set light position to\
                        %.2f,%.2f,%.2f"%(r,h,t)
                        return
                    else:
                        self.cmdbuf = "Invalid number of arguments\
                        for set light"
                        return
                else:
                    if n == 1:
                        self.lighting = True 
                        self.cmdbuf = "Successfully turn on light."
                    return
            elif name == "drawball" or name == "db":
                self.context = 1
                mathdraw.context = 1
                if n == 2:
                    args = re.match(r'\s*(\d+(\.\d+)?)\s*',results.group(2))
                    if args == None:
                        self.cmdbuf = "Invalid arguments for drawball"
                        return
                    R = float(args.group(1))
                    [x,y,z]=cursor.transform[0]
                    [r,g,b]=self.color
                    mathdraw.add("useMaterial(%.2f,%.2f,%.2f,0.5,0.5)"%(r,g,b))
                    mathdraw.add("saveMatrices()")
                    mathdraw.add("glMatrixMode(GL_MODELVIEW)")
                    mathdraw.add("glTranslatef(%.2f,%.2f,%.2f)"%(x,y,z))
                    mathdraw.add("glutSolidSphere(%.2f,20,20)"%R)
                    mathdraw.add("popMatrices()")
                    self.cmdbuf = ""
                else:
                    self.cmdbuf = "Invaild arguments for drawball"
                    return
            elif name == "drawcube" or name == "dc":
                self.context = 1
                mathdraw.context = 1
                if n == 2:
                    args = re.match(r'\s*((\-)?\d+(\.\d+)?)\s+((\-)?\d+(\.\d+)?)\s+((\-)?\d+(\.\d+)?)\s*',results.group(2))
                    if args == None:
                        self.cmdbuf = "Invalid arguments for drawcube"
                        return
                    if args.lastindex == 7:
                        [l,w,h] = float(args.group(1)),float(args.group(4)),\
                                float(args.group(7))
                        [x,y,z]=cursor.transform[0]
                        [r,g,b]=self.color
                        mathdraw.add("useMaterial(%.2f,%.2f,%.2f,0.5,0.5)"\
                        %(r,g,b))
                        mathdraw.add("saveMatrices()")
                        mathdraw.add("glMatrixMode(GL_MODELVIEW)")
                        mathdraw.add("glTranslatef(%0.2f,%0.2f,%0.2f)"%(x,y,z))
                        mathdraw.add("glScalef(%0.2f,%0.2f,%0.2f)"%(l,w,h))
                        mathdraw.add("glutSolidCube(1)")
                        mathdraw.add("popMatrices()")
                        self.cmdbuf = ""
                        return
                    else:
                        self.cmdbuf = "Invalid number of arguments for drawcube"
                        return
                else:
                    self.cmdbuf = "Invaild arguments for drawball"
                    return
            elif name == "curve" or name == "cv":
                self.context = 1
                mathdraw.context = 1
                if n == 2:
                    args = re.match(r'\s*(.*)',results.group(2))
                    if args == None:
                        self.cmdbuf = "Invalid arguments for drawball"
                        return
                    filename = args.group(1)
                    [r,g,b]=self.color
                    try:
                        with open(filename,"r") as f:
                            mathdraw.add("glColor3f(%.2f,%.2f,%.2f)"%(r,g,b))
                            mathdraw.add("glDisable(GL_LIGHTING)")
                            mathdraw.add("glBegin(GL_LINE_STRIP)")
                            read = f.readlines()
                            x,y,z = 0,0,0
                            for nums in read:
                                ns = re.match\
                                (r'(\-?\d+(.\d+)?)(\s+(\-?\d+(.\d+)?)(\s+(\-?\d+(.\d+)?))?)?',nums)
                                if ns.lastindex == 3:
                                    if ns.group(1) != None:
                                        x = float(ns.group(1))
                                    if ns.group(4) != None:
                                        y = float(ns.group(4))
                                    if ns.group(7) != None:
                                        z = float(ns.group(7))
                                    mathdraw.add("glVertex3f(%.2f,%.2f,%.2f)"\
                                    %(x,y,z))
                            mathdraw.add("glEnd()")
                            mathdraw.add("glEnable(GL_LIGHTING)")
                    except:
                        self.cmdbuf = filename + ": no such file!"
                        return
                    self.cmdbuf = ""
                else:
                    self.cmdbuf = "Invaild arguments for drawball"
                    return
            else:
                self.cmdbuf = "Unrecognized command!"
                return
        else:
            self.cmdbuf = ""
                        
def name_to_frgb(name):
    try:
        [r,g,b] = name_to_rgb(name)
    except:
        [r,g,b] = [255,255,255]
    r = r/float(255)
    g = g/float(255)
    b = b/float(255)
    return [r,g,b]

def display():
    glClearColor(0,0,0,0)   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    for i in range(0,4):
        panel.draw(mathdraw)
    glutSwapBuffers()

def reshape(w,h):
    global winw, winh
    winw, winh = w, h
    mathdraw.setWinW(w)
    mathdraw.setWinH(h)

ball = ThreeDObject()
ball.addDraw("useMaterial(1.0,1.0,1.0,0.5,0.5)")
ball.addDraw("glutSolidSphere(0.1,10,10)")

cursor = ThreeDObject()
cursor.addChild([[[0.0,0.0,0.0],[0.0,0.0,1.0,0.0],[1.0,1.0,1.0]],ball])

panel = Panel()
mathdraw = MathDraw(winw,winh)
mathdraw.setBgColor(0.0,0.0,0.0,0.0)
mathdraw.back()
# mathdraw.add("drawquad(-2.0,-2.0,2.0,2.0,[0.0,0.0,1.0])")
mathdraw.mainp()
robot = Robot()
mathdraw.add("drawArrow([-3.0,0.0,0.0],[3.0,0.0,0.0],[1.0,0.0,0.0])")
mathdraw.add("drawArrow([0.0,-3.0,0.0],[0.0,3.0,0.0],[0.0,1.0,0.0])")
mathdraw.add("drawArrow([0.0,0.0,-3.0],[0.0,0.0,3.0],[0.0,0.0,1.0])")
mathdraw.add("drawCursor(self.objects[0].transform[0])")
# mathdraw.add("robot.draw()")
# mathdraw.add("glutSolidDodecahedron()")
# mathdraw.add("glutSolidIcosahedron()")
# mathdraw.add("glutSolidOctahedron ()")
# mathdraw.add("glutSolidRhombicDodecahedron()")
# mathdraw.add("glutSolidSierpinskiSponge(3,[0.0,0.0,0.0],1.0)")
# mathdraw.add("glutSolidTetrahedron()")
# mathdraw.add("useMaterial(1.0,0.0,0.0,0.5,0.5)")
# mathdraw.add("glutSolidTorus(0.5,1.5,20,20)")
mathdraw.addObject(cursor)
mathdraw.fore()
mathdraw.add("glColor3f(1.0,1.0,1.0)")
mathdraw.addString([mathdraw.foreground.left,mathdraw.foreground.bottom+0.05],\
                    panel.cmdbuf,[1.0,1.0,1.0])
mathdraw.addString([mathdraw.foreground.left,mathdraw.foreground.top - \
                    (mathdraw.foreground.top-mathdraw.foreground.bottom)/24],\
                    "",[1.0,1.0,1.0])

def keyboard(keyCode,x,y):
    panel.input(keyCode,mathdraw)
    glutPostRedisplay()

def special(keyCode,x,y):
    panel.special(keyCode,mathdraw)
    glutPostRedisplay()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(winw,winh)
glutCreateWindow('interactive')
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special)
glutMainLoop()
