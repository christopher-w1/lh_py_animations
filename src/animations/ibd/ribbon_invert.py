class RibbonI():
    @staticmethod
    def get_instance(xsize, ysize, fps):
        instance = RibbonI(xsize, ysize, fps)
        #instance.params()
        return instance
    
    def get_frame(self):
        next(self.ribbon_appear)
        return self.frame
                
    def appear_ribbon(self):
        # Paint background
        for y in range(14):
            for x in range(28):
                self.frame[x][y] = self.color_bg
        
        # Wait for start
        for _ in range(30):
            yield False
        
        # Appear from bottom left to top right
        for y in range(13,-1,-1):
            for x in range(28):
                if self.bitmap[y][x] == "3" or self.bitmap[y][x] == "4":
                    self.frame[x][y] = self.color_1
                    yield False
                    yield False
                    yield False
        
        # Appear from right to left
        for x in range(27,-1,-1):
            for y in range(14):
                if self.bitmap[y][x] == "2":
                    self.frame[x][y] = self.color_2
                    yield False
                    yield False
                    yield False

        # Appear from top left to bottom right
        for x in range(28):
            for y in range(14):
                if self.bitmap[y][x] == "1" or self.bitmap[y][x] == "4":
                    self.frame[x][y] = self.color_3
                    yield False
                    yield False
                    yield False
        while True:
            yield True
        

    
    
    def __init__(self, xsize=28, ysize=14, fps=30):
        self.name = "IBD - Ribbon inverted"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps

        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.color_bg = [125,80,140]
        self.color_1 = [255,255,255]
        self.color_2 = [242,242,242]
        self.color_3 = [240,240,240]

        self.ribbon_appear = self.appear_ribbon()

        self.bitmap = ["0000000000000000000000000000",
                       "0000000000222222000000000000",
                       "0000000001100000330000000000",
                       "0000000001110003330000000000",
                       "0000000001111003330000000000",
                       "0000000000111103300000000000",
                       "0000000000011444000000000000",
                       "0000000000034441110000000000",
                       "0000000003333011111100000000",
                       "0000000033330001111111000000",
                       "0000000333330000011111000000",
                       "0000000333300000001110000000",
                       "0000000003000000000000000000",
                       "0000000000000000000000000000"]