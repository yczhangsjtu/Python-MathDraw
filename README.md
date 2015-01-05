Python-MathDraw
===============

PyOpenGL implementation of a vim-like 3d drawing program.

Three layers of scene: Background, 3d part, foreground.

A pointer identifying which scene is currently being operated by the command.

The normal mode and command mode are just like vim. There is no edit mode or visual mode.

The four views are 3d, front, left, top. By default the view mode is all.

There is a Panel class that is responsible for accepting the input from user, and record the state. Each time it changes state it exerts the change on an instance of the MathDraw class, and the MathDraw class is responsible for drawing.

A cursor is maintained by the Panel, and any drawing will be locatedat the cursor.

The MathDraw class maintains several list of PyOpenGL statements for drawing. In the "display" callback function it just execute(eval) these statements. And a draw command draw another object simply by adding the corresponding PyOpenGL statements. 

Currently supported commands:

These are prefixed by ":"

back/b: set scene pointer to background

main/m: set scene pointer to 3d part

fore/f: set scene pointer to foreground

quit/q: quit the program

cursor/c [x,y,z]: set the location of the cursor, and if no argument, print the location of cursor

all/a: set view to be all, when all views are shown

td: set view to be 3d

front/fr: set view to be front

left/l: set view to be left

top/t: set view to be top

setcolor/sc colorname/r,g,b: set the current color

setnolight/snl: turn off the light

setlight/sl [x,y,z]: turn on the light/set location of light

drawball/db r: draw a ball of radius r

drawcube/dc l,w,h: draw a cube of length,width,height l,w,h

curve/cv datafile: read data from file and draw a curve

These are commands carried out instantly

a: rotate the camera to left

d: rotate the camera to right

w: raise the camera

s: lower the camera

q: camera farther

e: camera closer

hjkl: move cursor, the direction is dependent on the view mode such that the movement direction coincides with the vim. In all view mode the movement is identical to that in top mode.

ui: move cursor along the z direction no matter the view mode
