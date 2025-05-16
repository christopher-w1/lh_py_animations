from pyghthouse.utils._color import from_hsv
from math import sqrt

class Lighthouse():
    @staticmethod
    def get_instance(xsize, ysize, fps=5):
        instance = Lighthouse(xsize, ysize, fps)
        instance.params()
        return instance
    

    def params(self):
        self.xsize = 28
        self.ysize = 14
        self.fps = 30
        self.name = "Lighthouse"

    def __init__(self, xsize=28, ysize=14, fps=30):
        self.name = "Lighthouse"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps

        self.color_bg = [0,0,0]
        self.color_1 = [60,220,10]
        self.color_2 = [250,255,255]
        self.color_3 = [255,5,5]
        self.color_4 = [128,128,128]
        self.color_5 = [250,200,10]
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmap = ["5500000000004444000000000055",
                       "5555550000444444440000555555",
                       "5555555555222222225555555555",
                       "5555555555222222225555555555",
                       "5555550000333333330000555555",
                       "5500000000333333330000000055",
                       "0000000000222222220000000000",
                       "0000000000222222220000000000",
                       "0000000000333333330000000000",
                       "0000000000333333330000000000",
                       "0000000000222222220000000000",
                       "0000000000222222220000000000",
                       "0000001111111111111111000000",
                       "0001111111111111111111111000"]
        

    def get_frame(self):
        self.set_frame()
        return self.frame


    def set_frame(self):
        for x in range(0, 28):
            for y in range(0, 14):
                
                if self.bitmap[y][x] == "1":
                    self.frame[x][y] = self.color_1
                elif self.bitmap[y][x] == "2":
                    self.frame[x][y] = self.color_2
                elif self.bitmap[y][x] == "3":
                    self.frame[x][y] = self.color_3
                elif self.bitmap[y][x] == "4":
                    self.frame[x][y] = self.color_4
                elif self.bitmap[y][x] == "5":
                    distance = sqrt(pow(x-13.5,2)+pow(y-2.5,2)*1000)*0.005+1
                    v = 1/distance
                    self.frame[x][y] = from_hsv(0.15,0.6,v)
                else:
                    self.frame[x][y] = self.color_bg
                    #root = pow(x-13.5,2)-pow(y-2.5,2)*1
                    #if root > 0:
                    #    distance = sqrt(pow(x-13.5,2)-pow(y-2.5,2)*1)+1
                    #    v = distance
                    #else:
                    #    v = 0
                    #self.frame[x][y] = from_hsv(0.15,0.9,v)