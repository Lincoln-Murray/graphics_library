import math
import random

half_height, half_width = 1,1

def random_colour():
    hexlen = 0
    while hexlen != 7:
        random_number = random.randint(0, 16777215)
        hex_number = '#' + format(random_number, 'x')
        hexlen = len(hex_number)
    return hex_number

def dim_colour(colour, scale_factor, _gl):
    _r, _g, _b = _gl.r, _gl.g, _gl.b
    hex_colour = colour[1:]
    r, g, b = int(hex_colour[:2], 16), int(hex_colour[2:4], 16), int(hex_colour[4:], 16)
    r = max(0, min(255, int(r * scale_factor*_r)))
    g = max(0, min(255, int(g * scale_factor*_g)))
    b = max(0, min(255, int(b * scale_factor*_b)))
    return '#%02x%02x%02x' % (r,g,b)

def load_mtl(file_name):
    file = open(file_name, "rt")
    materials = {}
    current_name = None
    current_material = []
    for line in file:
        if "newmtl" in line:
            if current_name != None:
                materials[current_name] = current_material
            current_name = line.split()[-1]
            current_material = []
        elif 'Ka' in line:
            split = line.split()
            if len(split[1]) >1:
                if split[1][0] == '-' and split[1][1] == '0' and len(split[1]) == 2:
                    split[1] = '0'
                else:
                    while split[1][-1] == '0' or split[1][-1] == '.':
                        if split[1][-1] == '.':
                            split[1] = split[1][:-1]
                            break
                        else:
                            split[1] = split[1][:-1]
            if len(split[2]) >1:
                if split[2][0] == '-' and split[2][1] == '0' and len(split[2]) == 2:
                    split[2] = '0'
                else:
                    while split[2][-1] == '0' or split[2][-1] == '.':
                        if split[2][-1] == '.':
                            split[2] = split[2][:-1]
                            break
                        else:
                            split[2] = split[2][:-1]
            if len(split[3]) >1:
                if split[3][0] == '-' and split[3][1] == '0' and len(split[3]) == 2:
                    split[3] = '0'
                else:
                    while split[3][-1] == '0' or split[3][-1] == '.':
                        if split[3][-1] == '.':
                            split[3] = split[3][:-1]
                            break
                        else:
                            split[3] = split[3][:-1]
            current_material.append('#%02x%02x%02x' % (int(float(split[1])*255), int(float(split[2])*255), int(float(split[3])*255)))
    if current_name != None:
        materials[current_name] = current_material
    return materials

def get_normal_from_triangle(x1,y1,z1,x2,y2,z2,x3,y3,z3):
    lx1, ly1, lz1 = x2 - x1, y2 - y1, z2 - z1
    lx2, ly2, lz2 = x3 - x1, y3 - y1, z3 - z1
    nx,ny,nz = ly1 * lz2 - lz1 * ly2, lz1 * lx2 - lx1 * lz2, lx1 * ly2 - ly1 * lx2
    normal_length = (nx*nx+ny*ny+nz*nz)**0.5
    if normal_length == 0:
        return 0,0,0
    else:
        return nx/normal_length, ny/normal_length, nz/normal_length

def render_wall_from_normalised_points(x1_3d,y1_3d,z1_3d,x2_3d,y2_3d,z2_3d,x3_3d,y3_3d,z3_3d,colour,_gl):
    global half_width, half_height
    if not _gl.wiremesh:
        nx,ny,nz = get_normal_from_triangle(x1_3d,y1_3d,z1_3d,x2_3d,y2_3d,z2_3d,x3_3d,y3_3d,z3_3d)
        if nz <= 0:
            colour = dim_colour(colour,-nz,_gl)
    else:
        nz = -1
        colour = ''
    _outline = _gl.outline

    if nz <=0:
        x1_2d = x1_3d*half_width+half_width
        y1_2d = y1_3d*half_height+half_height
        x2_2d = x2_3d*half_width+half_width
        y2_2d = y2_3d*half_height+half_height
        x3_2d = x3_3d*half_width+half_width
        y3_2d = y3_3d*half_height+half_height
        z_list = [z1_3d, z2_3d, z3_3d]
        z_list.sort(reverse=True)
        return [int(x1_2d),int(y1_2d),int(x2_2d),int(y2_2d),int(x3_2d),int(y3_2d),z_list[0],_outline,colour]

