#library imports
import Main
import rasteriser

#init the models and library class instances
model = 'models/cube.stl'
model_2 = 'models/teapot.obj'

renderer = Main.gl(1920,1080, 55, 1000, 0.1)
#cube = Main.object(renderer, model,0,0,1,0,35,0, 0.0000001, 0.0000001, 0.0000001, None)
cube = Main.object(renderer, model_2,0,-2.5,0,180,0,38, 2, 2, 2, None)

renderer.camera_absolute(_camera_x = 0, _camera_y = 0, _camera_z = 10, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0)

light1 = Main.light(renderer, -10,-10,-10, 1,1,1)

renderer.view_style(False, 0.1, '')

rast = rasteriser.rasteriser(1080, 1920)
triangles = renderer.new_frame()
for tri in triangles:
    rast.draw_triangle(triangle=[tri[0], tri[1], tri[2], tri[3], tri[4], tri[5]], colour=tri[-1])


with open("text.bmp", "wb") as test:
    string = '424D'
    size = 1920*1080*4+54
    hsize = size.to_bytes(4,'little')
    string = bytearray.fromhex(string)
    for byte in hsize: string.append(byte)
    for byte in bytearray.fromhex('000000003600000028000000'): string.append(byte)
    for byte in int(1920).to_bytes(4,'little'): string.append(byte)
    for byte in int(1080).to_bytes(4,'little'): string.append(byte)
    for byte in bytearray.fromhex('0100180000000000'): string.append(byte)
    for byte in int(1920*1080*4).to_bytes(4,'little'): string.append(byte)
    for byte in bytearray.fromhex('130B0000'): string.append(byte)
    for byte in bytearray.fromhex('130B0000'): string.append(byte)
    for byte in bytearray.fromhex('00000000'): string.append(byte)
    for byte in bytearray.fromhex('00000000'): string.append(byte)
    count = 0
    for byte in string:
        test.write(byte.to_bytes())
    for x in reversed(rast.image_pixels):
        for y in x:
            y = y[1:]
            new_y = y[4] + y[5] + y[2] + y[3] + y[0] +y[1]
            for byte in bytearray.fromhex(new_y):
                test.write(byte.to_bytes())        
