import multiprocessing
import time
import random
import numpy as np
from color_functions import cycle

class GameOfLife(multiprocessing.Process):
    def stop(self):
        self._stop_event.set()
    
    @staticmethod
    def get_instance(xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps=10):
        new_instance = GameOfLife()
        new_instance._stop_event = multiprocessing.Event()
        new_instance.params(xsize, ysize, framequeue, commandqueue, fps)
        return new_instance

    def params(self, xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps=10):
        # Initialisiere ein 14x28 Raster zufällig
        self.grid = np.random.choice([0, 1], size=(xsize, ysize))
        self.xsize = xsize
        self.ysize = ysize
        self.framequeue = framequeue
        self.commandqueue = commandqueue
        self.fps = fps
        self.update_interval = 0.5  # 0.5 Sekunden für den nächsten Zustand
        self.fade_steps = int(fps * self.update_interval)*1  # Anzahl der Frames für die Überblendung
        self.transition_grid = np.copy(self.grid)  # Zielgrid für die Übergangsberechnung
        self.counter = 0
        self.color = (255, 0, 0)
        
    def reset_grid(self):
        self.grid = np.random.choice([0, 1], size=(self.xsize, self.ysize))
        self.transition_grid = np.copy(self.grid) 

    def count_neighbors(self, x, y):
        neighbors = [
            (x-1, y-1), (x-1, y), (x-1, y+1),
            (x, y-1),           (x, y+1),
            (x+1, y-1), (x+1, y), (x+1, y+1)
        ]
        count = 0
        for nx, ny in neighbors:
            if 0 <= nx < self.xsize and 0 <= ny < self.ysize:
                count += self.grid[nx, ny]
        return count

    def update_grid(self):
        # Berechnet den nächsten Zustand des Grids
        self.grid = np.copy(self.transition_grid)
        new_grid = np.copy(self.grid)
        for x in range(self.xsize):
            for y in range(self.ysize):
                alive = self.grid[x, y] == 1
                neighbors = self.count_neighbors(x, y)
                
                if alive and (neighbors < 2 or neighbors > 3):
                    new_grid[x, y] = 0  # Zelle stirbt
                elif not alive and neighbors == 3:
                    new_grid[x, y] = 1  # Zelle wird geboren
        self.transition_grid = new_grid  # Übergangsziel setzen

    def get_fade_frame(self, step):
        # Interpoliert zwischen dem aktuellen Grid und dem Ziel-Grid für eine sanfte Überblendung
        alpha = step / self.fade_steps
        fade_frame = np.zeros((self.xsize, self.ysize, 3), dtype=int)
        for x in range(self.xsize):
            for y in range(self.ysize):
                start_color= self.color if self.grid[x, y] == 1 else (0, 0, 0)
                end_color = self.color if self.transition_grid[x, y] == 1 else (0, 0, 0)
                
                # Linearer Übergang zwischen start_color und end_color
                fade_color = tuple(int(start * (1 - alpha) + end * alpha) for start, end in zip(start_color, end_color))
                fade_frame[x, y] = fade_color
        return fade_frame.tolist()

    def run(self):
        step = 0  # Übergangsschritte
        
        while not self._stop_event.is_set():
            
            self.color = cycle(self.color, 2)

            # Prüfen, ob es Zeit für das nächste Grid-Update ist
            if step >= self.fade_steps:
                self.update_grid()
                if np.array_equal(self.grid, self.transition_grid):
                    print("Grid and transition grid are identical, resetting grid.")
                    self.reset_grid()
                step = 0  # Zurücksetzen der Schritte für die Überblendung

            # Fade-Frame basierend auf dem aktuellen Schritt erzeugen und zur Queue hinzufügen
            self.framequeue.put(self.get_fade_frame(step+1))
            step += 1
            
            
            # Stop-Befehl abfangen
            if not self.commandqueue.empty():
                command = self.commandqueue.get_nowait()
                if command == "STOP":
                    print("Received STOP command. Exiting Game of Life.")
                    break

            # Warten, um die Ziel-FPS zu erreichen
            time.sleep(1 / self.fps)

        print("Game of Life subprocess stopped.")
        exit(0)
