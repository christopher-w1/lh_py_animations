from PIL import Image, ImageDraw

class Text_PMI():
    @staticmethod
    def get_instance(xsize, ysize, fps=10):
        return Text_PMI(xsize,ysize,fps)
    
    def get_frame(self):
        next(self.text_PMI)
        return self.frame

    # Text: PMI
    def set_text_PMI_1(self):
        color_idx = 0
        frame_count = 0
        while True:
            colors = [(128,128,128), (0,0,255), (255,0,0)]
            for y in range(14):
                for x in range(28):
                    if self.bitmap[y][x] == "0":
                        self.frame[x][y] = (0,0,0)
                    if self.bitmap[y][x] == "1":
                        self.frame[x][y] = colors[color_idx]
                    if self.bitmap[y][x] == "2":
                        self.frame[x][y] = colors[(color_idx+1)%len(colors)]
                    if self.bitmap[y][x] == "3":
                        self.frame[x][y] = colors[(color_idx+2)%len(colors)]
            frame_count += 1
            if frame_count == self.fps:
                frame_count = 0
                color_idx = (color_idx + 1) % len(colors)

            yield None

    def set_text_PMI_2(self):
        while True:
            for y in range(14):
                for x in range(28):
                    if self.bitmap[y][x] != "0":
                        self.frame[x][y] = (255,255,255)
            next(self.set_colors)
            yield None

    

    
    def iterate_colors(self):
        get_colors = []
        for x in range(28):
            get_colors.append(self.change_color())
            for _ in range(x):
                for get_color in get_colors:
                    next(get_color)
        

        while True:
            for x in range(28):
                color = next(get_colors[x])
                for y in range(14):
                    if self.frame[x][y] == (255,255,255):
                        self.frame[x][y] = color
                    
            yield None

    def change_color(self, jump=0):
        
        while True:
            # red to grey
            color = [255,0,0]
            while color[0] > 128 and jump <= 0:
                color[0] -= 1
                color[1] += 1
                color[2] += 1
                yield color
            # color = [127, 128, 128]
            jump -= 1

            for _ in range(10):
                yield color
            # grey to blue
            color = [128, 128, 127]
            while color[0] > 0 and jump <= 0:
                color[0] -= 1
                color[2] += 1
                yield color
            # color = [0, 128, 255]
            jump -= 1

            # blue to grey
            color = [0,128,255]
            while color[2] > 128 and jump <= 0:
                color[0] += 1
                color[2] -= 1
                yield color
            # color = [128, 128, 127]
            

            jump -= 1
            # grey to red
            color = [127, 128, 128]
            while color[1] > 0 and jump <= 0:
                color[0] += 1
                color[1] -= 1
                color[2] -= 1
                yield color
            
            # color = [255, 0, 0]

            jump = 0


    def __init__(self,xsize=28, ysize=14, fps=10):
        self.name = "Text - PMI"
        self.xsize = xsize
        self.ysize = ysize
        self.fps = fps
        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        #self.text_PMI = self.set_text_PMI_1()
        self.text_PMI = self.set_text_PMI_2()
        self.set_colors = self.iterate_colors()
        self.bitmap = ["0000000000000000000000000000",
                       "0000000000000000000000000000",
                       "1111111000002200000000220033",
                       "1100000110002220000002220033",
                       "1100000011002222000022220033",
                       "1100000011002202200220220033",
                       "1100000110002200222200220033",
                       "1111111000002200022000220033",
                       "1100000000002200000000220033",
                       "1100000000002200000000220033",
                       "1100000000002200000000220033",
                       "1100000000002200000000220033",
                       "0000000000000000000000000000",
                       "0000000000000000000000000000"]