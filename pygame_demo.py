#library imports
import Main
import pygame as pg
import time

start = time.time()

#init the models and library class instances
model = 'models/teapot.obj'
model_2 = 'models/cube.obj'

renderer = Main.gl(1920,1080, 55, 1000, 0.1)
teapot_1 = Main.object(renderer, model,-4.5,-1,0,0,45,180, 1, 1, 1, '#FF0000')
teapot_2 = Main.object(renderer, model,4.5,-1,0,0,315,180, 1, 1, 1, '#0000FF')
cube = Main.object(renderer, model_2,0,0,0,0,35,0, 1, 1, 1, '#00FF00')
light1 = Main.light(renderer, 0, 0, 10, 1, 1, 1)

renderer.camera_absolute(_camera_x = 0, _camera_y = 0, _camera_z = 10, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0)

light1 = Main.light(renderer, -10,-10,-10, 1,1,1)

#init the window and viewport
pg.init()

screen = pg.display.set_mode((renderer.width, renderer.height))
pg.display.set_caption("Graphics Library: cube demo")

renderer.view_style(False, 0.1, '')

clock = pg.time.Clock()
while 1:
    screen.fill((0,0,0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    pg.display.set_caption(f"Graphics Library: cube demo - FPS: {clock.get_fps()}")

    triangles = renderer.new_frame()
    renderer.move_camera(_camera_angle_z = 1, _camera_angle_y=2)

    for tri in triangles:
        pg.draw.polygon(screen, (tri[-1]), [(tri[0], tri[1]), (tri[2], tri[3]), (tri[4], tri[5])])

    if time.time() - start > 10: exit()

    clock.tick(60)
    pg.display.flip()
