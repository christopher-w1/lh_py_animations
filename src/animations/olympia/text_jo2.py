from PIL import Image, ImageDraw

class Text_jo2():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        return Text_jo2(xsize,ysize,fps)
    

    def get_frame(self):
        if self.scroll_wait <= 0:
            next(self.text)
            self.scroll_wait = 5
        self.scroll_wait -= 1
        return self.frame


    # Text: sag JO! zu Olympia
    def set_text(self):
        text_xOff = 40
        while True:
            img = Image.new("RGB", (28,14))
            draw = ImageDraw.Draw(img)
            draw.fontmode = "1"
            draw.text((int(text_xOff),-2), "Dein  JO!  fur  Olympia", font_size=12, stroke_width=0)
            for y in range(14):
                for x in range(28):
                    self.frame[x][y] = img.getpixel((x,y))
                    #if img.getpixel((x,y)) == (255,255,255):
                    #    self.frame[x][y] = [255,255,255]
                    #else:
                    #    self.frame[x][y] = [0,0,0]
            
            self.tranform_u(text_xOff)
            text_xOff -= 1
            if text_xOff < -145: #130
                text_xOff = 28
            yield None

    # Add dots to transfoem "u" to "ü"
    def tranform_u(self, text_xOff):
        x1 = 64 + text_xOff
        x2 = 68 + text_xOff
        if x1 >= 0 and x1 < 28:
            self.frame[x1][1] = [255,255,255]
        if x2 >= 0 and x2 < 28:  
            self.frame[x2][1] = [255,255,255]


    def __init__(self,xsize=28, ysize=14, fps=30):
        self.name = "Text - \"Dein  JO!  fur  Olympia\""
        self.xsize = xsize
        self.ysize = ysize

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.text = self.set_text()
        self.scroll_wait = 0