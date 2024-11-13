from enum import Enum
import math
import color_functions as clr

class Shape(Enum):
    ORB    = 0
    SQUARE = 1
    LINE   = 2

class Renderbox:
        
    class Orb():
        def __init__(self, x_pos, y_pos, x_vector=0.0, y_vector=0.0, color=(255,0,0), health=-1,
                     animation_speed=1.0, colorshift=None, gravity=False, radius=2.0, fade_threshold=None,
                     enery_loss_factor=1.0, shape=0, y_render_scaling=0.85, rotation=0):
            self.y_render_scaling = y_render_scaling
            self.x_vector = x_vector
            self.y_vector = y_vector
            self.radius = radius
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.color = color
            self.colorshift = colorshift
            self.gravity = gravity
            self.loss_factor = enery_loss_factor
            self.hp_ticks = health
            self.fade_threshold = fade_threshold
            self.animation_speed = animation_speed
            self.shape = shape
            self.grid_size = math.ceil(self.radius*2) + (1 if shape==0 else 1)
            self.grid = [[0.0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
            self.rotation = rotation
            print(f"New orb spawned at {x_pos}, {y_pos}")
            
        def _move(self, free_space_map: list[list[int]]):
            if self.exists > 1:
                self.exists -= 1

            new_x = self.x_pos + self.x_vector * self.animation_speed
            new_y = self.y_pos + self.y_vector * self.animation_speed

            if new_x < 0 or new_x >= len(free_space_map) or not free_space_map[new_x][self.y_pos]: 
                self.x_vector = -self.x_vector
                self.x_pos = 0
            else:
                self.x_pos = new_x

            if new_y < 0 or new_y >= len(free_space_map[0]) or not free_space_map[self.x_pos][new_y]:
                self.y_vector = -self.y_vector
                self.y_pos = 0
            else: 
                self.y_pos = new_y      
            
        def _shift_color(self):
            self.color = clr.shift(self.color, self.colorshift)

        def _apply_g(self):
            g = self.gravity * self.animation_speed
            self.y_vector += g

        def _lose_energy(self):
            self.x_vector *= self.loss_factor
            self.y_vector *= self.loss_factor

        def _decay(self):
            if self.hp_ticks > 0:
                self.hp_ticks -= 1
            else:
                self.loss_factor = 0.97
                self.color = clr.decay(self.color, 0.03)
                r, g, b = self.color
                if r + g + b < 1:
                    self.is_dead = True
                    
        def teleport_to(self, new_x, new_y):
            self.x_pos, self.y_pos = new_x, new_y
        
        def time_tick(self, free_space_map: list[list[bool]]):
            """
            Lets the orb go through a single time tick.

            Args:
                free_space_map list[list[bool]]: A boolean grid that contains True when there is free space
            """
            if self.x_vector or self.y_vector:
                self._move(free_space_map)
            if self.gravity: 
                self._apply_g()
            if self.loss_factor < 1.0: 
                self._lose_energy()    
            if self.colorshift:
                self._shift_color()  
            if self.hp_ticks >= 0:
                self._decay()
                
        def brightness_factor(self, x1, x2, y1, y2):
            if self.shape == 0:  # Orb-shaped
                distance = math.sqrt(((x1 - x2)/self.y_render_scaling) ** 2 + (y1 - y2) ** 2)
                brightness = math.sqrt(max(0, self.radius - distance) / self.radius)
                
            elif self.shape == 1:  # Square-shaped
                x_proximity =  max(0, self.radius - abs(x1 - x2))
                y_proximity =  max(0, self.radius - abs(y1 - y2))
                brightness = min(x_proximity, y_proximity)
                
            else:  # Line-shaped
                rot = self.rotation
                dx = x1 - x2
                dy = y1 - y2
                # Berechne die projizierte Entfernung entlang der Linie
                distance_along_line = abs(dx * math.cos(rot) + dy * math.sin(rot))
                # Berechne die senkrechte Entfernung zur Linie
                distance_perpendicular = abs(dy * math.cos(rot) - dx * math.sin(rot))
                # Die Helligkeit sinkt entlang der senkrechten Entfernung zur Linie
                brightness = max(0, 1 - distance_perpendicular / self.radius)
            
            return brightness

        def get_indices(self) -> tuple[int]:
            """
            Calculates the starting/stopping indices of the render index

            Returns:
                tuple[int]: x, y
            """
            x_pos = int(self.x_pos) - int(self.grid_size * 0.5)
            y_pos = int(self.y_pos) - int(self.grid_size * 0.5)
            return (x_pos, y_pos)
                
        def get_grid(self) -> list[list[float]]:
            """
            Renders the object to a small grid. Each entry will be a float that is either 0 if outside of the
            object or a brightness value depending to proximity of the center if within the object.
            
            Returns:
                list[list[float]]: Grid containing opacity values
            """
            x_off=(self.x_pos) % 1 - 0.5
            y_off=(self.y_pos) % 1 - 0.5
            x_pos = self.grid_size * 0.5 + x_off
            y_pos = self.grid_size * 0.5 + y_off 
            for x_i in range(self.grid_size):
                for y_i in range(self.grid_size):
                    brightness = self.brightness_factor(x_pos, x_i, y_pos, y_i)
                    self.grid[x_i][y_i] = brightness
            return self.grid

x = Renderbox.Orb(0.5, 0.5, shape=0, radius=1)
for line in x.get_grid():
    print(" | ".join([str(min(int(brightness*10),9)) for brightness in line]))
print(x.get_indices())