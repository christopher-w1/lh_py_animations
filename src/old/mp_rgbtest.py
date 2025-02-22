import tkinter as tk
import color_functions as clr
import math, random, time, multiprocessing
from stopwatch import Stopwatch
from pyghthouse import Pyghthouse

class RgbTest(multiprocessing.Process):
    def stop(self):
        self._stop_event.set()
    
    @staticmethod
    def get_instance(xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 60, animspeed = 1.0):
        new_instance = RgbTest()
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

    def process_pixel(self, pixel):
        r, g, b = pixel
        
        if r == g and r == b and r > 0:
            r -= 5
            g -= 5
            b -= 5
        elif r <= 0 and g <= 0 and b <= 0:
            r = 255
            g = 0
            b = 0
        elif r > 0 and g >= 0 and b <= 0:
            r -= 5
            g += 5
        elif r <= 0 and g > 0 and b >= 0:
            g -= 5
            b += 5
        elif r <= 255 and g <= 255 and b >= 255:
            r += 5
            g += 5
        else:
            r += 1
            g += 1
            b += 1
        
        return (r, g, b)
    
    def sequence(self, counter):
        r, g, b = 0, 0, 0
        
        if counter < 256:
            r = counter
        elif counter < 512:
            r = 255
            g = counter - 255
        elif counter < 768:
            r = 767 - counter
            g = 255
            b = counter - 511
        elif counter < 1024:
            g = 1023 - counter
            b = 255
        elif counter < 1280:
            b = 1279 - counter
        elif counter < 1536:
            r = counter - 1279
            g = r
            b = r
        elif counter < 2048:
            r = 2047-counter
            g = r
            b = r
            
        return (r, g, b)      
          
    def sequence_b(self, counter):
        r, g, b = 0, 0, 0
        
        if counter < 256:
            r = counter
        elif counter < 512:
            r = 255
            g = counter - 255
        elif counter < 768:
            r = 255
            g = 255
            b = counter - 511
        elif counter < 1024:
            r = 1023 - counter
            g = 255
            b = 255
        elif counter < 1280:
            g = 1279 - counter
            b = 255
        elif counter < 1536:
            b = 1535 - counter
            
    def sequence_c(self, counter):
        r, g, b = 0, 0, 0
        
        if counter < 256:
            r = 255
            g = 255
            b = 255
        elif counter < 512:
            r = 255
        elif counter < 768:
            g = 255
        elif counter < 1024:
            b = 255
            
        return (r, g, b)        
    
    def run(self):
        for x in range(len(self.matrix)):
                for y in range(len(self.matrix[0])):
                    pixel = (255, 255, 255)
                    
                    self.matrix[x][y] = pixel
                    
        
        while not self._stop_event.is_set():

            update_interval = 1/self.fps
            self.frametimer.set(update_interval)

            for x in range(len(self.matrix)):
                for y in range(len(self.matrix[0])):
                    #self.matrix[x][y] = self.process_pixel(self.matrix[x][y])
                    a = x #if y % 2 == 0 else len(self.matrix) - x - 1
                    self.matrix[a][y] = self.sequence_c((self.counter + (len(self.matrix)*y*0 + len(self.matrix[0])*x)*4 )%2048)
                    
                    
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
    

