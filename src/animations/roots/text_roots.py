from PIL import Image, ImageDraw
from random import random

class Text_roots():
    class Dot():
        def __init__(self, x, y, x_velocity, color):
            self.x = x
            self.y = y
            self.velocity = x_velocity
            self.color = color

        def move(self):
            old_x = self.x
            self.x = (self.velocity + self.x) % 28
            return int(old_x) == int(self.x)

        def get_dot(self):
            return (int(self.x), self.y, self.color)
        
    
    @staticmethod
    def get_instance(xsize, ysize, fps=10):
        return Text_roots(xsize,ysize,fps)
    
    def get_frame(self):
        if self.wait > 0:
            self.wait -=1
            return self.frame
        self.increase_value()
        self.draw_points()
        self.set_text_ROOTS()
        self.wait = 1
        return self.frame
    

    def draw_points(self):
        for dot in self.dots:
            has_moved = dot.move()
            x, y, color = dot.get_dot()
            # Reverse increase_value effect
            if has_moved:
                self.frame[x][y] = self.frame[x][y][:]
                for i in range(3):
                    if color[i] <= 5:
                        self.frame[x][y][i] -= 1
            else:
                old_color = self.frame[x][y]
                self.frame[x][y] = color#self.mix_color(old_color, color)

    def mix_color(self, color1, color2):
        color = [0,0,0]
        for i in range(3):
            color[i] = (color1[i] + color2[i]) / 2
            if color[i] >= 255:
                color[i] = 255
        
        return color
    
    def increase_value(self):
        for y in range(13):
            if 4 > y or y > 8:
                for x in range(28):
                    color = self.frame[x][y][:]
                    for i in range(len(color)):
                        color[i] += 2
                        if color[i] >= 255:
                            color[i] = 255
                    self.frame[x][y] = color


    def set_text_ROOTS(self):    
        for y in range(4,9):
            for x in range(28):
                if self.bitmap[y][x] == "1":
                    self.frame[x][y] = self.color
                else:
                    self.frame[x][y] = [0,0,0]


    def init_dots(self):
        color1 = [50,110,110]
        color2 = [90,70,20]
        color3 = [220,80,50]
        color4 = [160,60,60]
        color5 = [0,0,100]
        
        dot1  = self.Dot(5,  0,  (random()*0.4+0.5)     , color1)
        dot2  = self.Dot(27, 0,  (random()*0.4+0.5)*(-1), color2)
        dot3  = self.Dot(14, 1,  (random()*0.4+0.5)     , color1)
        dot4  = self.Dot(24, 1,  (random()*0.4+0.5)*(-1), color3)
        dot5  = self.Dot(0,  2,  (random()*0.4+0.5)     , color4)
        dot6  = self.Dot(20, 2,  (random()*0.4+0.5)*(-1), color2)
        dot7  = self.Dot(2,  3,  (random()*0.4+0.5)     , color3)
        dot8  = self.Dot(14, 3,  (random()*0.4+0.5)*(-1), color5)
        dot9  = self.Dot(8,  9,  (random()*0.4+0.5)     , color5)
        dot10 = self.Dot(15, 9,  (random()*0.4+0.5)*(-1), color4)
        dot11 = self.Dot(0,  10, (random()*0.4+0.5)     , color2)
        dot12 = self.Dot(18, 10, (random()*0.4+0.5)*(-1), color4)
        dot13 = self.Dot(20, 11, (random()*0.4+0.5)     , color3)
        dot14 = self.Dot(27, 11, (random()*0.4+0.5)*(-1), color2)
        dot15 = self.Dot(15, 12, (random()*0.4+0.5)     , color1)
        dot16 = self.Dot(25, 12, (random()*0.4+0.5)*(-1), color2)
        self.dots = [dot1, dot2, dot3, dot4, dot5, dot6, dot7, dot8, dot9, dot10, dot11, dot12, dot13, dot14, dot15, dot16]
    
    def __init__(self,xsize=28, ysize=14, fps=10):
        self.name = "Text - ROOTS"
        self.xsize = xsize
        self.ysize = ysize
        
        self.color = [255,255,255]

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])
        
        self.init_dots()

        self.wait = 10

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