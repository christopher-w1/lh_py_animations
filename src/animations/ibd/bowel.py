from PIL import Image, ImageDraw
from color_functions import interpolate
import pathlib,os,random



class Inflammation:
    def __init__(self, x, y, radius, color=(212, 56, 64)):
        self.x = x 
        self.y = y  
        self.radius = radius
        self.color = color
        self.full_life = 100 + random.randint(0, 100)
        self.life = self.full_life - 1

    def render(self, frame, background):
        for i in range(-self.radius, self.radius + 1):
            for j in range(-self.radius, self.radius + 1):
                if i**2 + j**2 <= self.radius**2:
                    xi = self.x + i
                    yj = self.y + j
                    if 0 <= xi < len(frame) and 0 <= yj < len(frame[0]):
                        background_color = frame[xi][yj]
                        new_color = (
                            background[xi][yj][0] * self.color[0] // 255,
                            background[xi][yj][1] * self.color[1] // 255,
                            background[xi][yj][2] * self.color[2] // 255
                        )
                        
                        distance = (i**2 + j**2)**0.5
                        factor = (1 - (2 * abs((self.full_life / 2) - self.life) / self.full_life))**0.5 / (1 + distance / self.radius)
                        
                        frame[xi][yj] = interpolate(new_color, background_color, factor)
        self.life -= 1
        return self.life > 0

class Bowel():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        return Bowel(xsize,ysize,fps)
    
    def __init__(self,xsize=28, ysize=14, fps=30):
        self.name = "IBD - Bowel"
        self.xsize = xsize
        self.ysize = ysize
        self.framecounter = 0.0
        self.fps = fps

        self.frame : list[list[tuple[int, int, int]]] = []
        self.background : list[list[tuple[int, int, int]]]  = []
        self.inflammations : list[Inflammation] = []
        
        for x in range(xsize):
            self.frame.append([])
            self.background.append([])
            for y in range(ysize):
                self.frame[x].append((0,0,0))
                self.background[x].append((0,0,0))

        img = Image.open(os.path.join(pathlib.Path(__file__).parent,'bowel.png'))
        for y in range(0, 28, 2):
            for x in range(28):
                r, g, b = 0, 0, 0
                try:
                    pixel = img.getpixel((x,y))
                    r,g,b,_ = pixel if isinstance(pixel, tuple) and len(pixel) == 4 else (0,0,0,0) 
                except IndexError:
                    print(f"Error: {x} {y} {self.xsize} {self.ysize}")
                self.frame[x][y//2] = (r,g,b)
                self.background[x][y//2] = (r,g,b)

    def next_frame(self):
        for y in range(self.ysize):
            for x in range(self.xsize):
                self.frame[x][y] = self.background[x][y]

        # Neue Entzündung zufällig hinzufügen (z. B. 1% Chance pro Frame)
        if random.random() < 0.05:
            print("Adding new inflammation")
            x = random.randint(4, self.xsize - 5)
            y = random.randint(4, self.ysize - 5)
            radius = random.randint(3, 5)
            self.inflammations.append(Inflammation(x, y, radius))

        # Aktive Entzündungen rendern und filtern
        self.inflammations = [
            inf for inf in self.inflammations if inf.render(self.frame, self.background)
        ]

    def get_frame(self):
        self.framecounter += 1
        timestep = self.framecounter / self.fps
        
        if timestep > 1:
            timestep = 0
            self.next_frame()
            
        return self.frame

