from PIL import Image, ImageDraw

class Text_sctt_long():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        return Text_sctt_long(xsize,ysize,fps)
    

    def get_frame(self):
        if self.scroll_wait <= 0:
            next(self.text)
            self.scroll_wait = 5
        self.scroll_wait -= 1
        return self.frame


    # Text: Science Comes To Town 2026
    def set_text(self):
        text_xOff = 40
        while True:
            img = Image.new("RGB", (28,14))
            draw_Science = ImageDraw.Draw(img)
            draw_Science.fontmode = "" #1           
            draw_Science.text((int(text_xOff),-2), "Science", font_size=13, stroke_width=0, fill=(255,0,158))

            draw_Comes_To = ImageDraw.Draw(img)
            draw_Comes_To.fontmode = "" #1           
            draw_Comes_To.text((int(text_xOff)+54,-2), "Comes  To", font_size=13, stroke_width=0, fill=(71,158,1))

            draw_Town_2026 = ImageDraw.Draw(img)
            draw_Town_2026.fontmode = "" #1           
            draw_Town_2026.text((int(text_xOff)+126,-2), "Town  2026", font_size=13, stroke_width=0, fill=(51,105,255))
            for y in range(14):
                for x in range(28):
                    self.frame[x][y] = img.getpixel((x,y))
                    
                    #if img.getpixel((x,y)) == (255,255,255):
                    #    self.frame[x][y] = [255,255,255]
                    #else:
                    #    self.frame[x][y] = [0,0,0]
            #self.fix_pixel(text_xOff)
            text_xOff -= 1
            if text_xOff < -215:
                text_xOff = 28
            yield None

    def fix_pixel(self, text_xOff):
        pass
        #self.frame[][]

    def __init__(self,xsize=28, ysize=14, fps=30):
        self.name = "Text - \"Science Comes To Town 2026\""
        self.xsize = xsize
        self.ysize = ysize

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.text = self.set_text()
        self.scroll_wait = 0