def rotate_point(axisone,axistwo,raxis, angle):
    raxisone = axisone * math.cos(angle) - axistwo * math.sin(angle)
    raxistwo = axisone * math.sin(angle) + axistwo * math.cos(angle)
    return raxisone,raxistwo,raxis

def scale_point(x,y,z, zfar, znear, fov, ar, camera_x, camera_y, camera_z ,camera_angle_x, camera_angle_y, camera_angle_z):
    x,y,z = rotate_point(x,y,z, camera_angle_z)
    x,y,z = rotate_point(z,x,y, camera_angle_y)
    x,y,z = rotate_point(y,z,x, camera_angle_x)
    x,y,z = camera_x+x,camera_y+y,camera_z+z
    if z != 0:
        x = (ar*(1/math.tan(fov/2))*x)/z
        y = ((1/math.tan(fov/2))*y)/z
        z = z*(zfar/(zfar-znear))-((zfar*znear)/(zfar-znear))
    return [x,y,z]

class gl:
    map_array = []    
    def __init__(self, _width = 1920, _height = 1080, _fov = 55, _zfar = 1000, _znear = 0.1):
        if _fov >= 180:
            _fov = math.radians(55)
        else:
            _fov = math.radians(_fov)
        global half_width, half_height
        self.camera_x, self.camera_y, self.camera_z = 0,0,0
        self.camera_angle_x, self.camera_angle_y, self.camera_angle_z = 0,0,0
        self.ar = int(_height)/int(_width)
        half_width, half_height = int(_width/2), int(_height/2)
        self.zfar, self.znear, self.fov = _zfar, _znear, _fov
        self.width = _width
        self.height = _height
        self.wiremesh = False
        self.r, self.g, self.b = 1,1,1
        self.background_colour = '#000000'
        self.outline = ''

    def camera_absolute(self, _camera_x = None, _camera_y = None, _camera_z = None, _camera_angle_x = None, _camera_angle_y = None, _camera_angle_z = None):
        if _camera_x != None:
            self.camera_x = _camera_x
        if _camera_y != None:
            self.camera_y = _camera_y
        if _camera_z != None:
            self.camera_z = _camera_z
        if _camera_angle_x != None:
            self.camera_angle_x = math.radians(_camera_angle_x)
        if _camera_angle_y != None:
            self.camera_angle_y = math.radians(_camera_angle_y)
        if _camera_angle_z != None:
            self.camera_angle_z = math.radians(_camera_angle_z)

    def move_camera(self, _camera_x = 0, _camera_y = 0, _camera_z = 0, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0):
        self.camera_z += math.cos(self.camera_angle_y) * _camera_z
        self.camera_x += math.sin(self.camera_angle_y) * _camera_z
        self.camera_x += math.cos(self.camera_angle_y) * _camera_x
        self.camera_z += math.sin(self.camera_angle_y) * _camera_x
        self.camera_y += _camera_y
        
        self.camera_angle_x, self.camera_angle_y, self.camera_angle_z = self.camera_angle_x + math.radians(_camera_angle_x), self.camera_angle_y + math.radians(_camera_angle_y), self.camera_angle_z + math.radians(_camera_angle_z)

    def view_style(self, _wiremesh = False, _r = 1, _g = 1, _b = 1, _background_colour = '', _background_brightness = 0.4, outline_colour = ''):
        if _background_colour == '':
            r = max(0, min(255, int(_background_brightness*_r*255)))
            g = max(0, min(255, int(_background_brightness*_g*255)))
            b = max(0, min(255, int(_background_brightness*_b*255)))
            self.background_colour = '#%02x%02x%02x' % (r,g,b)
        else:
            self.background_colour = _background_colour
        self.r, self.g, self.b = _r, _g, _b
        self.wiremesh = _wiremesh
        self.outline = outline_colour

    def new_frame(self):
        frame = []
        
        for model in self.map_array:
            for wall_num in range(0,len(model)):
                wall = model[wall_num]
                for point in range(0,len(wall)-1):
                    locals()["sp" + str(point) + str(wall_num)] = scale_point(wall[point][0],wall[point][1],wall[point][2], self.zfar, self.znear, self.fov, self.ar, self.camera_x, self.camera_y, self.camera_z , self.camera_angle_x, self.camera_angle_y, self.camera_angle_z)
                temp_tri = render_wall_from_normalised_points(locals()["sp0"+ str(wall_num)][0],locals()["sp0"+ str(wall_num)][1],locals()["sp0"+ str(wall_num)][2],locals()["sp1"+ str(wall_num)][0],locals()["sp1"+ str(wall_num)][1],locals()["sp1"+ str(wall_num)][2],locals()["sp2"+ str(wall_num)][0],locals()["sp2"+ str(wall_num)][1],locals()["sp2"+ str(wall_num)][2],wall[len(wall)-1], self)
                if temp_tri != None:
                    frame.append(temp_tri)
                    print(temp_tri)
        frame.sort(key=lambda l : l[6], reverse= True)
        return frame

    def render_image(self, output_location = "images/output", file_format = '.svg', _line_thickness = 1):
        output = open(output_location + file_format, 'w')
        if file_format == '.svg':
            intro_string = '''<svg version="1.1" width="'''+str(self.width)+'''" height="'''+str(self.height)+'''" xmlns="http://www.w3.org/2000/svg">
                <rect width="100%" height="100%" fill="'''+self.background_colour+'''" />
            '''
            output.write(intro_string)
            triangles = self.new_frame()

            for tri in triangles:
                if tri[-2] == '':
                    tri[-2] = tri[-1]
                output.write('  <polygon points="'+str(tri[0])+' '+str(tri[1])+' '+str(tri[2])+' '+str(tri[3])+' '+str(tri[4])+' '+str(tri[5])+' " stroke="'+tri[-2]+'" fill="'+tri[-1]+'" stroke-width="'+str(_line_thickness)+'"/>\n')

            output.write('</svg>')
        output.close()

