from PIL import Image, ImageDraw

class Text_roots():
    @staticmethod
    def get_instance(xsize, ysize, fps=10):
        return Text_roots(xsize,ysize,fps)
    

    def get_frame(self):
        self.set_text_ROOTS()
        return self.frame


    def set_text_ROOTS(self):    
        for y in range(14):
            for x in range(28):
                if self.bitmap[y][x] == "1":
                    self.frame[x][y] = self.color
                else:
                    self.frame[x][y] = [0,0,0]


    def __init__(self,xsize=28, ysize=14, fps=10):
        self.name = "Text - ROOTS"
        self.xsize = xsize
        self.ysize = ysize
        
        self.color = (200,231,247)

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmap = ["0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0111100111001111011111001110",
                       "1100101100111001100100011001",
                       "0011101100010001100100000100",
                       "0110101100111001100100010011",
                       "1100100111001111000011001110",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000"]