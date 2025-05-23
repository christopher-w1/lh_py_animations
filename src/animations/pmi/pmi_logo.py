from math import sqrt
from pyghthouse.utils import from_hsv
from time import sleep
class PMI():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        return PMI(xsize,ysize,fps)
    

    def get_frame(self):
        self.set_frame()
        return self.frame
    
    def set_frame(self):
        # Center of circles in (x, y)
        # Color in (h,s,v_scale)
        blue_center = (13.5, 0.5)
        blue_t_center = (12.5, 9)
        blue_hsv = (0.62, 0.9, 1)
        
        grey_center = (3.5, 9)
        grey_t_center = (14, 3)
        grey_hsv = (0.62, 0.0, 0.6)
        
        red_center = (23.5, 9)
        red_t_center = (13, 3)
        red_hsv = (1, 0.9, 1)

        points = [(blue_center, blue_t_center, blue_hsv), (grey_center, grey_t_center, grey_hsv), (red_center, red_t_center, red_hsv)]


        for y in range(14):
            for x in range(28):
                for point in points:
                    center, t_center, hsv = point
                    h, s , v_scale = hsv
                    
                    offset = 7
                    distance = abs( sqrt(pow(x-center[0], 2) + pow((y-center[1]) * 1.8, 2)) - offset )
                    
                    t_distance= sqrt(pow((x - t_center[0]), 2) + pow((y - t_center[1])*1.8, 2))
                    
                    thickness = (2.2 - t_distance*0.09)
                    
                    if thickness > 0.3:
                        v = distance = (1 - distance/thickness) * v_scale
                    else:
                        v = 0                    
                    
                    if v > 0:
                        self.frame[x][y] = from_hsv(h, s, v)
                    

    

    def __init__(self,xsize=28, ysize=14, fps=10):
        self.name = "PMI - Logo"
        self.xsize = xsize
        self.ysize = ysize
        
        self.color = (200,231,247)

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmap = ["0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000"]