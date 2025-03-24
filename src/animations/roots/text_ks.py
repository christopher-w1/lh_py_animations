from PIL import Image, ImageDraw

class Text_ks():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        return Text_ks(xsize,ysize,fps)
    

    def get_frame(self):
        if self.scroll_wait <= 0:
            next(self.text_KS)
            self.scroll_wait = 4
        self.scroll_wait -= 1
        return self.frame


    # Text: #KielScales2025
    def set_text_KS(self):
        text_xOff = 40
        while True:
            img = Image.new("RGB", (28,14))
            draw = ImageDraw.Draw(img)
            draw.fontmode = "1"
            draw.text((int(text_xOff),0), "#KielScales25    2025CE    1000CE    500CE    500 BCE    1000 BCE", font_size=12, stroke_width=0)
            for y in range(14):
                for x in range(28):
                    if img.getpixel((x,y)) == (255,255,255):
                        self.frame[x][y] = self.color
                    else:
                        self.frame[x][y] = [0,0,0]
            text_xOff -= 1
            if text_xOff < -400:
                text_xOff = 28
            yield None


    def __init__(self,xsize=28, ysize=14, fps=30):
        self.name = "Text - \"#KielScales2025\" - ROOTS"
        self.xsize = xsize
        self.ysize = ysize
        
        self.color = (200,231,247)

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.text_KS = self.set_text_KS()
        self.scroll_wait = 0