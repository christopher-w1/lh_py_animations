from random import random

class Sailing():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        return Sailing(xsize,ysize,fps)
    

    def get_frame(self):
        if self.wait <= 0:
            next(self.animation)
            self.wait = 30
        self.wait -= 1
        return self.frame


    def draw(self):
        while True:
            for y in range(14):
                for x in range(28):
                    if self.bitmaps[0][y][x] == "0":
                        self.frame[x][y] = self.color_bg
                    elif self.bitmaps[0][y][x] == "1":
                        self.frame[x][y] = self.color_water
                    elif self.bitmaps[0][y][x] == "2":
                        self.frame[x][y] = self.color_white
                    elif self.bitmaps[0][y][x] == "3":
                        self.frame[x][y] = self.color_red
                    elif self.bitmaps[0][y][x] == "4":
                        self.frame[x][y] = self.color_light
                    elif self.bitmaps[0][y][x] == "5":
                        self.frame[x][y] = self.color_ground

            self.draw_sails()
            yield None


    def draw_sails(self):
        self.move_sails()
        for it_y in range(7):
            for it_x in range(8):
                x_offset, y_offset = self.sail1_pos
                x = int(it_x + x_offset)
                y = int(it_y + y_offset)
                if self.bitmaps[1][it_y][it_x] == "1":
                    self.frame[x][y] = self.color_sail
                elif self.bitmaps[1][it_y][it_x] == "2":
                    self.frame[x][y] = self.color_pole
                elif self.bitmaps[1][it_y][it_x] == "3":
                    self.frame[x][y] = self.color_hull
                
                x_offset, y_offset = self.sail2_pos
                x = int(it_x + x_offset)
                y = int(it_y + y_offset)
                if self.bitmaps[2][it_y][it_x] == "1":
                    self.frame[x][y] = self.color_sail
                elif self.bitmaps[2][it_y][it_x] == "2":
                    self.frame[x][y] = self.color_pole
                elif self.bitmaps[2][it_y][it_x] == "3":
                    self.frame[x][y] = self.color_hull

    def move_sails(self):
        move = (random() - 0.5) * 2
        x,y = self.sail1_pos
        x += move
        x = x if x >= 1 else 1
        x = x if x < 4 else 3
        self.sail1_pos = (x, y)

        move = (random() - 0.5) * 2
        x,y = self.sail2_pos
        x += move
        x = x if x >= 12 else 12
        x = x if x < 15 else 14
        self.sail2_pos = (x, y)

    def __init__(self,xsize=28, ysize=14, fps=30):
        self.name = "Sailing"
        self.xsize = xsize
        self.ysize = ysize

        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.animation = self.draw()
        self.wait = 0

        self.sail1_pos = (1,3)
        self.sail2_pos = (12,5)

        self.color_bg = (0,0,0)
        self.color_water = (50, 60, 255)
        self.color_white = (255,255,255)
        self.color_red = (255,10,5)
        self.color_light = (255,255,100)
        self.color_ground = (180,180,200)
        
        self.color_sail = self.color_white
        self.color_pole = (120, 67, 21)
        self.color_hull = (150,160,170)

        self.bitmaps = [# Background bitmap: 0 Background | 1 Water | 2 White | 3 Red | 4 Lightsource | 5 Ground
                        ["4440004000000000000000000000",
                         "4440000000000000000000000000",
                         "4400040000000000000000000000",
                         "0000400000000000000000000000",
                         "4000000000000000000000003000",
                         "0000000000000000000000020200",
                         "0000000000000000000000033300",
                         "1111111111111111111111122211",
                         "1111111111111111111111533351",
                         "1111111111111111111111155511",
                         "1111111111111111111111111111",
                         "1111111111111111111111111111",
                         "1111111111111111111111111111",
                         "1111111111111111111111111111"],
                         
                        # Sail 1 Bitmap: 0 Background | 1 Sail | 2 Pole | 3 Hull
                        ["02100000",
                         "02110000",
                         "02111000",
                         "02111100",
                         "02111100",
                         "33333333",
                         "03333330"],
                        
                        
                        # Sail 2 Bitmap: 
                        ["02100000",
                         "02111000",
                         "02111100",
                         "02111110",
                         "02111110",
                         "33333333",
                         "03333330"]
                        ]