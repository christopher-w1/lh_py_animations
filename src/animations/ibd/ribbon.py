class Ribbon():
    @staticmethod
    def get_instance(xsize, ysize, fps):
        instance = Ribbon(xsize, ysize, fps)
        #instance.params()
        return instance
    
    def get_frame(self):
        next(self.ribbon_appear)
        return self.frame
                
    def appear_ribbon(self):
        for _ in range(30):
            yield False
        # Appear from bottom left to top right
        for y in range(13,-1,-1):
            for x in range(28):
                if self.bitmap[y][x] == "3" or self.bitmap[y][x] == "4":
                    self.frame[x][y] = self.color_1
                    yield False
                    yield False
        
        # Appear from right to left
        for x in range(27,-1,-1):
            for y in range(14):
                if self.bitmap[y][x] == "2":
                    self.frame[x][y] = self.color_2
                    yield False
                    yield False

        # Appear from top left to bottom right
        for x in range(28):
            for y in range(14):
                if self.bitmap[y][x] == "1" or self.bitmap[y][x] == "4":
                    self.frame[x][y] = self.color_3
                    yield False
                    yield False
        while True:
            yield True
        

    
    
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

        self.color_1 = [188,55,230]
        self.color_2 = [179,52,218]
        self.color_3 = [174,50,212]

        self.ribbon_appear = self.appear_ribbon()

        self.bitmap = ["0000000000000000000000000000",
                       "0000000000022222200000000000",
                       "0000000000110000033000000000",
                       "0000000000111000333000000000",
                       "0000000000111100333000000000",
                       "0000000000011110330000000000",
                       "0000000000001144400000000000",
                       "0000000000003444111000000000",
                       "0000000000333301111110000000",
                       "0000000003333000111111100000",
                       "0000000033333000001111100000",
                       "0000000033330000000111000000",
                       "0000000000300000000000000000",
                       "0000000000000000000000000000"]