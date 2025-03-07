import tkinter as tk
import color_functions as clr
import math, random, time, multiprocessing
from stopwatch import Stopwatch
from pyghthouse import Pyghthouse
import pyghthouse.utils as utils
from colorsys import hsv_to_rgb,rgb_to_hsv



class ChildProtSymbol(multiprocessing.Process):
    def stop(self):
        self._stop_event.set()
    
    @staticmethod
    def get_instance(xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 60, animspeed = 1.0):
        new_instance = ChildProtSymbol()
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

        self.child_prot_symbol = [[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                  [0,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0],
                                  [0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,0],
                                  [0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,0],
                                  [0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0],
                                  [0,1,1,1,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1,1,1,0],
                                  [0,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,0],
                                  [0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0],
                                  [0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0],
                                  [0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0]]
        self.decay = False
        self.h = 0.535
        self.s = 0.6
        self.v = 1
        

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


    def smooth_bg(self):
        if (self.decay):
            if (self.v < 0.7):
                self.v = 0.7
                self.decay = False
            else:
                self.v -= 0.005

        else:
            if (self.v > 0.95):
                self.v = 0.95
                self.decay = True
            else:
                self.v += 0.005
    
    def run(self):
        # get empty img
        # img = Pyghthouse.empty_image()

        while not self._stop_event.is_set():

            update_interval = 1/self.fps*2
            self.frametimer.set(update_interval)
       
            
            self.smooth_bg()
            for y in range(14):
                for x in range(28):
                    if (self.child_prot_symbol[y][x]):
                        self.matrix[x][y] = utils.from_hsv(1,0,self.v*0.3+0.7)
                    else:
                        self.matrix[x][y] = utils.from_hsv(self.h, self.s, self.v)

            

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