import Main
import math
from tkinter.ttk import *
from tkinter import *

model = 'models/cube.obj'

cube = Main.object(model,0,0,-10,45,45, 0, None)
renderer = Main.gl(1920,1080, math.radians(55), 1000, 0.1)
renderer.map_array.append(cube.get_object())
speed = -0.4
hwstr = str(renderer.width) + 'x' + str(renderer.height)
ar = int(renderer.height)/int(renderer.width)
renderer.camera_angle_y = math.pi
#init the window and viewport
master = Tk()
master.geometry(hwstr)
master.title("Cube demo")

frame = Frame(master, width=renderer.width, height=renderer.height, bg="black")
frame.focus_set()
frame.pack(anchor=SW, side=LEFT)
viewport = Canvas(frame, width=renderer.width, height=renderer.height)
viewport.pack(side=TOP)

def loop():
    viewport.create_rectangle(0,0,renderer.width,renderer.height, fill="white")
    triangles = renderer.new_frame()
    #renderer.move_camera(_camera_z = 0)
    for i in range(0,len(triangles)-1):
        points = [triangles[i][0], triangles[i][1], triangles[i][2], triangles[i][3], triangles[i][4], triangles[i][5]]
        viewport.create_polygon(points, fill=triangles[i][-1])
    master.after(50,loop)

master.after(1,loop)
master.mainloop()