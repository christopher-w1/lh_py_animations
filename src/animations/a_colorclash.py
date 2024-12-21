import color_functions as clr
import math, random
from color_functions import color_average, interpolate, hsv_to_rgb, multiply_val

class ColorClashAnimation():
    class Orb:
        def __init__(self, x, y, vecx, vecy, limx, limy, colorshift = 0, hue = None) -> None:
            self.lim_x = limx
            self.lim_y = limy
            self.move_x = vecx
            self.move_y = vecy
            self.radius = 2
            self.x = x
            self.y = y
            #self.color = color.rand_vibrant_color(3)
            self.color = clr.shift(clr.rand_rgb_color(3), random.randint(0, 360))
            if hue:
                self.color = multiply_val(hsv_to_rgb(hue, 100, 100), 2)
            self.colorshift = colorshift
            self.loss_factor = random.uniform(0.99, 0.999)
            self.is_dead = False
            self.exists = 10
            self.hp = random.randint(100, 1000)
            
        def bounceAction(self):
            self.is_dead = True

        def move(self) -> None:
            if self.exists > 1:
                self.exists -= 1

            new_x = self.x + self.move_x
            new_y = self.y + self.move_y

            # Bounce
            if new_x >= self.lim_x:
                self.move_x = 0 - self.move_x
                self.x = self.lim_x
                self.bounceAction()
                
            elif new_x <= 0: 
                self.move_x = 0 - self.move_x
                self.x = 0
                self.bounceAction()
                
            else:
                self.x = new_x

            if new_y >= self.lim_y:
                self.move_y = 0 - self.move_y
                self.y = self.lim_y
                self.bounceAction()
                
            elif new_y <= 0:
                self.move_y = 0 - self.move_y
                self.y = 0
                self.bounceAction()
                
            else: 
                self.y = new_y      

            self.lose_energy()    
            self.shift_color()  
            self.decay()
            

        def shift_color(self):
            self.color = clr.shift(self.color, self.colorshift)

        def apply_gravity(self):
            g = 0.03
            self.move_y += g

        def lose_energy(self):
            self.move_x *= self.loss_factor
            self.move_y *= self.loss_factor

        def decay(self):
            if math.sqrt(math.pow(self.move_x, 2) + math.pow(self.move_y, 2)) < 0.1:
                self.hp -= 50
            if self.hp > 0:
                self.hp -= 1
            else:
                self.loss_factor = 0.97
                self.color = clr.decay(self.color, 0.03)
                r, g, b, = self.color
                if r+g+b < 1:
                    self.is_dead = True

        def energize(self):
            energy = math.sqrt(math.pow(self.move_x, 2) + math.pow(self.move_y, 2))
            if energy < 1:
                self.loss_factor = 1.01
            elif energy > 3:
                self.loss_factor = 0.99

    def stop(self):
        self._stop_event.set()
        
    @staticmethod
    def get_instance(xsize, ysize, fps = 30, animspeed = 1.0):
        new_instance = ColorClashAnimation()
        new_instance.params(xsize, ysize, fps, animspeed)
        return new_instance

    def params(self, xsize, ysize, fps = 30, animspeed = 1.0) -> None:
        self.matrix = [[(0, 0, 0) for _ in range(ysize)] for _ in range(xsize)]
        self.blur_matrix = [[(0, 0, 0) for _ in range(ysize)] for _ in range(xsize)]
        self.lim_x = xsize-1
        self.lim_y = ysize-1
        self.fps = fps
        self.name = "Color Clash"
        self.orbs = []
        self.spawnmore = True
        for _ in range(5):
            self.add_rand_orb()
              

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
                new[x][y] = clr.wash(self.matrix[x][y])
        return self.collapse_matrix(new)

    
    def add_rand_orb(self):
        y = random.uniform(0, self.lim_y)
        colorshift = random.uniform(0.0, 1.0)*2
        vecy = 0
        x = 0
        vecx = random.uniform(0.1, 1)
        hue = random.randint(0, 360)
        self.orbs.append(self.Orb(x, y, vecx, vecy, self.lim_x, self.lim_y, colorshift, hue))
        
        x = self.lim_x
        vecx = 0 - vecx
        hue = (hue+180) % 360
        self.orbs.append(self.Orb(x, y, vecx, vecy, self.lim_x, self.lim_y, colorshift, hue))
        
    def add_rand_orb_2(self):
        y = random.uniform(0, self.lim_y)
        vecy = 0
        if random.randint(0, 1):
            x = 0
            vecx = random.uniform(0.1, 1)
            hue = random.randint(0, 180)
        else:
            x = self.lim_x
            vecx = random.uniform(-0.1, -1)
            hue = random.randint(181,360)
        colorshift = random.uniform(0.0, 1.0)*2
        self.orbs.append(self.Orb(x, y, vecx, vecy, self.lim_x, self.lim_y, colorshift, hue))
    
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
                        orbcolor = clr.gamma(orb.color, 1/orb.exists)
                        gradient_factor = 1 - min(distance / orb.radius, 1.0)
                        gradient_color = clr.interpolate(orbcolor, (0,0,0), gradient_factor)

                        self.matrix[i][j] = clr.brighten(gradient_color, self.matrix[i][j])
                        #self.matrix[i][j] = color.interpolate(gradient_color, self.matrix[i][j], 0.5)

    
    def get_frame(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                self.blur_matrix[x][y] = color_average([
                    self.matrix[max(0, min(x + i, len(self.matrix) - 1))][max(0, min(y + j, len(self.matrix[0]) - 1))]
                    for i in [-1, 0, 1]
                    for j in [-1, 0, 1]
                ])
                
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                self.matrix[x][y] = interpolate(self.matrix[x][y], self.blur_matrix[x][y], 0.9)
                self.matrix[x][y] = clr.shift(clr.decay(self.matrix[x][y], 0.001), 5)
                
        for orb in self.orbs:
            self.render_orb(orb)
            orb.move()
            if orb.is_dead:
                self.orbs.remove(orb)
                if self.spawnmore:
                    self.add_rand_orb()
                    self.add_rand_orb()
                    
        if len(self.orbs) > 15:
            self.spawnmore = False
        elif len(self.orbs) < 10:
            self.spawnmore = True
            
        return self.get_matrix()
    