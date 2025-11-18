import tkinter as tk
import color_functions as clr
import math, random, time, multiprocessing
from stopwatch import Stopwatch
from pyghthouse import Pyghthouse
import pyghthouse.utils as utils
from colorsys import hsv_to_rgb,rgb_to_hsv



class ChildProtSymbol(multiprocessing.Process):
    @staticmethod
    def get_instance(xsize, ysize, fps = 10):
        instance = ChildProtSymbol()
        instance.params()
        return instance

    def params(self) -> None:
        self.xsize = 14
        self.ysize = 28
        self.fps = 10
        self.name = "Tag der Kinderrechte - Schützende Hände"

        self.decay = False
        self.h = 0.535
        self.s = 0.6
        self.v = 1


    def get_frame(self):
        self.set_frame()
        return self.frame
    
    def set_frame(self):
        self.smooth_bg()
        for x in range(0, 28):
            for y in range(0, 14):
                if self.bitmap[y][x] == "1":
                    self.frame[x][y] = utils.from_hsv(1,0,self.v*0.3+0.7)
                else:
                    self.frame[x][y] = utils.from_hsv(self.h, self.s, self.v)


    def smooth_bg(self):
        if (self.decay):
            if (self.v < 0.7):
                self.v = 0.7
                self.decay = False
            else:
                self.v -= 0.001

        else:
            if (self.v > 0.95):
                self.v = 0.95
                self.decay = True
            else:
                self.v += 0.001


    def __init__(self, xsize=28, ysize=14, fps=10):
        self.name = "Tag der Kinderrechte - Schützende Hände"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmap = ["0000000000000110000000000000",
                       "0000000000001111000000000000",
                       "0000000000000110000000000000",
                       "0110000001111111111000000110",
                       "0110000000011111100000000110",
                       "0110000000011111100000000110",
                       "0110011000011001100001100110",
                       "0111000110011001100110001110",
                       "0111110011000000001100111110",
                       "0011111111100000011111111100",
                       "0000111111100000011111110000",
                       "0000001111110000111111000000",
                       "0000000011110000111100000000",
                       "0000000011110000111100000000"]