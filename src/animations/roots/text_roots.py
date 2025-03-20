from PIL import Image, ImageDraw

class Text_roots():
    @staticmethod
    def get_instance(xsize, ysize, fps=10):
        return Text_roots(xsize,ysize,fps)
    

    def get_frame(self):
        self.set_text_ROOTS()
        self.smooth_edge(1,5)
        return self.frame


    def set_text_ROOTS(self):    
        for y in range(14):
            for x in range(28):
                if self.bitmap[y][x] == "1":
                    self.frame[x][y] = self.color
                else:
                    self.frame[x][y] = [0,0,0]


    def smooth_edge(self, n=1, prio=3):
        # current frame in processing
        for _ in range(n): 
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
                
            
    def get_nearby_colors(self, x, y, prio=0):
        colors = []
        for offset_x in range(-1,2):
            for offset_y in range(-1,2):
                if (x+offset_x >= 0 and x+offset_x < len(self.frame)) and (y+offset_y >= 0 and y+offset_y < len(self.frame[0])):
                    colors.append(self.frame[x+offset_x][y+offset_y])
                    for _ in range(prio):
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


    def __init__(self,xsize=28, ysize=14, fps=10):
        self.name = "Text - ROOTS"
        self.xsize = xsize
        self.ysize = ysize
        
        self.color = (86,178,228)

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmap = ["0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0111100111001111011111001110",
                       "1100101100111001100100011001",
                       "0011101100010001100100000100",
                       "0110101100111001100100010011",
                       "1100100111001111000011001110",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000"]