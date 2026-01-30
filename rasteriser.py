import math

class rasteriser:
    def __init__(self, _height, _width, default_colour = '#000000'):
        self.height = _height
        self.width = _width
        self.image_pixels = []
        for x in range(0, self.height):
            self.image_pixels.append([])
            for y in range(0, self.width):
                self.image_pixels[x].append([])
                self.image_pixels[x][y] = default_colour
    
    def bottom_triangle(self, triangle, colour):
        if triangle[1] == triangle[3]:
            topv = [triangle[4], triangle[5]]
            v1 = [triangle[0], triangle[1]]
            v2 = [triangle[2], triangle[3]]
        elif triangle[3] == triangle[5]:
            topv = [triangle[0], triangle[1]]
            v1 = [triangle[4], triangle[5]]
            v2 = [triangle[2], triangle[3]]
        else:
            topv = [triangle[2], triangle[3]]
            v1 = [triangle[0], triangle[1]]
            v2 = [triangle[4], triangle[5]]
        if (v1[0]-topv[0])/(v1[1]-topv[1]) < (v2[0]-topv[0])/(v2[1]-topv[1]):
            islope1 = (v1[0]-topv[0])/(v1[1]-topv[1])
            islope2 = (v2[0]-topv[0])/(v2[1]-topv[1])
        else:
            islope2 = (v1[0]-topv[0])/(v1[1]-topv[1])
            islope1 = (v2[0]-topv[0])/(v2[1]-topv[1])
        x1 = topv[0]
        x2 = topv[0]
        called = False
        if topv[1] < 0:
            topv[1] = 0
        for y in range(topv[1], v1[1], 1):
            for x in range(math.floor(x1), math.ceil(x2), 1):
                if x > 0 and x < self.width:
                    if y > 0 and y < self.height:
                        self.image_pixels[y][x] = colour
                    called = True
            x1 += islope1
            x2 += islope2


    def top_triangle(self, triangle, colour):
        if triangle[1] == triangle[3]:
            bottomv = [triangle[4], triangle[5]]
            _v1 = [triangle[0], triangle[1]]
            _v2 = [triangle[2], triangle[3]]
        elif triangle[3] == triangle[5]:
            bottomv = [triangle[0], triangle[1]]
            _v1 = [triangle[4], triangle[5]]
            _v2 = [triangle[2], triangle[3]]
        else:
            bottomv = [triangle[2], triangle[3]]
            _v1 = [triangle[0], triangle[1]]
            _v2 = [triangle[4], triangle[5]]
        if _v1[0] <= _v2[0]:
            v1 = _v1
            v2 = _v2
        else:
            v1 = _v2
            v2 = _v1 
        islope1 = (bottomv[0]-v1[0])/(bottomv[1]-v1[1])
        islope2 = (bottomv[0]-v2[0])/(bottomv[1]-v2[1])
        '''
        if (bottomv[0]-v1[0])/(bottomv[1]-v1[1]) < (bottomv[0]-v2[0])/(bottomv[1]-v2[1]):
            islope1 = (bottomv[0]-v1[0])/(bottomv[1]-v1[1])
            islope2 = (bottomv[0]-v2[0])/(bottomv[1]-v2[1])
        else:
            islope2 = (bottomv[0]-v1[0])/(bottomv[1]-v1[1])
            islope1 = (bottomv[0]-v2[0])/(bottomv[1]-v2[1])
        '''
        if v1[0] < v2[0]:
            x1 = v1[0]
            x2 = v2[0]
            islope1 = (bottomv[0]-v1[0])/(bottomv[1]-v1[1])
            islope2 = (bottomv[0]-v2[0])/(bottomv[1]-v2[1])
        else:
            x1 = v2[0]
            x2 = v1[0]
            islope2 = (bottomv[0]-v1[0])/(bottomv[1]-v1[1])
            islope1 = (bottomv[0]-v2[0])/(bottomv[1]-v2[1])


        called = False
        for y in range(v1[1], bottomv[1], 1):
            for x in range(math.floor(x1), math.ceil(x2), 1):
                if x > 0 and x < self.width:
                    if y > 0 and y < self.height:    
                        self.image_pixels[y][x] = colour
                        called = True
            x1 += islope1
            x2 += islope2

    def draw_triangle(self, triangle, colour):
        if (triangle[1] == triangle[3] and triangle[5] < triangle[3]) or (triangle[3] == triangle[5] and triangle[1] < triangle[5]) or (triangle[1] == triangle[5] and triangle[3] < triangle[5]):
            self.bottom_triangle(triangle, colour)
        elif (triangle[1] == triangle[3] and triangle[5] > triangle[3]) or (triangle[3] == triangle[5] and triangle[1] > triangle[5]) or (triangle[1] == triangle[5] and triangle[3] > triangle[5]):
            self.top_triangle(triangle, colour)
        elif triangle[1] == triangle[3] and triangle[1] == triangle[5]:
            return
        
        else:
            new_tri = [[triangle[0],triangle[1]],[triangle[2],triangle[3]],[triangle[4],triangle[5]]]
            new_tri.sort(key=lambda y: y[-1])
            newx = int(new_tri[0][0] + ((new_tri[1][1]-new_tri[0][1])/(new_tri[2][1] - new_tri[0][1]))*(new_tri[2][0] - new_tri[0][0]))
            self.bottom_triangle([new_tri[0][0], new_tri[0][1], new_tri[1][0], new_tri[1][1], newx, new_tri[1][1]], colour)
            self.top_triangle([new_tri[2][0], new_tri[2][1], new_tri[1][0], new_tri[1][1], newx, new_tri[1][1]], colour)
           