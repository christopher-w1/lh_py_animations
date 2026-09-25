from PIL import Image, ImageDraw

class Text_SDay():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        return Text_SDay(xsize,ysize,fps)
    

    def get_frame(self):
        if self.scroll_wait <= 0:
            next(self.text)
            self.scroll_wait = 5
        self.scroll_wait -= 1
        return self.frame


    # Text: Science DAY
    def set_text(self):
        text_xOff = 40
        while True:
            img = Image.new("RGB", (28,14))
            draw_Science = ImageDraw.Draw(img)
            draw_Science.fontmode = "" #1           
            draw_Science.text((int(text_xOff),-2), "SCIENCE", font_size=13, stroke_width=0, fill=(3,116,255))

            draw_Comes_To = ImageDraw.Draw(img)
            draw_Comes_To.fontmode = "" #1           
            draw_Comes_To.text((int(text_xOff)+63,-2), "D", font_size=13, stroke_width=0, fill=(230,0,126))

            draw_Town_2026 = ImageDraw.Draw(img)
            draw_Town_2026.fontmode = "" #1           
            draw_Town_2026.text((int(text_xOff)+72,-2), "A", font_size=13, stroke_width=0, fill=(25,183,230))

            draw_Town_2026 = ImageDraw.Draw(img)
            draw_Town_2026.fontmode = "" #1           
            draw_Town_2026.text((int(text_xOff)+79,-2), "Y", font_size=13, stroke_width=0, fill=(250,143,0))
            for y in range(14):
                for x in range(28):
                    self.frame[x][y] = img.getpixel((x,y))
                    
                    #if img.getpixel((x,y)) == (255,255,255):
                    #    self.frame[x][y] = [255,255,255]
                    #else:
                    #    self.frame[x][y] = [0,0,0]
            #self.fix_pixel(text_xOff)
            text_xOff -= 1
            if text_xOff < -93:
                text_xOff = 28
            yield None

    def fix_pixel(self, text_xOff):
        pass
        #self.frame[][]

    def __init__(self,xsize=28, ysize=14, fps=30):
        self.name = "Text - \"SCIENCE DAY\""
        self.xsize = xsize
        self.ysize = ysize

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.text = self.set_text()
        self.scroll_wait = 0