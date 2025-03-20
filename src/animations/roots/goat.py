class Goat():
    @staticmethod
    def get_instance(xsize, ysize, fps=5):
        instance = Goat(xsize, ysize, fps)
        instance.params()
        return instance
    

    def params(self):
        self.xsize = 28
        self.ysize = 14
        self.fps = 5
        self.name = "Goat - ROOTS"
        

    def get_frame(self):
        self.set_frame()
        return self.frame


    def set_frame(self):
        for x in range(0, 28):
            for y in range(0, 14):
                
                if self.bitmap[y][x] == "1":
                    self.frame[x][y] = self.color_1
                #elif self.bitmap[y][x] == "2":
                #    self.frame[x][y] = self.color_2
                else:
                    self.frame[x][y] = self.color_bg

    
    def __init__(self, xsize=28, ysize=14, fps=2):
        self.name = "Goat - ROOTS"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        self.frame_number = 0

        self.color_bg = [0,0,0]
        self.color_1 = [240,170,90]
        self.color_2 = [255,220,150]
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmap = ["0000000000000000000000000000",
                       "0000000111100000011110000000",
                       "0000111110010000100111110000",
                       "0111000001111111111000001110",
                       "0000000112222222222110000000",
                       "0001111122222222222211111000",
                       "0011110012112222112100111100",
                       "0000000012222222222100000000",
                       "0000000001222222221000000000",
                       "0000000001221111221000000000",
                       "0000000000122112210000000000",
                       "0000000000011111100000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000"]