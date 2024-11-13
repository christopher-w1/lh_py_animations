from stopwatch import Stopwatch
import color_functions as clr
import math, random, multiprocessing, time
from pyghthouse import Pyghthouse

X_Scale = 0.7
BRIGHTNESS = 0.5
GAMMA = 1.5
PRESERVE_COLOR = 0.5

class Fireworks(multiprocessing.Process):
    class Orb():
        def __init__(self, x, y, vecx, vecy, limx, limy, colorshift = 0, motor = False, fps = 30, spd=1.0) -> None:
            self.lim_x = limx
            self.lim_y = limy
            self.move_x = vecx
            self.move_y = vecy
            self.radius = 2
            self.x = x
            self.y = y
            #self.color = color.rand_vibrant_color2(random.uniform(2.5, 3.5))
            self.color = clr.rand_metal_color(random.uniform(2.5, 3.5))
            self.colorshift = colorshift
            self.loss_factor = random.uniform(0.99, 0.999)
            self.is_dead = False
            self.blend_in = 10
            self.hp = random.randint(50, 70)
            self.level = 2
            self.weight = 1
            self.motor = motor
            self.pyghthouse = None
            self.animspeed = spd
            
        def set_pyghthouse(self, ph):
            self.pyghthouse = ph

        def getData(self):
            return self.x, self.y, self.move_x, self.move_y, self.color, self.level

        def move(self) -> None:
            if self.blend_in > 1:
                self.blend_in -= 1

            new_x = self.x + self.move_x*self.animspeed
            new_y = self.y + self.move_y*self.animspeed

            if new_y >= self.lim_y:
                self.move_y = 0
                self.move_x /= 2
            if self.level == 2 and (new_x < 0 or new_x > self.lim_x):
                new_x = new_x % (self.lim_x + 1)
            
            self.x, self.y = new_x, new_y

            self.apply_gravity()
            self.lose_energy()    
            self.shift_color()  
            self.decay()
            

        def shift_color(self):
            self.color = clr.shift(self.color, self.colorshift)

        def apply_gravity(self):
            g = 0.03*self.animspeed
            if self.motor:
                self.move_x += (self.move_x * abs(self.move_y * g * self.weight))
            else:
                self.move_y += (g * self.weight)

        def lose_energy(self):
            self.move_x *= (self.loss_factor ** self.animspeed)
            self.move_y *= (self.loss_factor ** self.animspeed)

        def decay(self):
            if self.level != 2 and math.sqrt(math.pow(self.move_x, 2) + math.pow(self.move_y, 2)) < (0.01):
                self.hp -= 5 * self.animspeed
            if self.hp > 0:
                self.hp -= 1
            else:
                self.loss_factor = 0.97
                self.color = (255, 128, 0) if self.level == 2 else clr.decay(self.color, 0.3)
                r, g, b, = self.color
                if r+g+b < 1:
                    self.is_dead = True

    def stop(self):
        self._stop_event.set()
        
    @staticmethod
    def get_instance(xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 30, animspeed = 0.5):
        new_instance = Fireworks()
        new_instance.daemon = True
        new_instance._stop_event = multiprocessing.Event()
        new_instance.params(xsize, ysize, framequeue, commandqueue, fps, animspeed)
        return new_instance
        
    def params(self, xsize, ysize, framequeue: multiprocessing.Queue, commandqueue: multiprocessing.Queue, fps = 30, animspeed = 1.0) -> None:
        self.matrix = [[(0, 0, 0) for _ in range(ysize)] for _ in range(xsize)]
        self.lim_x = xsize-1
        self.lim_y = ysize-1
        self.queue = framequeue
        self.commands = commandqueue
        self.fps = fps
        self.animspeed = animspeed
        #self.matrix = np.zeros((int(self.lim_x), int(self.lim_y), 3), dtype=np.uint8)
        self.orbs = []
        self.frametimer = Stopwatch()
        self.frametimer.set(1)
        self.quittimer = Stopwatch()
        self.quittimer.set(1)
        for _ in range(2):
            self.add_rocket()
            
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
                new[x][y] = clr.gamma(clr.wash(clr.multiply_val(self.matrix[x][y], BRIGHTNESS), PRESERVE_COLOR), GAMMA)
                #new[x][y] = color.gamma(color.wash(color.tint_rgb(self.matrix[x][y], (255, 64, 128))), 1.5)
        return self.collapse_matrix(new)
    
    def add_rocket(self):
        x = random.uniform(0, self.lim_x)
        y = self.lim_y-1
        has_motor = random.randint(0, 1) == 0
        vecx = (random.uniform(-0.1, 0.5) if x < (self.lim_x//2) else random.uniform(0.1, -0.5))
        vecy = random.uniform(-0.7, -0.8)*1.5 / (1 + has_motor)
        elem = self.Orb(x, y, vecx, vecy, self.lim_x, self.lim_y, 0, has_motor, spd = self.animspeed)
        elem.hp = int((10 + random.randint(0, 60))) 
        elem.level = 2
        elem.blend_in = int(2)+1
        elem.loss_factor = 1
        elem.weight = 1
        self.orbs.append(elem)

    def add_expl(self, x, y, vecx, vecy, color):
        elem = self.Orb(x, y, vecx, vecy, self.lim_x, self.lim_y, random.randint(0,5), spd = self.animspeed)
        smaller = (random.randint(0, 1))
        elem.level = 0
        elem.radius = 4 - smaller
        elem.hp = int(20)
        elem.color = color
        elem.loss_factor = 0.5
        elem.blend_in = int((8 - 4 * smaller))
        elem.weight = 0
        self.orbs.append(elem)
        
    def add_twinkle(self, x, y, vecx, vecy, color):
        elem = self.Orb(x, y, vecx, vecy, self.lim_x, self.lim_y, random.randint(0,5), spd = self.animspeed)
        elem.level = 3
        elem.radius = 4 + (random.randint(0, 2))
        elem.hp = int((20 + random.randint(0, 10)))
        elem.color = color
        elem.colorshift = 0
        elem.loss_factor = 0.5
        elem.blend_in = (10)
        elem.weight = 0.5
        self.orbs.append(elem)
        
    def add_tracers(self, x, y, color, speed = 1.0, weight = 1.0, n = None):
        direction = random.uniform(0.0, 1.0) 
        if not n:
            n = random.randint(3, 12)
        for i in range(n):
            speed += random.uniform(-0.3, 0.3)
            direction += (i/n)
            vecx = speed * math.cos(direction)
            vecy = speed * math.sin(direction)
            elem = self.Orb(x, y, vecx, vecy, self.lim_x, self.lim_y, 1)
            elem.level = 1
            elem.weight = weight
            elem.radius = 1
            elem.hp = int(15)
            elem.color = color
            elem.blend_in = int(random.randint(2, 7))
            #elem.loss_factor = 0.2
            self.orbs.append(elem)
    
    def render_orb(self, orb):
        # Rendere den Orb auf der Matrix
        x, y = int(orb.x), int(orb.y)
        for i in range(x - int(orb.radius/X_Scale), x + int(orb.radius/X_Scale) + 1):
            for j in range(y - orb.radius, y + orb.radius + 1):
                if 0 <= i < len(self.matrix) and 0 <= j < len(self.matrix[0]):
                    distance = math.sqrt(((i - orb.x) ** 2)*X_Scale + (j - orb.y) ** 2)
                    if distance <= orb.radius:
                        # Linearer Farbverlauf basierend auf Entfernung
                        orbcolor = clr.gamma(orb.color, 1/orb.blend_in)
                        if orb.level == 2:
                            orbcolor = clr.flicker_color(orbcolor, 5)
                        elif orb.level == 1:
                            orbcolor = clr.cycle(orbcolor, random.randint(0, 20), 8)
                        elif orb.level == 3:
                            orbcolor = clr.dither(clr.gamma(orbcolor, random.uniform(1, 20)), 120)
                            if random.randint(0, 5) == 0:
                                orbcolor = clr.gamma(orbcolor, 10)
                        gradient_factor = 1 - min(distance / orb.radius, 1.0)
                        gradient_color = clr.interpolate(orbcolor, (0,0,0), gradient_factor)
                        #self.matrix[i][j] = color.add(gradient_color, self.matrix[i][j])
                        self.matrix[i][j] = clr.brighten(gradient_color, self.matrix[i][j])
    
    def run(self):
        keep_running = True
        while keep_running and not self._stop_event.is_set():
            
            update_interval = 1/self.fps
            self.frametimer.set(update_interval)
            
            for x in range(len(self.matrix)):
                for y in range(len(self.matrix[0])):
                    self.matrix[x][y] = clr.decay(self.matrix[x][y], 0.16*self.animspeed)
                    
            for orb in self.orbs:           
                self.render_orb(orb)
                
                orb.move()
                x, y, mx, my, col, lv = orb.getData()
                if orb.is_dead:
                    self.orbs.remove(orb)
                if orb.hp < 1 and orb.level == 2:
                    self.add_rocket()
                    orb.level = -1
                    if orb.y < 20:
                        x, y, mx, my, col, _ = orb.getData()
                        if random.randint(0,2) == 1 and orb.y > 10:
                            self.add_tracers(x, y, (320,192,0), speed= 0.33, weight = 0.33)
                        else:
                            for _ in range(random.randint(1, 2)):
                                self.add_tracers(x, y, clr.gamma(col, 2))
                        if random.randint(0,1) == 1:
                            self.add_expl(x, y, mx, my, clr.multiply_val(col, random.randint(3, 8)))
                            self.add_twinkle(x, y, mx, my, clr.multiply_val(col, 4))
                        else:
                            self.add_expl(x, y, mx, my, clr.gamma(col, 3))

                    elif orb.level == 0:
                        orb.radius += 1
                    elif orb.level == 3 and len(self.orbs) < 20 and random.randint(1, 100) == 1:
                        self.add_expl(x, y, mx, my, clr.multiply_val(col, 10))
                        self.add_tracers(x, y, clr.gamma(col, 1))
            
            
            self.queue.put(self.get_matrix())

            if not self.commands.empty():
                self.commands.get_nowait()
                while not self.commands.empty():
                    self.commands.get_nowait()
                self.quittimer.set(1)
            elif self.quittimer.remaining_ms() == 0:
                print("No signal from control process. Quitting.")
                self._stop_event.set()
            
            wait = self.frametimer.remaining()
            time.sleep(wait)

        print("Terminating background process...")
        exit(0)
"""        
import main
if __name__ == "__main__":
    main.main("fireworks")
"""
 
        
    


