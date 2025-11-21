from math import sin, pi, sqrt

def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))

def smoothstep(x):
    # 0..1 smoothstep
    x = clamp(x, 0.0, 1.0)
    return x*x*(3 - 2*x)

class Pulseheart:
    @staticmethod
    def get_instance(out_x=28, out_y=14, fps=12, aa_samples=4, internal_size=28):
        inst = Pulseheart(out_x, out_y, fps, aa_samples, internal_size)
        inst.params()
        return inst

    def params(self):
        self.name = "Pulseheart"
        # Pulsing: fractional amplitude and frequency (Hz)
        self.pulse_strength = 0.14
        self.pulse_freq = 1.0

        # Farben (RGB)
        self.start_color = [100,150,255]
        self.end_color   = [205,50,150]

        # Mapping internal 28x28 -> equation coordinate space
        # Typical heart eq uses x,y around [-1.6,1.6]; du kannst diese Werte feinjustieren
        self.xmin, self.xmax = -1.6, 1.6
        self.ymin, self.ymax = -2.0, 4.5

        # edge softness in pixels (in internal grid units) - steuert weiche Kante
        self.edge_softness = 0.9

        # AA / internal size already set by constructor

    def __init__(self, out_x=28, out_y=14, fps=12, aa_samples=4, internal_size=28):
        self.out_x = out_x
        self.out_y = out_y
        self.internal_w = self.internal_h = internal_size
        self.fps = fps
        self.aa_samples = aa_samples if aa_samples >= 1 else 1
        self.frame_number = 0.0

        self.frame = [
            [[0,0,0] for _ in range(out_y)]
            for _ in range(out_x)
        ]
        self.internal = [
            [[0,0,0] for _ in range(self.internal_h)]
            for _ in range(self.internal_w)
        ]

    # ----- heart implicit function: F(x,y) = (x^2 + y^2 - 1)^3 - x^2 y^3
    def F(self, x, y):
        A = x*x + y*y - 1.0
        return A*A*A - (x*x)*(y*y*y)

    # analytical derivatives (partials)
    def Fx(self, x, y):
        A = x*x + y*y - 1.0
        return 6.0 * x * (A*A) - 2.0 * x * (y**3)

    def Fy(self, x, y):
        A = x*x + y*y - 1.0
        return 6.0 * y * (A*A) - 3.0 * (x**2) * (y**2)

    # approximate signed distance from implicit function: d ≈ F / |∇F|
    def signed_distance(self, x, y):
        f = self.F(x, y)
        fx = self.Fx(x, y)
        fy = self.Fy(x, y)
        grad = sqrt(fx*fx + fy*fy)
        if grad == 0.0:
            return f  # fallback
        return f / grad

    def get_frame(self):
        # time in seconds
        t = self.frame_number / max(1.0, self.fps)
        scale = 1.0 + self.pulse_strength * sin(2*pi*self.pulse_freq*t)

        iw = self.internal_w
        ih = self.internal_h

        # precompute sample offsets for AA
        samples = []
        if self.aa_samples <= 1:
            samples = [(0.5, 0.5)]
        else:
            n = int(self.aa_samples**0.5)
            if n < 1: n = 1
            step = 1.0 / n
            for iy in range(n):
                for ix in range(n):
                    samples.append(((ix + 0.5) * step, (iy + 0.5) * step))

        # Map internal pixel coords to equation space
        for px in range(iw):
            for py in range(ih):
                cov_acc = 0.0
                for (sx, sy) in samples:
                    sx_abs = px + sx
                    sy_abs = py + sy

                    # normalized [0..1]
                    nx = sx_abs / (iw - 1)
                    ny = sy_abs / (ih - 1)

                    # map to equation space
                    ex = self.xmin + nx * (self.xmax - self.xmin)
                    ey = self.ymin + ny * (self.ymax - self.ymin)

                    # translate to origin, then scale (pulse) around origin
                    y_offset = -0.15  # move shape slightly down (tuneable)
                    ey = -ey + y_offset

                    exs = ex / scale
                    eys = ey / scale

                    # signed distance (in equation-space units). Convert to approx pixel units by scaling
                    # relative pixel per unit: px_per_unit = iw / (xmax - xmin)
                    px_per_unit = iw / (self.xmax - self.xmin)
                    d = self.signed_distance(exs, eys) * px_per_unit

                    # convert to coverage via smoothstep around edge_softness
                    # inside (d<=0) -> cov ~1; outside -> falls to 0 over edge_softness
                    edge = max(1e-6, self.edge_softness)
                    if d <= -edge:
                        cov = 1.0
                    elif d >= edge:
                        cov = 0.0
                    else:
                        # map d from [-edge, edge] -> [1,0]
                        cov = smoothstep(1.0 - ((d + edge) / (2*edge)))
                    cov_acc += cov

                avg_cov = cov_acc / len(samples)

                if avg_cov > 0.0:
                    gradient = (sin(((self.frame_number / 30.0) + (px / max(1.0, iw))) * pi) + 1) / 2
                    base_color = [
                        int(self.start_color[i] + gradient * (self.end_color[i] - self.start_color[i]))
                        for i in range(3)
                    ]
                    self.internal[px][py] = [int(base_color[i] * avg_cov) for i in range(3)]
                else:
                    self.internal[px][py] = [0,0,0]

        # light internal smoothing (3x3 average)
        self._smooth_internal()

        # downsample internal -> output via averaging blocks (28x28 -> 28x14)
        self._downsample_to_output()

        self.frame_number += 1.0
        return self.frame

    def _smooth_internal(self):
        iw, ih = self.internal_w, self.internal_h
        buf = []
        for y in range(ih):
            buf.append([])
            for x in range(iw):
                cols = []
                for oy in (-1,0,1):
                    for ox in (-1,0,1):
                        nx, ny = x+ox, y+oy
                        if 0 <= nx < iw and 0 <= ny < ih:
                            cols.append(self.internal[nx][ny])
                n = max(1, len(cols))
                r = sum(c[0] for c in cols)//n
                g = sum(c[1] for c in cols)//n
                b = sum(c[2] for c in cols)//n
                buf[y].append([r,g,b])
        for y in range(ih):
            for x in range(iw):
                self.internal[x][y] = buf[y][x]

    def _downsample_to_output(self):
        iw, ih = self.internal_w, self.internal_h
        ox, oy = self.out_x, self.out_y
        for out_x in range(ox):
            sx0f = out_x * (iw / ox)
            sx1f = (out_x + 1) * (iw / ox)
            sx0 = int(sx0f); sx1 = min(iw, int(sx1f))
            if sx1 <= sx0: sx1 = min(iw, sx0+1)
            for out_y in range(oy):
                sy0f = out_y * (ih / oy)
                sy1f = (out_y + 1) * (ih / oy)
                sy0 = int(sy0f); sy1 = min(ih, int(sy1f))
                if sy1 <= sy0: sy1 = min(ih, sy0+1)
                rsum = gsum = bsum = count = 0
                for sx in range(sx0, sx1):
                    for sy in range(sy0, sy1):
                        c = self.internal[sx][sy]
                        rsum += c[0]; gsum += c[1]; bsum += c[2]; count += 1
                if count == 0:
                    self.frame[out_x][out_y] = [0,0,0]
                else:
                    self.frame[out_x][out_y] = [rsum//count, gsum//count, bsum//count]
