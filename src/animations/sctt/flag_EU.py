class EU_Flag():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        instance = EU_Flag(xsize, ysize, fps)
        return instance
        

    def get_frame(self):
        self.set_frame()
        return self.frame


    def set_frame(self):
        for y in range(14):
            for x in range(28):
                if self.bitmap1[y][x] == "1":
                    self.frame[x][y] = self.blue
                elif self.bitmap1[y][x] == "2":
                    self.frame[x][y] = self.yellow
                elif self.bitmap1[y][x] == "3":
                    self.frame[x][y] = self.dark_blue
                elif self.bitmap1[y][x] == "4":
                    self.frame[x][y] = self.light_blue
                else:
                    self.frame[x][y] = (0,0,0)
        self.star_animation()

    def star_animation(self):
        if self.wait <= 0:
            self.wait = 60
            self.stage = not self.stage

        if self.stage:
            self.frame[9] [3]  = self.dark_yellow
            self.frame[17][3]  = self.dark_yellow
            self.frame[5] [6]  = self.dark_yellow
            self.frame[21][6]  = self.dark_yellow
            self.frame[9] [9] = self.dark_yellow
            self.frame[17][9] = self.dark_yellow
        else:
            self.frame[13][3]  = self.dark_yellow
            self.frame[6] [4]  = self.dark_yellow
            self.frame[20][4]  = self.dark_yellow
            self.frame[6] [8]  = self.dark_yellow
            self.frame[20][8]  = self.dark_yellow
            self.frame[13][9] = self.dark_yellow

        self.wait -= 1



    def __init__(self, xsize=28, ysize=14, fps=30):
        self.name = "EU - Flag"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        
        self.frame=[]
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.stage = True
        self.wait = 60

        self.blue = (0, 51, 153)
        self.dark_blue = (0, 26, 77)
        self.light_blue = (0, 77, 230)
        self.yellow = (255, 204, 0)
        self.dark_yellow = (230,184,0)

        self.bitmap1 = ["0000000000000000000000000000",
                        "3444444444444444444444444440",
                        "3311111111111111111111111444",
                        "3111111112111211121111111144",
                        "3111112111111111111121111144",
                        "3111111111111111111111111144",
                        "3111121111111111111112111144",
                        "3111111111111111111111111144",
                        "3111112111111111111121111144",
                        "3111111112111211121111111144",
                        "3311111111111111111111111144",
                        "0333333333333333333333333334",
                        "0000000000000000000000000000",
                        "0000000000000000000000000000"]

        self.bitmap2 = ["0000000000000000000000000000",
                        "1111111111111111111111111111",
                        "1111111111111111111111111111",
                        "1111111112111211121111111111",
                        "1111112111111111111121111111",
                        "1111111111111111111111111111",
                        "1111121111111111111112111111",
                        "1111111111111111111111111111",
                        "1111112111111111111121111111",
                        "1111111112111211121111111111",
                        "1111111111111111111111111111",
                        "1111111111111111111111111111",
                        "0000000000000000000000000000",
                        "0000000000000000000000000000"]
        