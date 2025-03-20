class Roots():
    @staticmethod
    def get_instance(xsize, ysize, fps=10):
        return Roots(xsize,ysize,fps)
    
    def get_frame(self):
        self.set_frame()
        return self.frame

    def set_frame(self):
        for y in range(14):
            for x in range(28):
                if self.bitmap[y][x] == "0":
                    self.frame[x][y] = [2,10,13]
                elif self.bitmap[y][x] == "1":
                    self.frame[x][y] = self.color
                else:
                    self.frame[x][y] = [0,0,0]
    
    
    
    
    def __init__(self,xsize=28, ysize=14, fps=10):
        self.name = "Logo - ROOTS"
        self.xsize = xsize
        self.ysize = ysize
        
        self.color = [86,178,228]

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmap = ["0000000000000000000000000000",
                       "0000000001111122222220000000",
                       "0000011111111111222211100000",
                       "0001111111111112222111111000",
                       "0011111111112222211111111100",
                       "0111111111122222111111111110",
                       "0111111112222111111111111110",
                       "0111111111222211111111111110",
                       "0011111111122211111111111100",
                       "0001111112222111111111111000",
                       "0000011122111111111111100000",
                       "0000000011111111111100000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000"]
        