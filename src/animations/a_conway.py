import numpy as np
from color_functions import cycle

class ConwaysGameOfLife():
    
    @staticmethod
    def get_instance(xsize, ysize, fps=10):
        new_instance = ConwaysGameOfLife()
        new_instance.params(xsize, ysize, fps)
        new_instance.grid = np.random.choice([0, 1], size=(xsize, ysize))
        new_instance.transition_grid = np.copy(new_instance.grid)  # Zielgrid für die Übergangsberechnung
        return new_instance

    def params(self, xsize, ysize, fps):
        self.name = "Conway's Game Of Life"
        self.grid = []
        self.transition_grid = []
        self.xsize = xsize
        self.ysize = ysize
        self.fps = None
        self.update_interval = 0.5  # 0.5 Sekunden für den nächsten Zustand
        self.fade_steps = int(fps * self.update_interval)*1  # Anzahl der Frames für die Überblendung
        self.counter = 0
        self.step = 0
        self.color = (255, 0, 0)
        
    def reset_grid(self):
        self.grid = np.random.choice([0, 1], size=(self.xsize, self.ysize))
        self.transition_grid = np.copy(self.grid) 
        
    def is_static(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] != self.transition_grid[i][j]:
                    return False
        return True
                
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

    def get_frame(self):
        self.color = cycle(self.color, 2)

        # Prüfen, ob es Zeit für das nächste Grid-Update ist
        if self.step >= self.fade_steps:
            self.update_grid()
            if self.is_static():
                print("Grid and transition grid are identical, resetting grid.")
                self.reset_grid()
            self.step = 0  # Zurücksetzen der Schritte für die Überblendung

        # Fade-Frame basierend auf dem aktuellen Schritt erzeugen und zur Queue hinzufügen
        self.step += 1
        return self.get_fade_frame(self.step)
