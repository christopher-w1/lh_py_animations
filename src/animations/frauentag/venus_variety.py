from random import randint
import random

class Venus_variety():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        instance = Venus_variety(xsize, ysize, fps)
        instance.params()
        return instance
    

    def params(self):
        self.xsize = 28
        self.ysize = 14
        self.fps = 30
        self.name = "Venus - Variety"

        bitmap = ["0000000000000000000000000000",
                  "0000000000111111110000000000",
                  "0000000011000000001100000000",
                  "0000000100000000000010000000",
                  "0000000100000000000010000000",
                  "0000000011000000001100000000",
                  "0000000000111111110000000000",
                  "0000000000000110000000000000",
                  "0000000000111111110000000000",
                  "0000000000000110000000000000",
                  "0000000000000110000000000000",
                  "0000000000000110000000000000",
                  "0000000000000110000000000000",
                  "0000000000000000000000000000"]
        
        self.anim_num = 0
        self.anim_0 = self.white_screen()
        self.anim_1 = self.show_symbol(bitmap)
        self.anim_2 = self.turn_white(bitmap)
        self.anim_3 = self.terminate_symbol()
        
        

    def get_frame(self):
        if self.anim_num <= 3:
            self.set_frame()
        else:
            self.params()

        return self.frame


    def set_frame(self):
        match self.anim_num:
            case 0:
                next(self.anim_0)
            case 1:
                next(self.anim_1)
            case 2:
                next(self.anim_2)
            case 3:
                next(self.anim_3)




    def white_screen(self):
        for y in range(0,7):
            for x in range(0,28):
                self.frame[x][y] = [255,255,255]
                self.frame[27-x][13-y] = [255,255,255]
                yield False
        self.anim_num += 1
        yield True

    
    def show_symbol(self, bitmap):
        for y in range(0, 14):
            g = y * 18.214
            for x in range(0, 14):
                if bitmap[y][x] == "1":
                    self.frame[x][y] = [255, 255, 255]
                else:
                    r = int((x / 28) * 255)
                    b = 255 - int((x / 28) * 255)
                    self.frame[x][y] = [r, g, b]
                    self.frame[27 - x][13 - y] = [int(((27 - x) / 28) * 255), (13 - y) * 18.214, 255 - int(((27 - x) / 28) * 255)]
            
                if bitmap[13 - y][27 - x] == "1":
                    self.frame[27 - x][13 - y] = [255, 255, 255]
                else:
                    self.frame[27 - x][13 - y] = [int(((27 - x) / 28) * 255), (13 - y) * 18.214, 255 - int(((27 - x) / 28) * 255)]
                yield False
        
        for _ in range(100):
            yield False
        
        self.anim_num += 1
        yield True


    def turn_white(self,bitmap):
        coords = []
        for y in range(0,14):
            for x in range(0,28):
                coords.append((x,y))
        random.shuffle(coords)
        
        for x, y in coords:
            if bitmap[y][x] == "1":
                self.frame[x][y] = [0, 0, 0]
            else:
                self.frame[x][y] = [255, 255, 255]
            yield False
        
        for _ in range(100):
            yield False
        
        self.anim_num += 1
        yield True


    def terminate_symbol(self):
        # Term rows
        for y in range(0, 7):
            for x in range(0, 27):
                if self.frame[x][y] == [0, 0, 0]:
                    self.frame[x][y + 1] = [0, 0, 0]
                    self.frame[x][y] = [255, 255, 255]
                if 13 - y < 8:
                    continue
                else:
                    if self.frame[x][13 - y] == [0, 0, 0]:
                        self.frame[x][13 - y - 1] = [0, 0, 0]
                        self.frame[x][13 - y] = [255, 255, 255]
            for _ in range(8):
                yield False
        
        # Term collumns
        for x in range(7, 14):
            y = 7
            if self.frame[x][y] == [0, 0, 0]:
                #self.frame[x + 1][y] = [0, 0, 0]
                self.frame[x][y] = [255, 255, 255]
            if self.frame[27 - x][y] == [0, 0, 0]:
                #self.frame[27 - x - 1][y] = [0, 0, 0]
                self.frame[27 - x][y] = [255, 255, 255]
            for _ in range(8):
                yield False
        
        for x in range(0,28):
            for y in range(0,14):
                self.frame[x][13-y] = [0,0,0]
            yield False

        for _ in range(50):
                yield False

        self.anim_num += 1
        yield  True


        
    
    def __init__(self, xsize=28, ysize=14, fps=30):
        self.name = "Venus - Variety"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        bitmap = ["0000000000000000000000000000",
                  "0000000000111111110000000000",
                  "0000000011000000001100000000",
                  "0000000100000000000010000000",
                  "0000000100000000000010000000",
                  "0000000011000000001100000000",
                  "0000000000111111110000000000",
                  "0000000000000110000000000000",
                  "0000000000111111110000000000",
                  "0000000000000110000000000000",
                  "0000000000000110000000000000",
                  "0000000000000110000000000000",
                  "0000000000000110000000000000",
                  "0000000000000000000000000000"]
        
        self.anim_num = 0
        self.anim_0 = self.white_screen()
        self.anim_1 = self.show_symbol(bitmap)
        self.anim_2 = self.turn_white(bitmap)
        self.anim_3 = self.terminate_symbol()