import tkinter as tk
import color_functions as clr
import math, random, time, multiprocessing
from stopwatch import Stopwatch
from pyghthouse import Pyghthouse

class RainAnimation(multiprocessing.Process):
    class Drop:
        def __init__(self, x, y, vecx, vecy, limx, limy, colorshift = 0) -> None:
            self.lim_x = limx
            self.lim_y = limy
            self.move_x = vecx
            self.move_y = vecy
            self.radius = 1
            self.x = x
            self.y = y
            #self.color = color.rand_vibrant_color(3)
            #self.color = color.rand_metal_color(2)
            self.color = clr.rand_faculty_color(2)
            self.colorshift = colorshift
            self.loss_factor = random.uniform(0.99, 0.999)
            self.alive = True

        def move(self) -> None:

            new_x = self.x + self.move_x
            new_y = self.y + self.move_y

            # Bounce
            if new_x >= self.lim_x:
                self.move_x = 0 - self.move_x
                self.x = self.lim_x
                #self.shift_color()
            elif new_x <= 0: 
                self.move_x = 0 - self.move_x
                self.x = 0
                #self.shift_color()
            else:
                self.x = new_x

            if new_y >= self.lim_y:
                self.move_y = 0 - self.move_y
                self.y = self.lim_y
                self.alive = False
                
            elif new_y <= 0:
                self.move_y = 0 - self.move_y
                self.y = 0
                #self.shift_color()
            else: 
                self.y = new_y      
  
            self.shift_color()  
            

        def shift_color(self):
            self.color = clr.shift(self.color, self.colorshift)

        
    def stop(self):
        self._stop_event.set()
        
    @staticmethod
    def get_instance(xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 30, animspeed = 1.0):
        new_instance = RainAnimation()
        new_instance._stop_event = multiprocessing.Event()
        new_instance.params(xsize, ysize, framequeue, commandqueue, fps, animspeed)
        return new_instance
        
    def params(self, xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 30, animspeed = 1.0) -> None:
        self.matrix = [[(0.0, 0.0, 0.0) for _ in range(ysize)] for _ in range(xsize)]
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
        self.spawnmore = True

    def collapse_matrix(self, matrix):
        collapsed_matrix = []
        for x in range(len(matrix)):
            collapsed_row = []
            for y in range(0, len(matrix[0]), 2):
                pixel1 = matrix[x][y]
                pixel2 = matrix[x][min(y + 1, len(matrix[x])-1)]

                # Calc average of two pixels
                collapsed_pixel = (
                    (pixel1[0] + pixel2[0]) // 2,
                    (pixel1[1] + pixel2[1]) // 2,
                    (pixel1[2] + pixel2[2]) // 2
                )

                collapsed_row.append(collapsed_pixel)
            collapsed_matrix.append(collapsed_row)
        return collapsed_matrix
    
    def get_matrix(self):
        new = [row[:] for row in self.matrix]
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                #self.matrix[x][y] = color.dither(self.matrix[x][y], 10)
                color = clr.from_float(self.matrix[x][y])
                new[x][y] = clr.wash(color)
        return self.collapse_matrix(new)

    
    def add_rand_orb(self):
        x = random.uniform(0, self.lim_x)
        y = 1 #random.uniform(0, self.lim_y)
        vecx = 0# random.uniform(0.1, 1)
        vecy = random.uniform(0.5, 1.0)
        colorshift = random.uniform(0.0, 1.0)*2
        self.orbs.append(self.Drop(x, y, vecx, vecy, self.lim_x, self.lim_y, colorshift))
    
    def render_orb(self, orb):
        # Rendere den Orb auf der Matrix mit seiner aktuellen Position
        x, y = int(orb.x), int(orb.y)
        #print(f"Orb at {x} {y}")
        for i in range(x - orb.radius, x + orb.radius + 1):
            for j in range(y - orb.radius, y + orb.radius + 1):
                if 0 <= i < len(self.matrix) and 0 <= j < len(self.matrix[0]):
                    distance = math.sqrt((i - orb.x) ** 2 + (j - orb.y) ** 2)
                    if distance <= orb.radius:
                        ###self.matrix[i][j] = color.brighten(orb.color, self.matrix[i][j])
                        # Linearer Farbverlauf basierend auf der Entfernung
                        orbcolor = orb.color
                        gradient_factor = 1 - min(distance / orb.radius, 1.0)
                        gradient_color = clr.interpolate(orbcolor, (0,0,0), gradient_factor)
                        gradient_color = clr.from_float(gradient_color)
                        self.matrix[i][j] = clr.brighten(gradient_color, self.matrix[i][j])
    
    def run(self):
        
        spawn_intervall = 100
        
        while not self._stop_event.is_set():

            update_interval = 1/self.fps
            self.frametimer.set(update_interval)

            for x in range(len(self.matrix)):
                for y in range(len(self.matrix[0])):
                    self.matrix[x][y] = clr.shift(clr.decay(self.matrix[x][y], 1/16), 0)
                    
            for orb in self.orbs:
                self.render_orb(orb)
                orb.move()
                if not orb.alive:
                    self.orbs.remove(orb)
                        
            spawn_intervall -= 1
            if spawn_intervall < 1:
                spawn_intervall = 3
                self.add_rand_orb()
                
            
            self.queue.put(self.get_matrix())

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
    main.main("rain")"""