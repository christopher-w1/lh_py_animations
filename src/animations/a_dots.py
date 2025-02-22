import color_functions as clr
import time
from stopwatch import Stopwatch
import pyghthouse.utils as utils
from colorsys import hsv_to_rgb,rgb_to_hsv



class Dots():
    def stop(self):
        self._stop_event.set()
    
    @staticmethod
    def get_instance(xsize, ysize, fps = 60, animspeed = 1.0):
        new_instance = Dots()
        new_instance.params(xsize, ysize, fps)
        return new_instance

    def params(self, xsize, ysize, fps) -> None:
        self.matrix = [[(0, 0, 0) for _ in range(ysize)] for _ in range(xsize)]
        self.lim_x = xsize-1
        self.lim_y = ysize-1
        self.counter = 0
        self.frametimer = Stopwatch()
        self.name = "Moving Dots"
        self.fps = fps
        # initiliase all dots
        self.d1 = self.Dot(0,  0,  [86, 35 ,129], (1, 0.8))
        self.d2 = self.Dot(5,  2,  [228,49 ,23 ], (1, 0.7))
        self.d3 = self.Dot(10, 4,  [153,194,33 ], (1, 0.6))
        self.d4 = self.Dot(15, 6,  [106,172,218], (1, 0.5))
        self.d5 = self.Dot(20, 8,  [57 ,132,46 ], (0.5, 1))
        self.d6 = self.Dot(25, 10, [242,148,0  ], (0.6, 1))
        self.d7 = self.Dot(0,  12, [0,  103,124], (0.7, 1))
        self.d8 = self.Dot(5,  0,  [0,  61, 134], (0.8, 1))
        self.dots = [self.d1,self.d2,self.d3,self.d4,self.d5,self.d6,self.d7,self.d8]
        self.framebuffer = []
        

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


    class Dot:
        def __init__(self, x:float = 0, y:float = 0, color:list[int] = [255,0,0], vector = (0.5,0.5)):
            self.x = x
            self.y = y
            self.color = color
            # Vector is defined for the move func as (<change of x>, <change of y>). 
            # First move of the vector must be to a valid index
            self.vector = vector

        def move(self):
            self.checkValidMove()
            self.x += self.vector[0]
            self.y += self.vector[1]

        def checkValidMove(self):
            vector_x, vector_y = self.vector

            # check if next move is out of bounds
            if int(self.x + vector_x) < 0 or int(self.x + vector_x) > 27:
                self.vectorInvertX()

            if int(self.y + vector_y) < 0 or int(self.y + vector_y) > 13:
                self.vectorInvertY()

        def vectorInvertX(self):
            vector_x, vector_y = self.vector
            vector_x *= -1
            self.vector = (vector_x, vector_y)

        def vectorInvertY(self):
            vector_x, vector_y = self.vector
            vector_y *= -1
            self.vector = (vector_x, vector_y)

    def shadow(self, img:list):
        '''
        Mutates variable: img

        Shadow takes an img and reduce the brightness of all colors
        '''
        for y in range(len(img)):
            for x in range(len(img[0])):
                # Get current color in hsv
                r = img[y][x][0]
                g = img[y][x][1]
                b = img[y][x][2]

                h, s, v = rgb_to_hsv(r/255.0,g/255.0,b/255.0)

                # Reduce value (brightness)
                v = v - 0.08
                if v <= 0:
                    v = 0

                # Set new color
                img[y][x] = utils.from_hsv(h,s,v)



    def setColor(self, img:list, x:int, y:int, color:list[int]):
        '''
        Mutates variable: img

        Set a pixel with the new color combined with the previous color 
        '''
        # Get current color
        r = img[x][y][0]
        g = img[x][y][1]
        b = img[x][y][2]

        # Combine colors
        r += color[0]
        g += color[1]
        b += color[2]

        # Check if value is in bound
        if r > 255:
            r = 255

        if g > 255:
            g = 255

        if b > 255:
            b = 255

        # Set color
        img[x][y][0] = r
        img[x][y][1] = g
        img[x][y][2] = b


    
    def generate_next_frame(self):
        self.shadow(self.matrix)
    
        # Place all dots and move them
        for dot in self.dots:
            self.setColor(self.matrix, int(dot.x), int(dot.y), dot.color)
            dot.move()

        self.counter = (self.counter + 4) % 2048
        return self.get_matrix()
    
    def get_frame(self):
        if len(self.framebuffer) > 1:
            return self.framebuffer.pop(0)
        
        if len(self.framebuffer) == 0:
            self.framebuffer.append(self.generate_next_frame())

        frame_A = self.framebuffer[0]
        frame_B = self.generate_next_frame()

        n_interframes = 3
        for i in range(n_interframes):
            factor = (i+1)/(n_interframes+1) if n_interframes > 1 else 0.5
            interframe = []
            for x in range(len(frame_A)):
                row = []
                for y in range(len(frame_A[0])):
                    pixel_A = frame_A[x][y]
                    pixel_B = frame_B[x][y]
                    row.append(clr.interpolate(pixel_B, pixel_A, factor))
                interframe.append(row)
            self.framebuffer.append(interframe)
        return self.framebuffer.pop(0)

