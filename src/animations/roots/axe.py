class Axe():
    @staticmethod
    def get_instance(xsize, ysize, fps=5):
        instance = Axe(xsize, ysize, fps)
        instance.params()
        return instance
    

    def params(self):
        self.xsize = 28
        self.ysize = 14
        self.fps = 5
        self.name = "Axe - ROOTS"
        

    def get_frame(self):
        self.set_frame(self.bitmaps[int(self.frame_number)])
        self.frame_number += 0.04
        self.frame_number %= 2
        return self.frame


    def set_frame(self, bitmap):
        for x in range(0, 28):
            for y in range(0, 14):
                
                if bitmap[y][x] == "1":
                    self.frame[x][y] = self.color_1
                elif bitmap[y][x] == "2":
                    self.frame[x][y] = self.color_2
                elif bitmap[y][x] == "3":
                    self.frame[x][y] = self.color_3
                else:
                    self.frame[x][y] = self.color_bg

    
    def __init__(self, xsize=28, ysize=14, fps=2):
        self.name = "Axe - ROOTS"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        self.frame_number = 0

        self.color_bg = [0,0,0]
        self.color_1 = [100,100,110]
        self.color_2 = [180,100,10]
        self.color_3 = [240,170,90]
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmaps = [["0000000000000000000000000000",
                         "0000001133133111111100000000",
                         "0000011111311111111110000000",
                         "0000011113131111111110000000",
                         "0000000131113111111100000000",
                         "0000000022222000000000000000",
                         "0000000022222000000000000000",
                         "0000000022222000000000000000",
                         "0000000022222000000000000000",
                         "0000000022222000000000000000",
                         "0000000022222000000000000000",
                         "0000000022222000000000000000",
                         "0000000022222000000000000000",
                         "0000000000000000000000000000"],
                        
                        ["0000000000000000000000000000",
                         "0000000000011130000000000000",
                         "0000000001111131133000000000",
                         "0000000011111333111111100000",
                         "0000000001331131111111110000",
                         "0000000000221131111111110000",
                         "0000000002222200111111100000",
                         "0000000022222000000000000000",
                         "0000000222220000000000000000",
                         "0000002222200000000000000000",
                         "0000022222000000000000000000",
                         "0000222220000000000000000000",
                         "0002222200000000000000000000",
                         "0000000000000000000000000000"]]