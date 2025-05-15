from PIL import Image, ImageDraw

class Text_ibd():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        return Text_ibd(xsize,ysize,fps)
    

    def get_frame(self):
        if self.scroll_wait <= 0:
            next(self.text_ibd)
            self.scroll_wait = 5
        self.scroll_wait -= 1
        return self.frame


    # Text: IBD Day
    def set_text_ibd(self):
        text_xOff = 40
        while True:
            img = Image.new("RGB", (28,14))
            draw = ImageDraw.Draw(img)
            draw.fontmode = "1"
            draw.text((int(text_xOff),-2), "World IBD Day", font_size=12, stroke_width=0)
            for y in range(14):
                for x in range(28):
                    if img.getpixel((x,y)) == (255,255,255):
                        self.frame[x][y] = self.color
                    else:
                        self.frame[x][y] = [0,0,0]
            text_xOff -= 1
            if text_xOff < -53:
                text_xOff = 28
            yield None


    def __init__(self,xsize=28, ysize=14, fps=30):
        self.name = "Text - \"World IBD Day\" - IBD"
        self.xsize = xsize
        self.ysize = ysize
        
        self.color = (188,55,230)

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.text_ibd = self.set_text_ibd()
        self.scroll_wait = 0