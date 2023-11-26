import tkinter as tk
import color_functions as color
import math, random

class BounceAnimation:
    class Orb:
        def __init__(self, x, y, vecx, vecy, limx, limy, colorshift = 0) -> None:
            self.lim_x = limx
            self.lim_y = limy
            self.move_x = vecx
            self.move_y = vecy
            self.radius = 2
            self.x = x
            self.y = y
            #self.color = color.rand_vibrant_color(3)
            self.color = color.shift(color.rand_rgb_color(3), random.randint(0, 360))
            self.colorshift = colorshift
            self.loss_factor = random.uniform(0.99, 0.999)
            self.is_dead = False
            self.exists = 10
            self.hp = random.randint(100, 1000)

        def move(self) -> None:
            if self.exists > 1:
                self.exists -= 1

            new_x = self.x + self.move_x
            new_y = self.y + self.move_y

            # Bounce
            if new_x >= self.lim_x:
                self.move_x = 0 - self.move_x
                self.x = self.lim_x
                #self.shift_color()
            elif new_x <= 0: 
                self.move_x = 0 - self.move_x
                self.x = 0
                #self.shift_color()
            else:
                self.x = new_x

            if new_y >= self.lim_y:
                self.move_y = 0 - self.move_y
                self.y = self.lim_y
                
            elif new_y <= 0:
                self.move_y = 0 - self.move_y
                self.y = 0
                #self.shift_color()
            else: 
                self.y = new_y      

            self.apply_gravity()
            self.lose_energy()    
            self.shift_color()  
            self.decay()
            

        def shift_color(self):
            self.color = color.shift(self.color, self.colorshift)

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
                self.color = color.decay(self.color, 0.03)
                r, g, b, = self.color
                if r+g+b < 1:
                    self.is_dead = True

        def energize(self):
            energy = math.sqrt(math.pow(self.move_x, 2) + math.pow(self.move_y, 2))
            if energy < 1:
                self.loss_factor = 1.01
            elif energy > 3:
                self.loss_factor = 0.99

    def __init__(self, limx, limy) -> None:
        self.matrix = [[(0, 0, 0) for _ in range(limy)] for _ in range(limx)]
        self.lim_x = limx
        self.lim_y = limy
        self.spawnmore = True
        #self.matrix = np.zeros((int(self.lim_x), int(self.lim_y), 3), dtype=np.uint8)
        self.orbs = []
        for _ in range(5):
            self.add_rand_orb()

    def get_matrix(self):
        new = [row[:] for row in self.matrix]
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                #self.matrix[x][y] = color.dither(self.matrix[x][y], 10)
                new[x][y] = color.wash(self.matrix[x][y])
        return new

    
    def add_rand_orb(self):
        x = random.uniform(0, self.lim_x)
        y = 1 #random.uniform(0, self.lim_y)
        vecx = random.uniform(0.1, 1)
        vecy = random.uniform(0.1, 1)
        colorshift = random.uniform(0.0, 1.0)*2
        self.orbs.append(self.Orb(x, y, vecx, vecy, self.lim_x, self.lim_y, colorshift))
    
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
                        orbcolor = color.gamma(orb.color, 1/orb.exists)
                        gradient_factor = 1 - min(distance / orb.radius, 1.0)
                        gradient_color = color.interpolate(orbcolor, (0,0,0), gradient_factor)

                        self.matrix[i][j] = color.brighten(gradient_color, self.matrix[i][j])
    
    def do_iterate(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[0])):
                self.matrix[x][y] = color.shift(color.decay(self.matrix[x][y], 0.15), 0)
                
        for orb in self.orbs:
            self.render_orb(orb)
            orb.move()
            if orb.is_dead:
                self.orbs.remove(orb)
                if self.spawnmore:
                    self.add_rand_orb()
                    self.add_rand_orb()
                    
        if len(self.orbs) > 25:
            self.spawnmore = False
        elif len(self.orbs) < 5:
            self.spawnmore = True
            #orb.shift_color()
        
        
    





class ScalableCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.original_width = 28
        self.original_height = 28
        self.scale_factor = 10
        self.scale_canvas(self.scale_factor)

    def scale_canvas(self, factor):
        self.scale_factor = factor
        self.config(width=self.original_width * factor, height=self.original_height * factor* 1.5)
        self.master.geometry(f"{int((self.original_width) * factor + 20)}x{int((self.original_height) * factor *1.5 + 20)}")

def collapse_matrix(matrix):
    collapsed_matrix = []

    for x in range(len(matrix)):
        collapsed_row = []
        for y in range(0, len(matrix[0]), 2):
            pixel1 = matrix[x][y]
            pixel2 = matrix[x][min(y + 1, len(matrix[x])-1)]

            # Median der beiden Pixel berechnen
            collapsed_pixel = (
                (pixel1[0] + pixel2[0]) // 2,
                (pixel1[1] + pixel2[1]) // 2,
                (pixel1[2] + pixel2[2]) // 2
            )

            collapsed_row.append(collapsed_pixel)

        collapsed_matrix.append(collapsed_row)

    return collapsed_matrix

def stretch_matrix(matrix):
    stretched_matrix = []

    for row in matrix:
        stretched_row = []
        for pixel in row:
            stretched_row.append(pixel)
            stretched_row.append(pixel)  # Füge den Pixel noch einmal hinzu, um ihn zu strecken
        stretched_matrix.append(stretched_row)

    return stretched_matrix


def update_canvas(canvas, matrix):
    canvas.delete("all") 
    matrix = stretch_matrix(collapse_matrix(matrix))
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if j % 2 == 0: continue
            color = matrix[i][j]
            if max(color) < 1: continue
            x = i+1
            y = j+1
            canvas.create_rectangle(x * canvas.scale_factor, y * canvas.scale_factor * 1.33,
                                    (x + 1) * canvas.scale_factor, (y + 1) * canvas.scale_factor * 1.33,
                                    fill="#%02x%02x%02x" % color, outline="#202020")
            
def animate(animation: BounceAnimation, canvas, rt):
    animation.do_iterate()
    matrix = animation.get_matrix()
    update_canvas(canvas, matrix)
    rt.after(17, animate, animation, canvas, rt)

def main():
    root = tk.Tk()
    root.title("Scalable Canvas")

    canvas = ScalableCanvas(root, width=28, height=28, bg="black")
    canvas.pack(expand=tk.YES, fill=tk.BOTH)

    anim = BounceAnimation(27, 26)
    matrix = anim.get_matrix()

    update_canvas(canvas, matrix)

    animation_interval = 100  # Intervall in Millisekunden
    root.after(animation_interval, animate, anim, canvas, root)  # Erste Animation starten

    root.mainloop()

if __name__ == "__main__":
    main()


