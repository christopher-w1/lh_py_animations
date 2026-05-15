class Text_ibd_nb():
    @staticmethod
    def get_instance(xsize, ysize, fps=2):
        instance = Text_ibd_nb(xsize, ysize, fps)
        return instance
 
    def get_frame(self):
        if self.count < 4:
            self.count += 1
            return self.frame
        self.count = 0        
        
        self.offset %= len(self.bitmaps[1][0]) + 1
        for y in range(7):
            for x in range(28):
                if self.bitmaps[0][y][x] == "1":
                    self.frame[x][y] = self.color
        
        for y in range(7,14):
            for x in range(0,28):
                if self.bitmaps[1][y-7][int(x+self.offset) %len(self.bitmaps[1][0])] == "1":
                    self.frame[x][y] = self.color
                else: 
                    self.frame[x][y] = (0,0,0)
        self.offset += 1
        return self.frame

    def __init__(self, xsize=28, ysize=14, fps=2):
        self.name = "Scrolltext - IBD has no boarders"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        self.frame_number = 0
        self.count = 0
        self.offset = 0

        self.color = (188,55,230)
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmaps = [["0000000000000000000000000000",
                         "0011100111111100011111110000",
                         "0011100111001110011100111000",
                         "0011100111111100011100011100",
                         "0011100111001110011100111000",
                         "0011100111111100011111110000",
                         "0000000000000000000000000000"],
                        ["000000000000000000000000100100011000011100000010001000111000000011100001110001110001110001111001110000111",
                         "000000000000000000000000100100100100100000000011001001000100000010010010001001001001001001000001001001000",
                         "000000000000000000000000111100111100011000000010101001000100000011100010001001110001001001110001110000110",
                         "000000000000000000000000100100100100000100000010011001000100000010010010001001001001001001000001001000001",
                         "000000000000000000000000100100100100111000000010001000111000000011100001110001001001110001111001001001110",
                         "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                         "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"]
                        ]