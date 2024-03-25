from queue import SimpleQueue
import tkinter as tk
import os
import multiprocessing, time
from pyghthouse.ph import Pyghthouse
import pyghthouse.utils as utils
from mp_firework import Fireworks
from mp_bouncers import BounceAnimation as Bouncers
from mp_lavablob import Lavablobs
from mp_rgbtest import RgbTest
from mp_rain import RainAnimation
from stopwatch import Stopwatch


username = os.getenv('LIGHTHOUSE_USER')
token = os.getenv('LIGHTHOUSE_TOKEN')

class ScalableCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.original_width = 28
        self.original_height = 28
        self.scale_factor = 10
        self.y_distortion = 1
        self.scale_canvas(self.scale_factor)
        self.localqueue = SimpleQueue()
        self.fps_target = 10
        self.started = time.monotonic()
        self.timer = Stopwatch()
        self.timer.set(10)

    def scale_canvas(self, factor):
        self.scale_factor = factor
        self.config(width=self.original_width * factor, height=self.original_height * factor * self.y_distortion)
        self.master.geometry(f"{int((self.original_width + 2) * factor)}x{int((self.original_height + 3) * factor * self.y_distortion)}")

    def reset_counter(self):
        anim_fps = self.frames_queued / (time.monotonic() - self.started)
        view_fps = self.frames_displayed / (time.monotonic() - self.started)
        self.frames_queued = anim_fps
        self.frames_displayed = view_fps
        self.started = time.monotonic()-1
        
        
def stretch_matrix(matrix):
    stretched_matrix = []

    for row in matrix:
        stretched_row = []
        for pixel in row:
            stretched_row.append(pixel)
            stretched_row.append(pixel)  # Füge den Pixel noch einmal hinzu, um ihn zu strecken
        stretched_matrix.append(stretched_row)

    return stretched_matrix

def draw_rects(canvas: ScalableCanvas, matrix: tuple[int, int, int]):
     
    # Draw outline
    canvas.create_rectangle(1 * canvas.scale_factor-1, 1 * canvas.scale_factor * canvas.y_distortion-1,
                                (len(matrix) + 1) * canvas.scale_factor + 1, 2 * (len(matrix[0]) + 1) * canvas.scale_factor * canvas.y_distortion + 1,
                                fill="black", outline="grey")
    
    # Iterate through matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):

            # Extract color
            rgb = matrix[i][j]
            
            # Add offset
            x = i + 1
            y = 2 * (j + 1)

            # Draw colored rectangle
            canvas.create_rectangle(x * canvas.scale_factor, y * canvas.scale_factor * canvas.y_distortion,
                                    (x + 1) * canvas.scale_factor, (y + 1) * canvas.scale_factor * canvas.y_distortion,
                                    fill="#%02x%02x%02x" % rgb)


def update_canvas(canvas: ScalableCanvas, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, root):

    # Prepare timing parameters
    update_interval = 1 / (canvas.fps_target)
    canvas.timer.set(update_interval)
    wait = 1
    
    # Check if we have new frames
    if not framequeue.empty():

        # Get the newest frame that is ready
        matrix = framequeue.get()
        while not framequeue.empty(): 
            matrix = framequeue.get_nowait()

        # Draw matrix as rectangles on canvas
        canvas.delete("all")
        draw_rects(canvas, matrix)
        
        # Keep animation process running
        commandqueue.put("keep_running")

        # Wait remaining time until the next frame is needed
        wait = canvas.timer.remaining_ms(1)

    root.after(wait, update_canvas, canvas, framequeue, commandqueue, root)
            

            
def main(animation = 0):
    root = tk.Tk()
    root.title("Lighthouse Animation")
    
    fps = 30

    canvas = ScalableCanvas(root, width=28, height=28, bg="black")
    canvas.pack(expand=tk.YES, fill=tk.BOTH)
    canvas.fps_target = fps

    framequeue = multiprocessing.Queue()
    commandqueue = multiprocessing.Queue()
    match animation:
        case "fireworks":
            anim = Fireworks()
        case "lava":
            anim = Lavablobs()
        case "test":
            anim = RgbTest()
        #case "test2":
            #anim = RgbTest2()
        case "rain":
            anim = RainAnimation()
        case _:
            anim = Bouncers()

    anim.params(28, 27, framequeue, commandqueue, fps=fps, animspeed = 1)
    anim.set_pyghthouse(username, token)
    anim.start()

    animation_interval = 100  # Intervall in Millisekunden
    root.after(animation_interval, update_canvas, canvas, framequeue, commandqueue, root)  # Erste Animation starten

    
    root.mainloop()
    
if __name__ == "__main__":
    print("Pick an animation:")
    print("fireworks, lava, test, rain, bouncy_orbs")
    x = input()
    main(x)

