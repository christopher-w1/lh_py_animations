import math
import time
import color_functions as clr
from stopwatch import Stopwatch
from PIL import Image, ImageDraw

class ScrollText():
    def stop(self):
        pass
    
    @staticmethod
    def get_instance(xsize, ysize, fps = 60, animspeed = 1.0):
        new_instance = ScrollText()
        new_instance.params(xsize, ysize, fps, animspeed)
        return new_instance

    def params(self, xsize, ysize, fps = 60, animspeed = 1.0) -> None:
        self.name = "Scrolling Text"
        self.matrix = [[(0, 0, 0) for _ in range(ysize)] for _ in range(xsize)]
        self.fps = fps
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                self.matrix[x][y] = (0, 0, 0)
        self.text_xOff = 28
        self.cau_color = (155,10,125)
        self.timer = Stopwatch()
        self.timer.set(5)
        self.view = 0
        self.framequeue = []

    def collapse_matrix(self, matrix):
        collapsed_matrix = []
        for x in range(len(matrix)):
            collapsed_matrix.append(matrix[x][:14])
        return collapsed_matrix
    
    def get_matrix(self):
        new = [row[:] for row in self.matrix]
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                #self.matrix[x][y] = color.dither(self.matrix[x][y], 10)
                new[x][y] = clr.clip(clr.wash(self.matrix[x][y]))
        return self.collapse_matrix(new)    
    

    def get_frame(self):
        if len(self.framequeue) > 1:
            return self.framequeue.pop(0)
        
        if len(self.framequeue) == 0:
            self.framequeue.append(self.generate_next_frame())

        frame_A = self.framequeue[0]
        frame_B = self.generate_next_frame()

        n_interframes = 4 # 0 1 2 3
        for i in range(n_interframes):
            factor = (i+1)/(n_interframes+1) if n_interframes > 1 else 0.5
            #factor = 0.5* factor + 0.5 * (0.5 * (math.sin(math.pi * (factor - 0.5)) + 1))
            interframe = []
            for x in range(len(frame_A)):
                row = []
                for y in range(len(frame_A[0])):
                    pixel_A = frame_A[x][y]
                    pixel_B = frame_B[x][y]
                    row.append(clr.interpolate(pixel_B, pixel_A, factor))
                interframe.append(row)
            self.framequeue.append(interframe)
        return self.framequeue.pop(0)



    def generate_next_frame(self):
        img = Image.new("RGB", (28,28))
        draw = ImageDraw.Draw(img)
        draw.fontmode = "1"
        if self.view == 0:
            draw.text((self.text_xOff,0), "CAU", font_size=12, stroke_width=0.2, fill=self.cau_color)
        elif self.view == 1:
            draw.multiline_text((self.text_xOff,-3), "NotP\n2025", font_size=9, spacing=-2)
        else:
            draw.text((self.text_xOff,0), "Mut!", font_size=12, stroke_width=0.2, fill=self.cau_color)
        img = img.transpose(Image.TRANSPOSE) # type: ignore
        pixels = list(img.getdata())
        width, height = img.size
        self.matrix = [pixels[i * width:(i+1)*width] for i in range(height)]

        if (self.view and self.text_xOff > 1) or (not self.view and self.text_xOff > 3) or self.timer.has_elapsed():
            self.text_xOff -= 1

        if self.text_xOff < -28:
            self.view = (self.view + 1) % 3
            self.text_xOff = 28
            self.timer.set(5)
        
        return self.get_matrix()

