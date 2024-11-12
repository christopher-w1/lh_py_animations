import color_functions as color
import math, random

class BounceAnimation:
    class Orb:
        def __init__(self, x, y, vecx, vecy, limx, limy, colorshift=0, animspeed=1.0):
            self.lim_x = limx
            self.lim_y = limy
            self.move_x = vecx
            self.move_y = vecy
            self.radius = 2
            self.x = x
            self.y = y
            self.color = color.shift(color.rand_rgb_color(3), random.randint(0, 360))
            self.colorshift = colorshift
            self.loss_factor = random.uniform(0.99, 0.999)
            self.is_dead = False
            self.exists = 10
            self.hp = random.randint(100, 1000)
            self.animspeed = animspeed

        def move(self):
            if self.exists > 1:
                self.exists -= 1

            new_x = self.x + self.move_x * self.animspeed
            new_y = self.y + self.move_y * self.animspeed

            # Bounce
            if new_x >= self.lim_x:
                self.move_x = -self.move_x
                self.x = self.lim_x
            elif new_x <= 0: 
                self.move_x = -self.move_x
                self.x = 0
            else:
                self.x = new_x

            if new_y >= self.lim_y:
                self.move_y = -self.move_y
                self.y = self.lim_y
            elif new_y <= 0:
                self.move_y = -self.move_y
                self.y = 0
            else: 
                self.y = new_y      

            self.apply_gravity()
            self.lose_energy()    
            self.shift_color()  
            self.decay()
            
        def shift_color(self):
            self.color = color.shift(self.color, self.colorshift)

        def apply_gravity(self):
            g = 0.03 * self.animspeed
            self.move_y += g

        def lose_energy(self):
            self.move_x *= self.loss_factor
            self.move_y *= self.loss_factor

        def decay(self):
            if math.sqrt(self.move_x ** 2 + self.move_y ** 2) < 0.1:
                self.hp -= 50 * self.animspeed
            if self.hp > 0:
                self.hp -= 1
            else:
                self.loss_factor = 0.97
                self.color = color.decay(self.color, 0.03)
                r, g, b = self.color
                if r + g + b < 1:
                    self.is_dead = True

    def get_instance(self, xsize, ysize, fps=30, animspeed=1.0):
        instance = BounceAnimation()
        instance.matrix = [[(0, 0, 0) for _ in range(ysize)] for _ in range(xsize)]
        instance.animspeed = animspeed
        instance.lim_x = xsize - 1
        instance.lim_y = ysize - 1
        instance.fps = fps
        instance._add_initial_orbs()
        return instance
    
    def __init__(self):
        self.name = "Bouncing Balls Animation"
        self.matrix = []
        self.animspeed = 0
        self.lim_x = 0
        self.lim_y = 0
        self.fps = 0
        self.orbs = []
        self.spawnmore = True

    def _add_initial_orbs(self):
        for _ in range(5):
            self._add_rand_orb()

    def get_frame(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                self.matrix[x][y] = color.shift(color.decay(self.matrix[x][y], 0.1), 0)

        for orb in self.orbs:
            self._render_orb(orb)
            orb.move()
            if orb.is_dead:
                self.orbs.remove(orb)
                if self.spawnmore:
                    self._add_rand_orb()
                    self._add_rand_orb()

        if len(self.orbs) > 25:
            self.spawnmore = False
        elif len(self.orbs) < 5:
            self.spawnmore = True

        output_matrix = [row[:] for row in self.matrix]
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                output_matrix[x][y] = color.wash(self.matrix[x][y])
        return self._collapse_matrix(output_matrix) 

    def _collapse_matrix(self, matrix):
        collapsed_matrix = []
        for x in range(len(matrix)):
            collapsed_row = []
            for y in range(0, len(matrix[0]), 2):
                pixel1 = matrix[x][y]
                pixel2 = matrix[x][min(y + 1, len(matrix[x]) - 1)]

                # Calc average of two pixels
                collapsed_pixel = (
                    (pixel1[0] + pixel2[0]) // 2,
                    (pixel1[1] + pixel2[1]) // 2,
                    (pixel1[2] + pixel2[2]) // 2
                )

                collapsed_row.append(collapsed_pixel)
            collapsed_matrix.append(collapsed_row)
        return collapsed_matrix

    def _add_rand_orb(self):
        x = random.uniform(0, self.lim_x)
        y = 1
        vecx = random.uniform(0.1, 1)
        vecy = random.uniform(0.1, 1.5)
        colorshift = random.uniform(0.0, 1.0) * 2
        self.orbs.append(self.Orb(x, y, vecx, vecy, self.lim_x, self.lim_y, colorshift, animspeed=self.animspeed))

    def _render_orb(self, orb):
        x, y = int(orb.x), int(orb.y)
        for i in range(x - orb.radius, x + orb.radius + 1):
            for j in range(y - orb.radius, y + orb.radius + 1):
                if 0 <= i < len(self.matrix) and 0 <= j < len(self.matrix[0]):
                    distance = math.sqrt((i - orb.x) ** 2 + (j - orb.y) ** 2)
                    if distance <= orb.radius:
                        orbcolor = color.gamma(orb.color, 1 / orb.exists)
                        gradient_factor = 1 - min(distance / orb.radius, 1.0)
                        gradient_color = color.interpolate(orbcolor, (0, 0, 0), gradient_factor)
                        self.matrix[i][j] = color.brighten(gradient_color, self.matrix[i][j])
