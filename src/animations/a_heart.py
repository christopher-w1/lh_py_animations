from math import sqrt
from math import sin, pi

import animations.color_functions as clr


class Heart():
    @staticmethod
    def get_instance(xsize, ysize, fps=2):
        instance = Heart(xsize, ysize, fps)
        instance.params()
        return instance
    

    def params(self):
        self.xsize = 28
        self.ysize = 14
        self.fps = 60
        self.name = "Heart"

        self.color_heart = self.generate_color_heart()
        

    def get_frame(self):
        self.draw_heart(self.bitmaps[0])
        #self.smooth_edge(1, True)
        return self.frame


    def draw_heart(self, bitmap):
        color = next(self.color_heart)
        for x in range(0, 28):
            for y in range(0, 14):
                if bitmap[y][x] == "1":
                    self.frame[x][y] = color
                else:
                    self.frame[x][y] = (0,0,0)


    def generate_color_heart(self):
        faculties = {
        'theology': (86,35,129),
        'law': (228,49,23),
        'medicine': (153,194,33),
        'philosophy': (106,172,218),
        'agriculture/nutritional': (57,132,46),
        'mathematics/science': (242,148,0),
        'economics/social': (0,103,124),
        'technical': (0,61,134),
        }
        cau_color = (155,10,125)
        colors = [(255,0,0), (255,0,0), (155,10,125), (155,10,125), 
                  (86,35,129), (228,49,23), (153,194,33), (106,172,218), (57,132,46), (242,148,0), (0,103,124), (0,61,134), 
                  (155,10,125), (155,10,125)]
        
        generator = clr.generator_cycle_colors(colors, 25, 50)
        while True:
            yield next(generator)

    
    def __init__(self, xsize=28, ysize=14, fps=60):
        self.name = "Heart"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.color_heart = self.generate_color_heart()

        self.bitmaps = [["0000000000000000000000000000",
                         "0000000000000000000000000000",
                         "0000001111110001111110000000",
                         "0000111111111011111111100000",
                         "0001111111111111111111110000",
                         "0001111111111111111111110000",
                         "0000111111111111111111100000",
                         "0000011111111111111111000000",
                         "0000000111111111111100000000",
                         "0000000001111111110000000000",
                         "0000000000011111000000000000",
                         "0000000000000100000000000000",
                         "0000000000000000000000000000",
                         "0000000000000000000000000000"]]
    

    def smooth_edge(self, n, prio):
        # current frame in processing
        img = []
        
        for y in range(0, 14):
            img.append([])
            for x in range(0, 28):
                colors = self.get_nearby_colors(x, y, prio)
                mixed_color = self.get_mixed_color(colors)
                img[y].append(mixed_color)

        for y in range(0, 14):
            for x in range(0, 28):
                self.frame[x][y] = img[y][x]
                
            
    def get_nearby_colors(self, x, y, prio):
        colors = []
        
        for offset_x in range(-1,2):
            for offset_y in range(-1,2):
                
                if (x+offset_x >= 0 and x+offset_x < len(self.frame)) and \
                    (y+offset_y >= 0 and y+offset_y < len(self.frame[0])):
                    
                    colors.append(self.frame[x+offset_x][y+offset_y])
                    if prio:
			# increase dominance of center
                        colors.append(self.frame[x][y])
        
        return colors

    
    def get_mixed_color(self, colors:list[list[int]]):
        # Problem: Only works for larger forms, needs adjustments for smaller forms
        mixed_color = [0,0,0]
        
        for color in colors:
            mixed_color[0] += color[0]
            mixed_color[1] += color[1]
            mixed_color[2] += color[2]
        
        num_colors = len(colors)

        mixed_color[0] //= num_colors
        mixed_color[1] //= num_colors
        mixed_color[2] //= num_colors
        
        return mixed_color
