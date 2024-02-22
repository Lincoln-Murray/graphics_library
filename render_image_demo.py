import Main
import math
model = 'models/teapot.obj'
model_2 = 'models/cube.obj'

renderer = Main.gl(1920,1080, 55, 1000, 0.1)
teapot_1 = Main.object(model,-4.5,-1,0,0,45,180, 1, 1, 1, None)
teapot_2 = Main.object(model,4.5,-1,0,0,315,180, 1, 1, 1, None)
cube = Main.object(model_2,0,0,0,0,35,0, 1, 1, 1, None)

background_colour = '#000000'

ar = int(renderer.height)/int(renderer.width)
renderer.camera_absolute(_camera_x = 0, _camera_y = 0, _camera_z = 10, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0)




output = open("images/output.svg", 'w')
renderer.view_style(False, 1, 1, 1)
intro_string = '''<svg version="1.1" width="'''+str(renderer.width)+'''" height="'''+str(renderer.height)+'''" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="'''+background_colour+'''" />
'''
output.write(intro_string)
triangles = renderer.new_frame()

for tri in triangles:
    if tri[-2] == '':
        tri[-2] = tri[-1]
    output.write('  <polygon points="'+str(tri[0])+' '+str(tri[1])+' '+str(tri[2])+' '+str(tri[3])+' '+str(tri[4])+' '+str(tri[5])+' " stroke="'+tri[-2]+'" fill="'+tri[-1]+'" stroke-width="5"/>\n')

output.write('</svg>')
output.close()