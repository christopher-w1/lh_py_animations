import tkinter as tk
import time

class LocalDisplay(tk.Tk):
    def __init__(self, framequeue, fps=20):
        super().__init__()
        self.framequeue = framequeue
        self.fps_target = fps
        self.scale_factor = 10
        self.y_distortion = 1.15
        self.current_frame = None
        self.title("Lighthouse Display")
        self.canvas = tk.Canvas(self, width=28 * self.scale_factor + 14, height=28 * self.scale_factor * self.y_distortion + 20, bg="black")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.timer_interval = int(1000 / self.fps_target)
        self.after(self.timer_interval, self.update_display)

    def update_display(self):
        # Wenn neue Frames vorhanden sind, wird der neueste verarbeitet
        if not self.framequeue.empty():
            while not self.framequeue.empty():
                message = self.framequeue.get_nowait()
                if message == "stop":
                        self.destroy()
                        return
            
            if message:
                self.current_frame = message
            
            if self.current_frame:
                self.canvas.delete("all")
                self.draw_rects(self.current_frame)
        
        self.after(self.timer_interval, self.update_display)

    def draw_rects(self, matrix):
        for j, row in enumerate(matrix):
            for i, rgb in enumerate(row):
                x, y = (i + 1), 2 * (j + 1)
                r, g, b = rgb
                self.canvas.create_rectangle(
                    x * self.scale_factor, y * self.scale_factor * self.y_distortion,
                    (x + 1) * self.scale_factor, (y + 1) * self.scale_factor * self.y_distortion,
                    fill="#%02x%02x%02x" % (int(r), int(g), int(b))
                )
                

def start_local_display(framequeue, fps=20):
    display = LocalDisplay(framequeue, fps)
    display.mainloop()