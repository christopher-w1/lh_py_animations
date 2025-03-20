from random import shuffle

class Hill():
    @staticmethod
    def get_instance(xsize, ysize, fps=5):
        instance = Hill(xsize, ysize, fps)
        instance.params()
        return instance
    
    def params(self):
        self.xsize = 28
        self.ysize = 14
        self.fps = 5
        self.name = "Hill - ROOTS"
        

    def get_frame(self):
        if self.wait > 0:
            self.wait -= 1
            return self.frame
        
        if not self.stop:
            self.stop = next(self.hill)
            self.wait = 1
        
        return self.frame
 
    def build_hill(self):
        appear_order = []

        for y in range(14):
            appear_order.append([])
            for x in range(28):
                if self.bitmap[y][x] != "0":
                    appear_order[y].append((x,y))
            shuffle(appear_order[y])
        
        while True:
            if appear_order != []:
                row = appear_order.pop()
            else:
                yield True
            
            while row != []:
                x, y = row.pop()
                if self.bitmap[y][x] == "1":
                    self.frame[x][y] = self.color_1
                elif self.bitmap[y][x] == "2":
                    self.frame[x][y] = self.color_2
                yield False


    
    def __init__(self, xsize=28, ysize=14, fps=2):
        self.name = "Hill - ROOTS"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        self.frame_number = 0

        self.color_bg = [0,0,0]
        self.color_1 = [50,150,30]
        self.color_2 = [180,100,10]
        
        self.frame=[]
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
                       "0000000001111111111000000000",
                       "0000001111111111111111000000",
                       "0000111222222222222221110000",
                       "0001111111220000221111111000",
                       "0011111111220000221111111100",
                       "0000000000000000000000000000"]
        
        self.hill = self.build_hill()

        self.wait = 20
        self.stop = False