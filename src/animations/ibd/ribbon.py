class Ribbon():
    @staticmethod
    def get_instance(xsize, ysize, fps):
        instance = Ribbon(xsize, ysize, fps)
        #instance.params()
        return instance
    
    def get_frame(self):
        for y in range(14):
            for x in range(28):
                if self.bitmap[y][x] == "1":
                    self.frame[x][y] = self.color_1
                elif self.bitmap[y][x] == "2":
                    self.frame[x][y] = self.color_2
                elif self.bitmap[y][x] == "3":
                    self.frame[x][y] = self.color_3
        return self.frame
                

    def __init__(self, xsize=28, ysize=14, fps=30):
        self.name = "IBD - Ribbon"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps

        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.color_1 = [118,86,143]
        self.color_2 = [121,84,146]
        self.color_3 = [116,78,130]

        self.bitmap = ["0000000000000000000000000000",
                       "0000000000022222200000000000",
                       "0000000000110000330000000000",
                       "0000000000110000330000000000",
                       "0000000000011003300000000000",
                       "0000000000001113000000000000",
                       "0000000000003111000000000000",
                       "0000000000033001100000000000",
                       "0000000000333001110000000000",
                       "0000000033330000111100000000",
                       "0000003333000000001111000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000"]