import Main
model = 'models/teapot.obj'
model_2 = 'models/cube.obj'

renderer = Main.gl(1920,1080, 55, 1000, 0.1)
teapot_1 = Main.object(model,-4.5,-1,0,0,45,180, 1, 1, 1, None)
teapot_2 = Main.object(model,4.5,-1,0,0,315,180, 1, 1, 1, None)
cube = Main.object(model_2,0,0,0,0,35,0, 1, 1, 1, None)

renderer.camera_absolute(_camera_x = 0, _camera_y = 0, _camera_z = 10, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0)
renderer.view_style(False, 1, 1, 1, '', 0.2)


renderer.render_image("images/output", ".svg", 1)