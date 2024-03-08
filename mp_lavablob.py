from stopwatch import Stopwatch
import color_functions as color
import math, random, multiprocessing, time
from pyghthouse import Pyghthouse

def timedither(factor = 1.0):
    if factor == 1: return True
    val = random.randint(1, int (10/factor))
    return val <= 10

def cartesian(direction, amount):
    x = amount * math.cos(direction)
    y = amount * math.sin(direction)
    return x, y
        
def polar(x, y):
    direction = math.atan2(y, x)
    if direction < 0:
        direction += 2 * math.pi
    amount = math.sqrt(x**2 + y**2)
    return direction, amount

class Lavablobs(multiprocessing.Process):
    
    class MovingObject:
        gravity = 0.0001
        
        def __init__(self, x, y, limx, limy) -> None:
            self.lim_x = limx
            self.lim_y = limy
            self.radius = 3.0
            self.x = x
            self.y = y
            self.color = (512, 192, 64)
            
            self.weight = 1.0
            
            self.heat_energy = -0.1

            self.speed_x = 0
            self.speed_y = 0
            
            self.deform_x = 0
            self.deform_y = 0

            self.bounce = False
            self.pyghthouse = None
            
        def set_pyghthouse(self, ph):
            self.pyghthouse = ph
                    
        def apply_heat(self):
            change = (self.lim_y / 2) - self.y
            change /= self.lim_y
            #print(change, self.heat_energy)
            self.heat_energy += 0.002 * change
            if abs(self.heat_energy) > 0.5:
                self.speed_y += self.heat_energy*0.1
                self.heat_energy *= 0.9
            else:
                self.speed_y += self.heat_energy*0.001
            
        def apply_gravity(self):
            if self.within_y_bounds():
                self.speed_y += self.gravity * self.weight
                
        def apply_loss(self):
            self.speed_x *= 0.9999
            self.speed_y *= 0.9999
            
        def collide(self, other):
            x_target, y_target = (self.x + self.speed_x), (self.y + self.speed_y)
            collision_radius = self.radius + other.radius
            xdist = abs(x_target - other.x)
            ydist = abs(y_target - other.x)
            distance = math.sqrt(xdist**2 + ydist**2)
            if distance < collision_radius and self != other:
                #print("collision")
                if other.x > self.x and abs(self.speed_x) < 0.005:
                    self.speed_x += 0.001 / xdist
                    #if self.within_x_bounds(self.x - 0.05):
                    #    self.x -= 0.01 / xdist
                elif abs(self.speed_x) < 0.01:
                    self.speed_x -= 0.001 / xdist
                    #if self.within_x_bounds(self.x + 0.05):
                    #    self.x += 0.01 / xdist
            
        def within_x_bounds(self, x = None):
            if not x: x = self.x
            return x > 0 and x < self.lim_x
        
        def within_y_bounds(self, y = None):
            if not y: y = self.y
            return y > 0 and y < self.lim_y

        def move(self):
            x_target, y_target = (self.x + self.speed_x), (self.y + self.speed_y)

            if self.within_x_bounds(x_target):
                self.x = x_target
            else:
                self.speed_x = -self.speed_x * 0.75

            if self.within_y_bounds(y_target):
                self.y = y_target
            else:
                self.speed_y = -self.speed_y * 0.25

        def plastic_bounce(self):
            if (not self.bounce) and self.speed_y < 0.2 and self.deform_y > 0.2:
                self.bounce = True
            elif self.bounce and self.deform_y > 0.001:
                self.speed_y += self.deform_y * 0.5
                self.deform_y *= 0.5
            
        def time_step(self):
            self.apply_loss()
            self.apply_gravity()
            #self.plastic_bounce()
            self.apply_heat()
            self.move()
            #print(self.x, self.y, self.deform_y, self.speed_y)

            
    def set_pyghthouse(self, username, token):
        self.ph_user = username
        self.ph_token = token
        
    def init_lighthouse(self):
        self.pyghthouse = Pyghthouse(self.ph_user, self.ph_token)
        self.pyghthouse.start()    
        
    def send_picture_to_lh(self, matrix):
        img = self.pyghthouse.empty_image()
        for x in range(len(img)):
            for y in range(len(img[0])):
                img[x][y] = matrix[y][x]
        self.pyghthouse.set_image(img)

    def params(self, xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 30, animspeed = 1.0) -> None:
        self.matrix = [[(0, 0, 0) for _ in range(ysize)] for _ in range(xsize)]
        self.lim_x = xsize-1
        self.lim_y = ysize-1
        self.queue = framequeue
        self.commands = commandqueue
        self.fps = fps
        self.animspeed = animspeed
        self.orbs = []
        self.frametimer = Stopwatch()
        self.frametimer.set(1)
        self.quittimer = Stopwatch()
        self.quittimer.set(1)
        for _ in range(32):
            self.add_blob()
            
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
                new[x][y] = color.gamma(color.wash(self.matrix[x][y]), 1)
        return self.collapse_matrix(new)
    
    def add_blob(self):
        x = random.uniform(0, self.lim_x)
        y = self.lim_y * random.randint(0, 1)
        elem = self.MovingObject(x, y, self.lim_x, self.lim_y)
        elem.weight = 1
        elem.radius = random.uniform(1.5, 3.5)
        elem.heat_energy = random.uniform(-0.5, 0.5)
        self.orbs.append(elem)

    
    def render_orb(self, orb):
        # Rendere den Orb auf der Matrix
        x, y = int(orb.x), int(orb.y)
        d = 2
        amount = (abs(orb.y - (orb.lim_y / 2)) / orb.lim_y)**2
        d = (1 + 1 * amount)
        for i in range( int(x - orb.radius*d), int(x + orb.radius*d + 1)):
            for j in range( int(y - orb.radius*d), int(y + orb.radius*d + 1)):
                if 0 <= i < len(self.matrix) and 0 <= j < len(self.matrix[0]):
                    distance = math.sqrt((i - orb.x) ** 2 + (j - orb.y) ** 2)
                    if distance <= orb.radius*d:
                        # Linearer Farbverlauf basierend auf Entfernung
                        orbcolor = color.gamma(orb.color, 1)
                        gradient_factor = 1 - min(distance / (orb.radius*d), 1.0)
                        gradient_color = color.interpolate(orbcolor, (0,0,0), gradient_factor)
                        #self.matrix[i][j] = color.add(gradient_color, self.matrix[i][j])
                        self.matrix[i][j] = color.brighten(gradient_color, self.matrix[i][j])
    
    def run(self):
        
        self.init_lighthouse()
        while True:
            
            update_interval = 1/self.fps
            self.frametimer.set(update_interval)
            
            for x in range(len(self.matrix)):
                for y in range(len(self.matrix[0])):
                    self.matrix[x][y] = color.decay(self.matrix[x][y], 0.02*self.animspeed)
                    
            for orb in self.orbs:           
                self.render_orb(orb)
                for orb2 in self.orbs:
                    orb.collide(orb2)
                orb.time_step()
                
            
            self.queue.put(self.get_matrix())
            self.send_picture_to_lh(self.get_matrix())

            if not self.commands.empty():
                self.commands.get_nowait()
                while not self.commands.empty():
                    self.commands.get_nowait()
                self.quittimer.set(1)
            elif self.quittimer.remaining_ms() == 0:
                print("No signal from control process. Quitting.")
                exit(0)
            
            wait = self.frametimer.remaining()
            
            time.sleep(wait)
        
import mp_view
if __name__ == "__main__":
    mp_view.main("lava")


