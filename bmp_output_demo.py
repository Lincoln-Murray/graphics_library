#library imports
import Main
import rasteriser
import bmp_writer

#init the models and library class instances
model = 'models/cube.stl'
model_2 = 'models/teapot.obj'

renderer = Main.gl(1920,1080, 55, 1000, 0.1)
#cube = Main.object(renderer, model,0,0,1,0,35,0, 0.0000001, 0.0000001, 0.0000001, None)
cube = Main.object(renderer, model_2,0,-3.5,0,180,80,0, 2, 2, 2, None)

renderer.camera_absolute(_camera_x = 0, _camera_y = 0, _camera_z = 10, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0)

light1 = Main.light(renderer, 1,0,1, 1,1,1)

renderer.view_style(False, 0.1, '')

rast = rasteriser.rasteriser(1080, 1920)
triangles = renderer.new_frame()
for tri in triangles:
    rast.draw_triangle(triangle=[tri[0], tri[1], tri[2], tri[3], tri[4], tri[5]], colour=tri[-1])

bmp_writer.write_bmp('demo', 1920, 1080, rast.image_pixels) 
