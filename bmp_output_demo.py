#library imports
import Main
import rasteriser

#init the models and library class instances
model = 'models/cube.stl'
model_2 = 'models/cube.obj'

renderer = Main.gl(1920,1080, 55, 1000, 0.1)
cube = Main.object(renderer, model,0,0,1,0,35,0, 0.0000001, 0.0000001, 0.0000001, None)
cube = Main.object(renderer, model_2,-3,0,1,0,35,0, 0.5, 0.5, 0.5, None)

renderer.camera_absolute(_camera_x = 0, _camera_y = 0, _camera_z = 10, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0)

light1 = Main.light(renderer, -10,-10,-10, 1,1,1)

renderer.view_style(False, 0.1, '')

rast = rasteriser.rasteriser(100, 100)
triangles = renderer.new_frame()
#for tri in triangles:
#    print(tri)
#    rast.draw_triangle(triangle=[tri[0], tri[1], tri[2], tri[3], tri[4], tri[5]], colour=tri[-1])
rast.draw_triangle(triangle=[30, 10, 10, 40, 40, 40], colour='#FF0000')

from PIL import Image
import sys

def save_pixels_to_bmp(pixel_list, width, height, mode, output_file):
    """
    Save a list of pixel values to a BMP file.

    Args:
        pixel_list (list/tuple): Flat list of pixel values.
                                 - For 'L' mode: one value per pixel (0-255)
                                 - For 'RGB' mode: triplets (R, G, B) per pixel
        width (int): Image width in pixels.
        height (int): Image height in pixels.
        mode (str): 'L' for grayscale, 'RGB' for color.
        output_file (str): Path to save BMP file.
    """
    try:
        # Validate mode
        if mode not in ('L', 'RGB'):
            raise ValueError("Mode must be 'L' (grayscale) or 'RGB' (color).")

        # Validate pixel count
        expected_len = width * height
        if len(pixel_list) != expected_len:
            raise ValueError(f"Pixel list length {len(pixel_list)} does not match "
                             f"expected size {expected_len} for {width}x{height} {mode} image.")

        # Create image from pixel data
        img = Image.new(mode, (width, height))
        img.putdata(pixel_list)

        # Save as BMP
        img.save(output_file, format='BMP')
        print(f"Image saved successfully as {output_file}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

pixels = []
for x in range(len(rast.image_pixels)):
    for y in range(len(rast.image_pixels[x])):
        pixels.append(tuple(int(rast.image_pixels[x][y][1:][i:i+2], 16) for i in (0, 2, 4)))
save_pixels_to_bmp(pixels, 100, 100, 'RGB', 'grayscale.bmp')

'''
with open("text.bmp", "wb") as test:
    string = '424D'
    size = 1920*1080*4+54
    #print(size)
    hsize = size.to_bytes(4,'little')
    #print(hsize)
    #hsize = hsize[1:] + hsize[0].to_bytes()
    #for byte in hsize: #print(byte)
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
    for x in rast.image_pixels:
        for y in x:
            count += 1
            y = y[1:]
            new_y = y[4] + y[5] + y[2] + y[3] + y[0] +y[1]
            for byte in bytearray.fromhex('FFFFFF'):
                test.write(byte.to_bytes())
                if count == 2:
                    count = 0
                    for pad_byte in bytearray.fromhex('0000'): test.write(pad_byte.to_bytes())
'''