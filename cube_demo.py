#library imports
import Main
from tkinter.ttk import *
from tkinter import *
import time

#init the models and library class instances
model = 'models/cube.stl'
model_2 = 'models/cube.obj'

renderer = Main.gl(1920,1080, 55, 1000, 0.1)
cube = Main.object(model,0,0,1,0,35,0, 0.0000001, 0.0000001, 0.0000001, None)
cube = Main.object(model_2,-3,0,1,0,35,0, 0.5, 0.5, 0.5, None)

renderer.camera_absolute(_camera_x = 0, _camera_y = 0, _camera_z = 10, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0)

light1 = Main.light(-10,-10,-10, 1,1,1)

#init the window and viewport
master = Tk()
master.geometry(str(renderer.width) + 'x' + str(renderer.height))
master.title("Graphics Library: cube demo")

frame = Frame(master, width = renderer.width, height=renderer.height, bg="black")
frame.focus_set()
frame.pack(anchor=SW, side=LEFT)
viewport = Canvas(frame, width=renderer.width, height=renderer.height)
viewport.pack(side=TOP)

renderer.view_style(False, 0.1, '')

#main loop
def loop():
    start = time.time()
    viewport.create_rectangle(0,0,renderer.width,renderer.height, fill=renderer.background_colour)
    triangles = renderer.new_frame()
    renderer.move_camera(_camera_angle_z = 1, _camera_angle_y=2)
    for tri in triangles:
        viewport.create_polygon([tri[0], tri[1], tri[2], tri[3], tri[4], tri[5]],outline=tri[-2], fill=tri[-1])
    frame_time = int((time.time() - start)*1000)
    if frame_time < 50:
        master.after(50-frame_time,loop)
    else:
        master.after(1,loop)

#call the loop
master.after(1,loop)
master.mainloop()
