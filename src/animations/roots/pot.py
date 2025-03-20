from random import shuffle

class Pot():
    @staticmethod
    def get_instance(xsize, ysize, fps=10):
        return Pot(xsize,ysize,fps)
    
    def get_frame(self):
        if self.wait > 0:
            self.wait -= 1
            return self.frame
        
        if not self.stop:
            self.stop = next(self.anim_1)
            self.wait = 1
        
        return self.frame

    def build_vase(self):
        appear_order = []

        for y in range(14):
            appear_order.append([])
            for x in range(28):
                if self.bitmap[y][x] == "1":
                    appear_order[y].append((x,y))
            shuffle(appear_order[y])
        
        while True:
            if appear_order != []:
                row = appear_order.pop()
            else:
                yield True
            
            while row != []:
                x, y = row.pop()
                self.frame[x][y] = self.color
                yield False
    
    def __init__(self,xsize=28, ysize=14, fps=10):
        self.name = "Pot - ROOTS"
        self.xsize = xsize
        self.ysize = ysize
        
        self.color = [240,170,90]

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmap = ["0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000011111111111111111100000",
                       "0000100111111111111110010000",
                       "0000011111111111111111100000",
                       "0000111111111111111111110000",
                       "0001111111111111111111111000",
                       "0001111111111111111111111000",
                       "0000111111111111111111110000",
                       "0000011111111111111111100000",
                       "0000000111111111111110000000",
                       "0000000001111111111000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000"]
        
        self.wait = 20
        self.stop = False

        self.anim_1 = self.build_vase()
        
        



        