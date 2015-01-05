from math import sin,cos

with open("data","w") as f:
    for i in range(0,200):
        t = i*0.02 - 2
        x = cos(t)
        y = sin(t)
        z = t
        f.write("%.2f %.2f %.2f\n"%(x,y,z))
