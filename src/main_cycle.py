from queue import SimpleQueue
import tkinter as tk
import multiprocessing, time
from pyghthouse.ph import Pyghthouse
import pyghthouse.utils as utils
from mp_firework import Fireworks
from mp_bouncers import BounceAnimation as Bouncers
from mp_lavablob import Lavablobs
from mp_rgbtest import RgbTest
from mp_rain import RainAnimation
from mp_rebound import ReboundAnimation
from mp_diffraction import DiffAnimation
from stopwatch import Stopwatch

# Initialisiere den globalen Timer
timer = Stopwatch()

def read_auth(filename="auth.txt"):
    # Funktion zum Einlesen der Authentifizierungsdaten
    with open(filename) as src:
        username, token = None, None
        lines = src.readlines()
        for line in lines:
            line = line.split(":")
            if len(line) == 2:
                match line[0].strip().lower():
                    case 'name':
                        username = line[1].strip()
                        print(f"Username read from file: {username}")
                    case 'token':
                        token = line[1].strip()
                        print(f"Token read from file: {token}")
                    case _:
                        print(f"Unrecognized Key: '{line[0]}'")
        if not username or not token:
            print(f"Error: File {filename} is incomplete!")
        return username, token

class ScalableCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.original_width = 28
        self.original_height = 28
        self.scale_factor = 10
        self.y_distortion = 1.2
        self.scale_canvas(self.scale_factor)
        self.localqueue = SimpleQueue()
        self.fps_target = 10
        self.started = time.monotonic()
        self.timer = Stopwatch()
        self.timer.set(10)

    def scale_canvas(self, factor):
        # Funktion zum Skalieren des Canvas
        self.scale_factor = factor
        self.config(width=self.original_width * factor, height=self.original_height * factor * self.y_distortion)
        self.master.geometry(f"{int((self.original_width + 2) * factor)}x{int((self.original_height + 3) * factor * self.y_distortion)}")

    def reset_counter(self):
        # Funktion zum Zurücksetzen des FPS-Zählers
        anim_fps = self.frames_queued / (time.monotonic() - self.started)
        view_fps = self.frames_displayed / (time.monotonic() - self.started)
        self.frames_queued = anim_fps
        self.frames_displayed = view_fps
        self.started = time.monotonic()-1

def stretch_matrix(matrix):
    # Funktion zum Strecken der Matrix
    stretched_matrix = []
    for row in matrix:
        stretched_row = []
        for pixel in row:
            stretched_row.append(pixel)
            stretched_row.append(pixel)  # Füge den Pixel noch einmal hinzu, um ihn zu strecken
        stretched_matrix.append(stretched_row)
    return stretched_matrix

def draw_rects(canvas: ScalableCanvas, matrix: tuple[int, int, int]):
    # Funktion zum Zeichnen von Rechtecken auf dem Canvas
    canvas.create_rectangle(1 * canvas.scale_factor-1, 1 * canvas.scale_factor * canvas.y_distortion-1,
                            (len(matrix) + 1) * canvas.scale_factor + 1, 2 * (len(matrix[0]) + 1) * canvas.scale_factor * canvas.y_distortion + 1,
                            fill="black", outline="grey")
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            rgb = matrix[i][j]
            x = i + 1
            y = 2 * (j + 1)
            canvas.create_rectangle(x * canvas.scale_factor, y * canvas.scale_factor * canvas.y_distortion,
                                    (x + 1) * canvas.scale_factor, (y + 1) * canvas.scale_factor * canvas.y_distortion,
                                    fill="#%02x%02x%02x" % rgb)

def cycle_animation(anim_list, anim_index, framequeue, commandqueue, username, token):
    # Funktion zum Wechseln der Animation
    new_anim = anim_list[anim_index]
    anim_index = (anim_index + 1) % len(anim_list)  # Gehe zur nächsten Animation
    new_anim.set_pyghthouse(username, token)
    new_anim.start()
    return anim_index

def update_canvas(canvas: ScalableCanvas, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, root, anim_list, anim_index, username, token):

    update_interval = 1 / canvas.fps_target * 3
    canvas.timer.set(update_interval)
    wait = 1
    
    if not framequeue.empty():
        matrix = framequeue.get()
        while not framequeue.empty(): 
            matrix = framequeue.get_nowait()
        canvas.delete("all")
        draw_rects(canvas, matrix)
        
        # Prüfe, ob 10 Sekunden abgelaufen sind und die Animation gewechselt werden soll
        if timer.has_elapsed():
            anim_index = cycle_animation(anim_list, anim_index, framequeue, commandqueue, username, token)
            timer.set(10)  # Setze den Timer zurück

        commandqueue.put("keep_running")
        wait = canvas.timer.remaining_ms(1)

    root.after(wait, update_canvas, canvas, framequeue, commandqueue, root, anim_list, anim_index, username, token)

def main(animation=None):
    username, token = read_auth()
    if not username or not token:
        exit(1)
    
    # Liste der Animationen
    anim_list = [Fireworks(), Lavablobs(), RgbTest(), RainAnimation(), Bouncers(), ReboundAnimation(), DiffAnimation()]
    anim_index = 0  # Startindex der Animation

    fps = 40
    global timer
    timer.set(10)  # Initialer Timer für 10 Sekunden

    framequeue = multiprocessing.Queue()
    commandqueue = multiprocessing.Queue()
    anim = anim_list[anim_index]
    
    root = tk.Tk()
    root.title("Lighthouse Animation")
    canvas = ScalableCanvas(root, width=28, height=28, bg="black")
    canvas.pack(expand=tk.YES, fill=tk.BOTH)
    canvas.fps_target = fps
    root.after(100, update_canvas, canvas, framequeue, commandqueue, root, anim_list, anim_index, username, token)

    anim.params(28, 27, framequeue, commandqueue, fps=fps, animspeed = 1)
    anim.set_pyghthouse(username, token)
    anim.start()
    root.mainloop()

if __name__ == "__main__":
    main()
