from PIL import Image, ImageDraw
import pathlib,os

class Bowel():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        return Bowel(xsize,ysize,fps)

    def get_frame(self):
        return self.frame

    def __init__(self,xsize=28, ysize=14, fps=30):
        self.name = "IBD - Bowel"
        self.xsize = xsize
        self.ysize = ysize

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        img = Image.open(os.path.join(pathlib.Path(__file__).parent,'bowel.png'))
        for y in range(0, 28, 2):
            for x in range(28):
                (r,g,b,a) = img.getpixel((x,y))
                self.frame[x][y//2] = [r,g,b]
