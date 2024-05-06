#library imports
import math
import random
import string
from typing import Tuple, List

#global variables
half_height, half_width = 1,1

# convert (r,g,b) to hex
def _rgb_to_hex(rgb_colour: Tuple[int] | List[int]) -> string:
    return '#%02x%02x%02x' % (rgb_colour[0], rgb_colour[1], rgb_colour[2])

# convert hex to (r,g,b)
def _hex_to_rgb(hexidecimal: str) -> Tuple[int]:
    return int(hexidecimal[1:3], 16), int(hexidecimal[3:5], 16), int(hexidecimal[5:7], 16)

#generates a random hexedecimal colour string in the format '#000000'
def random_colour() -> string:
    hexlen = 0
    while hexlen != 7:
        random_number = random.randint(0, 16777215)
        hex_number = '#' + format(random_number, 'x')
        hexlen = len(hex_number)
    return hex_number

def dim_colour(colour, scale_factor, light_attributes) -> Tuple[int]:
    _r, _g, _b = light_attributes[3], light_attributes[4], light_attributes[5]

    r, g, b = colour
    r = max(0, min(255, int(r * scale_factor*_r)))
    g = max(0, min(255, int(g * scale_factor*_g)))
    b = max(0, min(255, int(b * scale_factor*_b)))

    return (r, g, b)

#averages rgb colours from a list in the format 'r, g, b'
def average_colour(colour_list) -> Tuple[int]:
    r, g, b = 0,0,0

    for count, colour in enumerate(colour_list):
        r, g, b = r + colour[0], g + colour[1], b + colour[2]

    if count!=0:
        r, g, b = int(r/count), int(g/count), int(b/count)

    return (r, g, b)

#loads materials from a .mtl file
def load_mtl(file_name) -> list:
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

#calculates the normal of a triangle
def get_normal_from_triangle(x1,y1,z1,x2,y2,z2,x3,y3,z3):
    lx1, ly1, lz1 = x2 - x1, y2 - y1, z2 - z1
    lx2, ly2, lz2 = x3 - x1, y3 - y1, z3 - z1
    nx,ny,nz = ly1 * lz2 - lz1 * ly2, lz1 * lx2 - lx1 * lz2, lx1 * ly2 - ly1 * lx2
    normal_length = (nx*nx+ny*ny+nz*nz)**0.5
    if normal_length == 0:
        return 0,0,0
    else:
        return nx/normal_length, ny/normal_length, nz/normal_length

#scales polygon points and applies appropriate colouring to faces
def render_wall_from_normalised_points(x1_3d,y1_3d,z1_3d,x2_3d,y2_3d,z2_3d,x3_3d,y3_3d,z3_3d,colour,wiremesh,light_array,outline) -> list:
    global half_width, half_height

    if not wiremesh:
        nx,ny,nz = get_normal_from_triangle(x1_3d,y1_3d,z1_3d,x2_3d,y2_3d,z2_3d,x3_3d,y3_3d,z3_3d)
        if nz <= 0:
            colour_list = []
            for light in light_array:
                x,y,z = light[0], light[1], light[2]
                length = (x**2 + y**2 + z**2)**0.5                
                colour_x = dim_colour(colour,-nx*(x/length), light)
                colour_y = dim_colour(colour,-ny*(y/length), light)
                colour_z = dim_colour(colour,-nz*(z/length), light)
                colour_list.append(average_colour((colour_x, colour_y, colour_z)))
                pass
            colour = _rgb_to_hex(average_colour(colour_list))
    else:
        nz = -1
        colour = ''
    _outline = outline

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

#rotates a point around the raxis(rotation axis) by an angle in radians
def rotate_point(axisone,axistwo,raxis, angle):
    sin_angle = math.sin(angle)
    cos_angle = math.cos(angle)
    raxisone = axisone * cos_angle - axistwo * sin_angle
    raxistwo = axisone * sin_angle + axistwo * cos_angle
    return raxisone,raxistwo,raxis

#scales a point based on the specifications of the camera(fov, location, angle, min and max distance)
def scale_point(x,y,z, zfar, znear, fov, ar, camera_x, camera_y, camera_z ,camera_angle_x, camera_angle_y, camera_angle_z) -> Tuple:
    x,y,z = rotate_point(x,y,z, camera_angle_z)
    x,y,z = rotate_point(z,x,y, camera_angle_y)
    x,y,z = rotate_point(y,z,x, camera_angle_x)
    x,y,z = camera_x+x,camera_y+y,camera_z+z
    if z != 0:
        tan_half_fov = math.tan(fov/2)
        x = (ar*(1/tan_half_fov)*x)/z
        y = ((1/tan_half_fov)*y)/z
        z = z*(zfar/(zfar-znear))-((zfar*znear)/(zfar-znear))
    return (x,y,z)

