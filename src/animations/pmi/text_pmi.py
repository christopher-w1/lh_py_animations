from PIL import Image, ImageDraw

class Text_PMI():
    @staticmethod
    def get_instance(xsize, ysize, fps=10):
        return Text_PMI(xsize,ysize,fps)
    
    def get_frame(self):
        next(self.text_PMI)
        return self.frame


    # Text: PMI
    def set_text_PMI(self):
        text_xOff = 3
        while True:
            img = Image.new("RGB", (28,14))
            draw = ImageDraw.Draw(img)
            draw.fontmode = "1"
            draw.text((int(text_xOff),-1), "PMI", font_size=12, stroke_width=0.2)
            for y in range(14):
                for x in range(28):
                    if img.getpixel((x,y)) == (255,255,255):
                        self.frame[x][y] = (255,255,255)
            next(self.colors)
            yield None

    
    def set_color(self):
        change_color = self.change_color()
        while True:
            for y in range(14):
                for x in range(28):
                    if self.frame[x][y] == (255,255,255):
                        color = next(change_color)
                        self.frame[x][y] = color
            yield None

    def change_color(self):
        
        while True:
            # red to grey
            color = [255,0,0]
            while color[0] >= 128:
                color[0] -= 0.1
                color[1] += 0.1
                color[2] += 0.1
                yield color
            # color = [127, 128, 128]
            
            # grey to blue
            color = [128, 128, 127]
            while color[0] >= 0:
                color[0] -= 0.1
                color[2] += 0.1
                yield color
            # color = [0, 128, 255]

            # blue to grey
            color = [0,128,255]
            while color[2] >= 128:
                color[0] += 0.1
                color[2] -= 0.1
                yield color
            # color = [128, 128, 127]

            # grey to red
            color = [127, 128, 128]
            while color[1] >= 0:
                color[0] += 0.1
                color[1] -= 0.1
                color[2] -= 0.1
                yield color
            # color = [255, 0, 0]


    def __init__(self,xsize=28, ysize=14, fps=10):
        self.name = "Text - PMI"
        self.xsize = xsize
        self.ysize = ysize
        
        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.text_PMI = self.set_text_PMI()
        self.colors = self.set_color()

        #self.bitmap(["0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000",
        #             "0000000000000000000000000000"])