import tkinter as tk
import color_functions as clr
import math, random, time, multiprocessing
from stopwatch import Stopwatch
from pyghthouse import Pyghthouse
import pyghthouse.utils as utils
from colorsys import hsv_to_rgb,rgb_to_hsv



class Dots(multiprocessing.Process):
    def stop(self):
        self._stop_event.set()
    
    @staticmethod
    def get_instance(xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 60, animspeed = 1.0):
        new_instance = Dots()
        new_instance._stop_event = multiprocessing.Event()
        new_instance.params(xsize, ysize, framequeue, commandqueue, fps, animspeed)
        return new_instance

    def params(self, xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 60, animspeed = 1.0) -> None:
        self.matrix = [[(0, 0, 0) for _ in range(ysize)] for _ in range(xsize)]
        self.lim_x = xsize-1
        self.lim_y = ysize-1
        self.queue = framequeue
        self.commands = commandqueue
        self.fps = fps
        #self.matrix = np.zeros((int(self.lim_x), int(self.lim_y), 3), dtype=np.uint8)
        self.orbs = []
        self.frametimer = Stopwatch()
        self.frametimer.set(1)
        self.quittimer = Stopwatch()
        self.quittimer.set(1)
        self.counter = 0
        

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


    
    def run(self):

        # initiliase all dots
        d1 = self.Dot(0,  0,  [86, 35 ,129], (1, 0.8))
        d2 = self.Dot(5,  2,  [228,49 ,23 ], (1, 0.7))
        d3 = self.Dot(10, 4,  [153,194,33 ], (1, 0.6))
        d4 = self.Dot(15, 6,  [106,172,218], (1, 0.5))
        d5 = self.Dot(20, 8,  [57 ,132,46 ], (0.5, 1))
        d6 = self.Dot(25, 10, [242,148,0  ], (0.6, 1))
        d7 = self.Dot(0,  12, [0,  103,124], (0.7, 1))
        d8 = self.Dot(5,  0,  [0,  61, 134], (0.8, 1))

        dots = [d1,d2,d3,d4,d5,d6,d7,d8]
                    
        
        while not self._stop_event.is_set():

            update_interval = 1/self.fps*4
            self.frametimer.set(update_interval)

            #for x in range(len(self.matrix)):
            #    for y in range(len(self.matrix[0])):
            #        #self.matrix[x][y] = self.process_pixel(self.matrix[x][y])
            #        a = x #if y % 2 == 0 else len(self.matrix) - x - 1
            #        self.matrix[a][y] = self.sequence_c((self.counter + (len(self.matrix)*y*0 + len(self.matrix[0])*x)*4 )%2048)
                    

            self.shadow(self.matrix)
        
            # Place all dots and move them
            for dot in dots:
                self.setColor(self.matrix, int(dot.x), int(dot.y), dot.color)
                dot.move()

            self.queue.put(self.get_matrix())
            self.counter = (self.counter + 4) % 2048

            if not self.commands.empty():
                self.commands.get_nowait()
                while not self.commands.empty():
                    self.commands.get_nowait()
                self.quittimer.set(1)
            elif self.quittimer.remaining_ms() == 0:
                print("No signal from control process. Quitting.")
                self._stop_event.set()
            
            wait = self.frametimer.remaining()
            
            time.sleep(wait)
        exit(0)
        
"""import main
if __name__ == "__main__":
    main.main("test")"""
    

