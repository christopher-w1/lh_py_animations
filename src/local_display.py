import multiprocessing
import tkinter as tk

class LocalDisplay(tk.Tk):
    def __init__(self, framequeue, stop_event, fps=20):
        super().__init__()
        self.stop_event = stop_event
        self.framequeue = framequeue
        self.fps_target = fps
        self.scale_factor = 10
        self.y_distortion = 1.15
        self.current_frame = None
        self.title("Lighthouse Display")
        self.canvas = tk.Canvas(
            self, width=28 * self.scale_factor + 14,
            height=30 * self.scale_factor * self.y_distortion, bg="#1F1F1F"
        )
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.timer_interval = int(1000 / self.fps_target)
        self.after(10, self.update_display)
        
    def update_display(self):
        # Verarbeitet den neuesten Frame, falls vorhanden
        if not self.framequeue.empty():
            while not self.framequeue.empty():
                message = self.framequeue.get_nowait()
                
            if message:
                self.current_frame = message
            
            if self.current_frame:
                self.canvas.delete("all")
                self.draw_rects(self.current_frame)
        
        # Überprüfen, ob der Prozess gestoppt werden soll
        if self.stop_event.is_set():
            print("Display terminated!")
            self.destroy()
        else:
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

class DisplayProcess(multiprocessing.Process):
    def __init__(self, framequeue, fps=20):
        super().__init__()
        self.framequeue = framequeue
        self.stop_event = multiprocessing.Event()
        self.fps = fps
        self.display = None

    def run(self):
        self.display = LocalDisplay(self.framequeue, self.stop_event, self.fps)
        self.display.mainloop()

    def stop(self):
        self.stop_event.set()
        print("Stop signal set. Waiting for LocalDisplay to close.")
