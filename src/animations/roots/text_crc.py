from PIL import Image, ImageDraw

class Text_crc():
    @staticmethod
    def get_instance(xsize, ysize, fps=10):
        return Text_crc(xsize,ysize,fps)
    

    def get_frame(self):
        if not self.stop:
            self.set_text_KC()
            self.stop=True
        return self.frame

     
    # Text: KC \n 2025
    def set_text_KC(self):
        img = Image.new("RGB", (28,14), (0,0,0))
        draw = ImageDraw.Draw(img)
        draw.fontmode = "1"
        draw.multiline_text((2,-3),"CRC\n1266", align="center", spacing=-3) 
        for y in range(14):
            for x in range(28):
                if img.getpixel((x,y)) == (255,255,255):
                    self.frame[x][y] = self.color
                else:
                    self.frame[x][y] = [0,0,0]


    def __init__(self,xsize=28, ysize=14, fps=10):
        self.name = "Text - \"CRC\\n1266\" - ROOTS"
        self.xsize = xsize
        self.ysize = ysize
        
        self.color = (200,231,247)

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.stop = False