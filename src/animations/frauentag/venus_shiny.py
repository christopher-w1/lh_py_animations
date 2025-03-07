from random import randint

class Venus_shiny():
    @staticmethod
    def get_instance(xsize, ysize, fps=2):
        instance = Venus_shiny(xsize, ysize, fps)
        instance.params()
        return instance
    

    def params(self):
        self.xsize = 28
        self.ysize = 14
        self.fps = 5
        self.name = "Venus - Shiny"
        self.frame_num = 0
        

    def get_frame(self):
        # Determine animation speed
        
        # Speed of fade in of the symbol
        if self.frame_num == 0 and self.start > 0:
            self.set_frame(self.bitmaps[0])
            self.frame_num = 3
        
        # Speed of shiny effect
        elif self.frame_num == 0:
            self.set_frame(self.bitmaps[0])
            self.frame_num = 25
        
        else:
            self.frame_num -= 1
        
        return self.frame


    def set_frame(self, bitmap):
        if self.start > 0:
            for x in range(0, 28):
                for y in range(0, 14):
                    if 0 <= y + self.start < len(self.frame[0]):
                        if bitmap[y][x] == "1":
                            self.frame[x][y + self.start] = [randint(220, 255), randint(0, 115), randint(120, 255)]
                        else:
                            self.frame[x][y + self.start] = [0, 0, 0]

            self.start -= 1
        else:
            for x in range(0, 28):
                for y in range(0, 14):
                    if bitmap[y][x] == "1":
                        self.frame[x][y] = [randint(220, 255), randint(0, 115), randint(120, 255)]
                    else:
                        self.frame[x][y] = [0, 0, 0]
        return self.frame

    
    def __init__(self, xsize=28, ysize=14, fps=2):
        self.name = "Heart - Frauentag"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        self.start = 14
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmaps = [["0000000000110111011000000000",
                         "0000000011000000000110000000",
                         "0000001100000000000001100000",
                         "0000011000000000000000110000",
                         "0000011000000000000000110000",
                         "0000011000000000000000110000",
                         "0000011000000000000000110000",
                         "0000001100000000000001100000",
                         "0000000110000000000011000000",
                         "0000000000110111011000000000",
                         "0000000000000111000000000000",
                         "0000000111111111111111000000",
                         "0000000000000111000000000000",
                         "0000000000000111000000000000"]]