class object(gl):
    def __init__(self, _model, x = 0, y = 0 , z = 0, ax = 0, ay = 0, az = 0, scale_x = 1, scale_y = 1, scale_z = 1,colour = None):
        ax, ay, az = math.radians(ax), math.radians(ay), math.radians(az)
        model = open(_model, 'rt')
        self.object_array = []
        if _model[-4:] == '.obj':
            count = 0
            current_material = None
            materials = load_mtl(_model[:-3]+ 'mtl')
            for line in model:
                if line == '\n':
                    pass
                elif line[0] == 'v' and line[1] == ' ':
                    count+=1
                    split = line.split()
                    if len(split[1]) >1:
                        if split[1][0] == '-' and split[1][1] == '0' and len(split[1]) == 2:
                            split[1] = '0'
                        else:
                            while split[1][-1] == '0' or split[1][-1] == '.':
                                if split[1][-1] == '.':
                                    split[1] = split[1][:-1]
                                    break
                                else:
                                    split[1] = split[1][:-1]
                    if len(split[2]) >1:
                        if split[2][0] == '-' and split[2][1] == '0' and len(split[2]) == 2:
                            split[2] = '0'
                        else:
                            while split[2][-1] == '0' or split[2][-1] == '.':
                                if split[2][-1] == '.':
                                    split[2] = split[2][:-1]
                                    break
                                else:
                                    split[2] = split[2][:-1]
                    if len(split[3]) >1:
                        if split[3][0] == '-' and split[3][1] == '0' and len(split[3]) == 2:
                            split[3] = '0'
                        else:
                            while split[3][-1] == '0' or split[3][-1] == '.':
                                if split[3][-1] == '.':
                                    split[3] = split[3][:-1]
                                    break
                                else:
                                    split[3] = split[3][:-1]
                    split[1], split[2], split[3] = rotate_point(float(split[1]), float(split[2]), float(split[3]), az)
                    split[1], split[2], split[3] = rotate_point(float(split[3]), float(split[1]), float(split[2]), ay)
                    split[1], split[2], split[3] = rotate_point(float(split[2]), float(split[3]), float(split[1]), ax)
                    locals()["v"+str(count)] = [float(split[1]*scale_x) + x, float(split[2]*scale_y) - y, float(split[3]*scale_z) + z]
                elif line[0] == 'f' and line[1] == ' ':
                    split = line.split()
                    for i in range(0, len(split)):
                        pos = 0
                        v, vt, vn = '', '', ''
                        for q in range(0, len(split[i])):
                            if i != 0:
                                char = split[i][q]
                                if char == '/':
                                    pos += 1
                                else:
                                    if pos == 0:
                                        v += char
                                    elif pos == 1:
                                        vt += char
                                    elif pos == 2:
                                        vn += char
                        if i != 0:
                            locals()["fv" + str(i)] = locals()["v"+str(v)]
                    if colour == None and current_material == None:
                        new_colour = random_colour()
                    else:
                        if colour != None:
                            new_colour = colour
                        else:
                            new_colour = current_material[0]
                    for p in range(2,len(split)-1):
                        self.object_array.append([locals()["fv1"], locals()["fv"+str(p)], locals()["fv"+str(p+1)], new_colour])
                elif line.split()[0] == 'usemtl':
                    current_material = materials[line.split()[1]]
        elif _model[-4:] == '.stl':
                if model.read()[:5] == 'solid':
                    ascii_stl = True
                else:
                    ascii_stl = False
                face = []
                if ascii_stl:
                    model = open(_model, 'rt')
                    for line in model:
                        split = line.split()
                        if split[0] == 'outer':
                            face = []
                        if split[0] == 'vertex':
                            split[1], split[2], split[3] = rotate_point(float(split[1]), float(split[2]), float(split[3]), az)
                            split[1], split[2], split[3] = rotate_point(float(split[3]), float(split[1]), float(split[2]), ay)
                            split[1], split[2], split[3] = rotate_point(float(split[2]), float(split[3]), float(split[1]), ax)
                            face.append([float(split[1]*scale_x) + x, float(split[2]*scale_y) - y, float(split[3]*scale_z) + z])
                        if split[0] == 'endloop':
                            face.append(random_colour())
                            self.object_array.append(face)
                            face = []
                else:
                    model = open(_model, 'rb')
                    byte_array = bytearray(model.read())
                    bytenum = 0
                    var_temp = None
                    temp = None
                    temp_2 = None
                    temp_vertex = []
                    tri = []
                    new_tri = True
                    for byte in byte_array:
                        bytenum +=1
                        if bytenum < 81:
                            pass
                        elif bytenum >= 81 and bytenum <=84:
                            if bytenum == 81:
                                var_temp = int(byte).to_bytes()
                            elif bytenum == 82 or bytenum == 83 or bytenum == 84:
                                var_temp = int(byte).to_bytes() + var_temp
                            if bytenum == 84:
                                tri_count = int.from_bytes(var_temp)
                        elif ((bytenum-85) % 50) == 0:
                            new_tri = True
                            var_temp = None
                            temp = 0
                            temp_2 = 0
                            temp_vertex = []
                            tri = []
                            new_tri = True
                        elif new_tri:
                            temp += 1
                            if temp == 12:
                                new_tri = False
                                temp = 0
                                temp_2 = 0
                        else:
                            temp+=1
                            if temp == 1 or temp == 5 or temp == 9:
                                var_temp = int(byte).to_bytes()
                            else:
                                var_temp = int(byte).to_bytes() + var_temp
                            if temp == 4 or temp == 8 or temp == 12:
                                temp_vertex.append(int.from_bytes(var_temp, signed = True))
                            if temp == 12:
                                temp = 0
                                temp_2+=1
                                temp_vertex[0], temp_vertex[1], temp_vertex[2] = rotate_point(float(temp_vertex[0]), float(temp_vertex[1]), float(temp_vertex[2]), az)
                                temp_vertex[0], temp_vertex[1], temp_vertex[2] = rotate_point(float(temp_vertex[2]), float(temp_vertex[0]), float(temp_vertex[1]), ay)
                                temp_vertex[0], temp_vertex[1], temp_vertex[2] = rotate_point(float(temp_vertex[1]), float(temp_vertex[2]), float(temp_vertex[0]), ax)
                                tri.append([float(temp_vertex[0]*scale_x) + x, float(temp_vertex[1]*scale_y) - y, float(temp_vertex[2]*scale_z) + z])
                                temp_vertex = []
                            if temp_2 == 3 and temp == 0:
                                tri = [tri[2], tri[1], tri[0]]
                                tri.append(random_colour())
                                self.object_array.append(tri)
                                tri = []
        super().map_array.append(self.object_array)
        self.map_position = super().map_array.index(self.object_array)

