import Main
import math
from tkinter.ttk import *
from tkinter import *

model = 'models/teapot.obj'
model_2 = 'models/cube.obj'

renderer = Main.gl(1920,1080, math.radians(55), 1000, 0.1)
cube = Main.object(renderer,model,-4.5,-1,0,0,45,180, 1, 1, 1, None)
bcube = Main.object(renderer,model,4.5,-1,0,0,315,180, 1, 1, 1, None)
ccube = Main.object(renderer,model_2,0,0,0,0,35,0, 1, 1, 1, None)

speed = -0.4
hwstr = str(renderer.width) + 'x' + str(renderer.height)
ar = int(renderer.height)/int(renderer.width)
renderer.camera_absolute(_camera_x = 0, _camera_y = 0, _camera_z = 10, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0)


#init the window and viewport
master = Tk()
master.geometry(hwstr)
master.title("Cube demo")

frame = Frame(master, width = renderer.width, height=renderer.height, bg="black")
frame.focus_set()
frame.pack(anchor=SW, side=LEFT)
viewport = Canvas(frame, width=renderer.width, height=renderer.height)
viewport.pack(side=TOP)

renderer.view_style(False)

def loop():
    viewport.create_rectangle(0,0,renderer.width,renderer.height, fill="black")
    triangles = renderer.new_frame()

    #renderer.move_camera(_camera_angle_z = 0, _camera_angle_y=2)
    for tri in triangles:
        viewport.create_polygon([tri[0], tri[1], tri[2], tri[3], tri[4], tri[5]],outline=tri[-2], fill=tri[-1])
    #master.after(50,loop)

master.after(1,loop)
master.mainloop()
