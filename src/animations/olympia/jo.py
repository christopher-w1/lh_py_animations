class Jo():
    @staticmethod
    def get_instance(xsize, ysize, fps=30):
        return Jo(xsize,ysize,fps)
    
    def get_frame(self):
        color = next(self.color_gen)
        for x in range(28):
            for y in range(14):
                
                if self.bitmap[y][x] == "1":
                    self.frame[x][y] = color
                
                elif self.bitmap[y][x] == "2":
                    self.frame[x][y] = (255,255,255)
                
                else:
                    self.frame[x][y] = (0,0,0)
        
        return self.frame
    
    def generator_cycle_colors(self, colors: list[tuple[int, int, int]], cycle_steps=25, wait_steps=50):
        """
        Cycle through a list of colors.

        Shows in each yield the current color or a step between two colors.
        For the colors used, the given list will be iterated through.
        """
        # Amount of steps to cycle from one color to the next
        cycle_steps = cycle_steps
        # Amount of steps the saem color should be shown
        wait_steps = wait_steps
    
        while True:
            for i in range(len(colors)-1):
                start_color = colors[i]
                end_color = colors[i+1]

                r_step = (end_color[0] - start_color[0]) / (cycle_steps + 1)
                r_raw = colors[i][0]
                g_step = (end_color[1] - start_color[1]) / (cycle_steps + 1)
                g_raw = colors[i][1]
                b_step = (end_color[2] - start_color[2]) / (cycle_steps + 1)
                b_raw = colors[i][2]

                for _ in range(wait_steps):
                    yield (int(r_raw), int(g_raw), int(b_raw))

                for _ in range(cycle_steps):
                    r_raw += r_step
                    g_raw += g_step
                    b_raw += b_step
                    yield (int(r_raw), int(g_raw), int(b_raw))

            r_step = (colors[0][0] - colors[-1][0]) / cycle_steps
            r_raw = colors[-1][0]
            g_step = (colors[0][1] - colors[-1][1]) / cycle_steps
            g_raw = colors[-1][1]
            b_step = (colors[0][2] - colors[-1][2]) / cycle_steps
            b_raw = colors[-1][2]

            for _ in range(wait_steps):
                yield (int(r_raw), int(g_raw), int(b_raw))

            for _ in range(cycle_steps):
                r_raw += r_step
                g_raw += g_step
                b_raw += b_step
                yield (int(r_raw), int(g_raw), int(b_raw))
    
    def __init__(self,xsize=28, ysize=14, fps=10):
        self.name = "Jo! - Logo"
        self.xsize = xsize
        self.ysize = ysize
        
        blue = (0,165,226)
        red = (228, 1, 66)
        yellow = (253, 191, 9)
        green = (28, 156, 73)
        colors = [blue, red, yellow, green]
        self.color_gen = self.generator_cycle_colors(colors, 50, 300)


        self.frame = []
        for x in range(xsize):
            self.frame.append([])
            for y in range(ysize):
                self.frame[x].append([0,0,0])

        self.bitmap = ["0000000000000000000000000000",
                       "0111111111111111111111111110",
                       "1111122211111222221111122211",
                       "1111122211122222222211122211",
                       "1111122211222222222221122211",
                       "1111122211222222222221122211",
                       "1111122211222222222221111111",
                       "1122222211122222222211122211",
                       "1122222111111222221111122211",
                       "0111111111111111111111111110",
                       "0000001111111110000000000000",
                       "0000011111110000000000000000",
                       "0000011100000000000000000000",
                       "0000000000000000000000000000"]