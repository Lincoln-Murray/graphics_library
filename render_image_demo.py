#import library
import Main

#create variables
model = 'models/teapot.obj'
model_2 = 'models/cube.obj'

#create instances from the library
renderer = Main.gl(1920,1080, 55, 1000, 0.1)
teapot_1 = Main.object(renderer, model,-4.5,-1,0,0,45,180, 1, 1, 1, '#FF0000')
teapot_2 = Main.object(renderer, model,4.5,-1,0,0,315,180, 1, 1, 1, '#0000FF')
cube = Main.object(renderer, model_2,0,0,0,0,35,0, 1, 1, 1, '#00FF00')
light1 = Main.light(renderer, 0, 0, 10, 1, 1, 1)

#set attributes
renderer.camera_absolute(_camera_x = 0, _camera_y = 0, _camera_z = 10, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0)
renderer.view_style(False, 0, '')

#render the image at the desired path
renderer.render_image("images/output", ".svg", 1)