from queue import SimpleQueue
import tkinter as tk
import multiprocessing, time
from mp_firework import Fireworks
from mp_bouncers import BounceAnimation as Bouncers
from mp_lavablob import Lavablobs
from stopwatch import Stopwatch

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
        self.frames_queued = 1
        self.frames_displayed = 1
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


def update_canvas(canvas: ScalableCanvas, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, root):
    update_interval = 1 / canvas.fps_target
    canvas.timer.set(update_interval)
    
    if not framequeue.empty():
        canvas.delete("all") 
        canvas.frames_displayed += 1
        matrix = framequeue.get_nowait()
        matrix = stretch_matrix(matrix)
        canvas.create_rectangle(1 * canvas.scale_factor-1, 1 * canvas.scale_factor * canvas.y_distortion-1,
                                (len(matrix) + 1) * canvas.scale_factor + 1, (len(matrix[0]) + 2) * canvas.scale_factor * canvas.y_distortion + 1,
                                fill="black", outline="grey")
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                rgb = matrix[i][j]
                
                # Skip every 2nd row
                if j % 2 == 0 or max(rgb) < 5: continue
            
                x = i+1
                y = j+1
                canvas.create_rectangle(x * canvas.scale_factor, y * canvas.scale_factor * canvas.y_distortion,
                                        (x + 1) * canvas.scale_factor, (y + 1) * canvas.scale_factor * canvas.y_distortion,
                                        fill="#%02x%02x%02x" % rgb)
    
    commandqueue.put("keep_running")
    wait = canvas.timer.remaining_ms(1)
    root.after(wait, update_canvas, canvas, framequeue, commandqueue, root)
            

            
def main(animation = 0):
    root = tk.Tk()
    root.title("Lighthouse Animation")
    
    fps = 35

    canvas = ScalableCanvas(root, width=28, height=28, bg="black")
    canvas.pack(expand=tk.YES, fill=tk.BOTH)
    canvas.fps_target = fps + 1

    framequeue = multiprocessing.Queue()
    commandqueue = multiprocessing.Queue()
    match animation:
        case "fireworks":
            anim = Fireworks()
        case "lava":
            anim = Lavablobs()
        case _:
            anim = Bouncers()

    anim.params(28, 27, framequeue, commandqueue, fps=fps, animspeed = 1)
    anim.start()

    animation_interval = 100  # Intervall in Millisekunden
    root.after(animation_interval, update_canvas, canvas, framequeue, commandqueue, root)  # Erste Animation starten

    
    root.mainloop()
    
if __name__ == "__main__":
    main()

