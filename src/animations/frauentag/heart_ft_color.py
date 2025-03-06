from math import sqrt
from math import sin, pi


class Heart_ft():
    @staticmethod
    def get_instance(xsize, ysize, fps=2):
        instance = Heart_ft(xsize, ysize, fps)
        instance.params()
        return instance
    

    def params(self):
        self.xsize = 28
        self.ysize = 14
        self.fps = 2
        self.name = "Heart - Frauentag"
        

    def get_frame(self):
        self.set_frame(self.bitmaps[0])
        self.frame_number += 0.5
        return self.frame


    def set_frame(self, bitmap):
        center_x, center_y = 13, 6
        max_distance = sqrt(center_x**2 + center_y**2)

        # Wähle die Farben für den Farbverlauf
        start_color = [100, 150, 255]  # Startfarbe (blau)
        end_color = [205, 50, 150]    # Endfarbe (rot)


        for x in range(0, 28):
            for y in range(0, 14):
                if bitmap[y][x] == "1":
                    #distance = sqrt((x - center_x)**2 + (y - center_y)**2)
                    #color_value = int((distance / max_distance) * 255)

                    # Farbverlaufsberechnung basierend auf der horizontalen Position
                    gradient = (sin(((self.frame_number / 30) + (x / 28)) * pi) + 1) / 2
                    interpolated_color = [
                        int(start_color[i] + gradient * (end_color[i] - start_color[i]))
                        for i in range(3)
                    ]

                    self.frame[x][y] = interpolated_color
                else:
                    self.frame[x][y] = [0, 0, 0]

    
    def __init__(self, xsize=28, ysize=14, fps=2):
        self.name = "Heart - Frauentag"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        self.frame_number = 0
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmaps = [["0000000000000000000000000000",
                         "0000000000000000000000000000",
                         "0000001111110001111110000000",
                         "0000111111111011111111100000",
                         "0001111111111111111111110000",
                         "0001111111111111111111110000",
                         "0000111111111111111111100000",
                         "0000011111111111111111000000",
                         "0000000111111111111100000000",
                         "0000000001111111110000000000",
                         "0000000000011111000000000000",
                         "0000000000000100000000000000",
                         "0000000000000000000000000000",
                         "0000000000000000000000000000"]]