#main graphics_library class
class gl:
    #class variables
    map_array = []
    light_array = []
    #creates passed attributes to class variables 
    def __init__(self, _width = 1920, _height = 1080, _fov = 55, _zfar = 1000, _znear = 0.1) -> None:
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
        self.background_colour = '#000000'
        self.outline = ''

    #sets the absolute location of the camera in global coordinates
    def camera_absolute(self, _camera_x = None, _camera_y = None, _camera_z = None, _camera_angle_x = None, _camera_angle_y = None, _camera_angle_z = None) -> None:
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

    #translates the location of the camera in local coordinates(mostly)
    def move_camera(self, _camera_x = 0, _camera_y = 0, _camera_z = 0, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0) -> None:
        self.camera_z += math.cos(self.camera_angle_y) * _camera_z
        self.camera_x += math.sin(self.camera_angle_y) * _camera_z
        self.camera_x += math.cos(self.camera_angle_y) * _camera_x
        self.camera_z += math.sin(self.camera_angle_y) * _camera_x
        self.camera_y += _camera_y
        
        self.camera_angle_x, self.camera_angle_y, self.camera_angle_z = self.camera_angle_x + math.radians(_camera_angle_x), self.camera_angle_y + math.radians(_camera_angle_y), self.camera_angle_z + math.radians(_camera_angle_z)

    #defines the style and renderer specifications
    def view_style(self, _wiremesh = False, _background = 1, outline_colour = '') -> None:
        #print(type(_background))
        if type(_background) != str:
            colours = []
            for light in self.light_array:
                colours.append((light[3],light[4],light[5]))
            if colours != []:
                hex_colour = _rgb_to_hex(average_colour(colours))[1:]
            else:
                hex_colour = '000000'
            _r, _g, _b = int(hex_colour[:2], 16), int(hex_colour[2:4], 16), int(hex_colour[4:], 16)
            r = max(0, min(255, int(_background*_r*255)))
            g = max(0, min(255, int(_background*_g*255)))
            b = max(0, min(255, int(_background*_b*255)))
            self.background_colour = '#%02x%02x%02x' % (r,g,b)
        else:
            self.background_colour = _background
        self.wiremesh = _wiremesh
        self.outline = outline_colour

    #calls a new frame and passes all walls and triangles to other functions
    def new_frame(self) -> list:
        frame = []
        sp = {
            0: {},
            1: {},
            2: {}
        }
        for model in self.map_array:
            for wall_num in range(0,len(model)):
                wall = model[wall_num]
                point_num = 0
                for point in wall[:-1]:
                    sp[point_num][wall_num] = scale_point(point[0],point[1],point[2], self.zfar, self.znear, self.fov, self.ar, self.camera_x, self.camera_y, self.camera_z , self.camera_angle_x, self.camera_angle_y, self.camera_angle_z)
                    point_num += 1

                temp_tri = render_wall_from_normalised_points(sp[0][wall_num][0],sp[0][wall_num][1],sp[0][wall_num][2],sp[1][wall_num][0],sp[1][wall_num][1],sp[1][wall_num][2],sp[2][wall_num][0],sp[2][wall_num][1],sp[2][wall_num][2],wall[len(wall)-1], self.wiremesh, self.light_array, self.outline)
                if temp_tri != None:
                    frame.append(temp_tri)
                    #print(temp_tri)
        frame.sort(key=lambda l : l[6], reverse= True)
        return frame

    #renders an image to the desired fromat
    def render_image(self, output_location = "images/output", file_format = '.svg', _line_thickness = 1) -> None:
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

#lighting class
class light():
    #pass attributes to local variables
    def __init__(self, parent, x, y, z, r, g, b) -> None:
        self.attributes = [x,y,z, r,g,b]
        self.parent = parent
        parent.light_array.append(self.attributes)
        self.light_position = parent.light_array.index(self.attributes)

    #translates the light locally
    def move_light(self,x,y,z) -> None:
        self.attributes[0] += x
        self.attributes[1] += y
        self.attributes[2] += z
        del self.parent.light_array[self.light_position]
        self.parent.light_array.append(self.attributes)
        self.light_position = self.parent.light_array.index(self.attributes)

    #deletes the light
    def delete(self) -> None:
        del self.parent.light_array[self.light_position]
        del self

#object class
class object():
    #load model and pass to parent
    def __init__(self, parent, _model, x = 0, y = 0 , z = 0, ax = 0, ay = 0, az = 0, scale_x = 1, scale_y = 1, scale_z = 1,colour = None, ignore_mtl = False) -> None:
        ax, ay, az = math.radians(ax), math.radians(ay), math.radians(az)
        model = open(_model, 'rt', encoding='cp1252')
        self.object_array = []
        self.parent = parent
        #load .obj files
        if _model[-4:] == '.obj':
            count = 0
            current_material = None
            if not ignore_mtl:
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
                        self.object_array.append([locals()["fv1"], locals()["fv"+str(p)], locals()["fv"+str(p+1)], _hex_to_rgb(new_colour)])
                elif line.split()[0] == 'usemtl':
                    current_material = materials[line.split()[1]]
        #load .stl files
        elif _model[-4:] == '.stl':
                if model.read()[:5] == 'solid':
                    ascii_stl = True
                else:
                    ascii_stl = False
                face = []
                #load ascii based stl
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
                    #load binary based stl
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
                                var_temp = int(byte)
                            elif bytenum == 82 or bytenum == 83 or bytenum == 84:
                                var_temp = int(byte) + var_temp
                            if bytenum == 84:
                                tri_count = int(var_temp)
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
                                var_temp = int(byte)
                            else:
                                var_temp = int(byte) + var_temp
                            if temp == 4 or temp == 8 or temp == 12:
                                temp_vertex.append(int(var_temp))
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
        parent.map_array.append(self.object_array)
        self.map_position = parent.map_array.index(self.object_array)
        
    def delete(self) -> None:
        del self.parent.map_array[self.map_array]
        del self
