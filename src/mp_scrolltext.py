import color_functions as clr
import time, multiprocessing
from stopwatch import Stopwatch
from PIL import Image, ImageDraw

class ScrollText(multiprocessing.Process):
    def stop(self):
        self._stop_event.set()
    
    @staticmethod
    def get_instance(xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 60, animspeed = 1.0):
        new_instance = ScrollText()
        new_instance._stop_event = multiprocessing.Event()
        new_instance.params(xsize, ysize, framequeue, commandqueue, fps, animspeed)
        return new_instance

    def params(self, xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 60, animspeed = 1.0) -> None:
        self.matrix = [[(0, 0, 0) for _ in range(ysize)] for _ in range(xsize)]
        
        self.queue = framequeue
        self.commands = commandqueue
        self.fps = fps
        self.frametimer = Stopwatch()
        self.frametimer.set(1)
        self.quittimer = Stopwatch()
        self.quittimer.set(1)

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

    def run(self):
        global x
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                self.matrix[x][y] = (0, 0, 0)
        x = 28
        cau_color = (155,10,125)
        timer = Stopwatch()
        timer.set(5)
        
        show_cau = True
        while not self._stop_event.is_set():

            update_interval = 1/self.fps
            self.frametimer.set(update_interval)
            img = Image.new("RGB", (28,28))
            draw = ImageDraw.Draw(img)
            draw.fontmode = "1"
            if show_cau:
                draw.text((x,0), "CAU", font_size=12, stroke_width=0.2, fill=cau_color)
            else:
                draw.multiline_text((x,-3), "NotP\n2024", font_size=9, spacing=-2)#, fill=cau_color)
            img = img.transpose(Image.TRANSPOSE)
            pixels = list(img.getdata())
            width, height = img.size
            self.matrix = [pixels[i * width:(i+1)*width] for i in range(height)]
            if (show_cau and x > 1) or (not show_cau and x > 3) or timer.has_elapsed():
                x -= 0.25

            if x < -28:
                show_cau = not show_cau
                x = 28
                timer.set(5)
            
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
    main.main("test")"""
    