#    def translate_absolute(self, _gl, _x=0, _y=0, _z=0, _angle_x=0, _angle_y=0, _angle_z=0):
#        _angle_x, _angle_y, _angle_z = math.radians(_angle_x), math.radians(_angle_y), math.radians(_angle_z)
#        new_object_array = []
#        for tri in self.object_array:
#            new_tri = []
#            print(tri)
#            for point in tri:
#                print(point)
#                if point != tri[-1]:
#                    x, y, z = point[0], point[1], point[2]
#                    x, y, z = rotate_point(x, y, z, _angle_z)
#                    z, x, y = rotate_point(z, x, y, _angle_y)
#                    y, z, x = rotate_point(y, z, x, _angle_x)
#                    point[0], point[1], point[2] = x+_x, y-_y, z+_z
#                new_tri.append(point)
#            print("\n")
#            new_object_array.append(new_tri)
#        print("\n\n\n\n")
#        self.object_array = new_object_array
#        del _gl.map_array[self.map_position]
#        _gl.map_array.append(self.object_array)
#        self.map_position = _gl.map_array.index(self.object_array)

#    def set_properties(self, _gl, x = 0, y = 0 , z = 0, ax = 0, ay = 0, az = 0, colour = None):
#        ax, ay, az = math.radians(ax), math.radians(ay), math.radians(az)
#        count = 0
#        new_object_array = []
#        for tri in self.object_array:
#            new_tri = []
#            for vertice in tri:
#                if vertice != tri[-1]:
#                    split = [0,vertice[0],vertice[1],vertice[2]]
#                    split[1], split[2], split[3] = rotate_point(float(split[1]), float(split[2]), float(split[3]), az)
#                    split[1], split[2], split[3] = rotate_point(float(split[3]), float(split[1]), float(split[2]), ay)
#                    split[1], split[2], split[3] = rotate_point(float(split[2]), float(split[3]), float(split[1]), ax)
#                    new_tri.append([float(split[1]) + x, float(split[2]) - y, float(split[3]) + z,tri[-1]])
#            new_object_array.append(new_tri)
#        self.object_array = new_object_array
#        print(self.object_array)
#        print('\n\n\n\n')
#        del _gl.map_array[self.map_position]
#        _gl.map_array.append(self.object_array)
#        self.map_position = _gl.map_array.index(self.object_array)