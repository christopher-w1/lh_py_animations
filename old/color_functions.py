import random, math

def rand_vibrant_color(intensity: float):
    high = 255*intensity
    mid = random.randint(0, 255)*intensity
    low = 0
    lst = [low, mid, high]
    random.shuffle(lst)
    return tuple(lst)

def rand_rgb_color(intensity: float):
    high = 255*intensity
    mid = 0
    low = 0
    lst = [low, mid, high]
    random.shuffle(lst)
    return tuple(lst)

def clip(color: (int, int, int)) -> (int, int, int):
    r, g, b = color
    return (max(0, min(r, 255)), max(0, min(g, 255)), max(0, min(b, 255)))

def wash(color: (int, int, int)) -> (int, int, int):
    r, g, b = color
    
    max_val = max(r, g, b)

    if max_val > 255:
        diff = max_val - 255
        diff_half = diff // 2

        r = min(255, r + diff_half)
        g = min(255, g + diff_half)
        b = min(255, b + diff_half)
            
    return (r, g, b)

def interpolate(color2, color1, factor):
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    return (r, g, b)

def gamma(color: (int, int, int), gamma: float) -> (int, int, int):
    r, g, b = color

    r /= 255.0
    g /= 255.0
    b /= 255.0

    r = int((r ** gamma) * 255 + 0.5)
    g = int((g ** gamma) * 255 + 0.5)
    b = int((b ** gamma) * 255 + 0.5)

    return (r, g, b)

def decay(color: (int, int, int), decay_factor: float) -> (int, int, int):
    r, g, b = color

    if max(r, g, b) < 5: 
        return color

    decay_factor += random.uniform(-0.05, 0.05)

    # Decay-Faktor sollte im Bereich [0, 1] liegen
    decay_factor = max(0.0, min(1.0, decay_factor))

    # Abdunkeln der Farbwerte
    r = int(r * (1 - decay_factor))
    g = int(g * (1 - decay_factor))
    b = int(b * (1 - decay_factor))

    return (r, g, b)


def brighten(color1: (int, int, int), color2: (int, int, int)) -> (int, int, int):
    r = max(color1[0], color2[0])
    g = max(color1[1], color2[1])
    b = max(color1[2], color2[2])
    return (r, g, b)


def shift(color: (int, int, int), shift_amount: int) -> (int, int, int):
    r, g, b = color

    # RGB zu HSV konvertieren
    h, s, v = rgb_to_hsv(r, g, b)

    # Hue verschieben (im Bereich [0, 360])
    h = (h + shift_amount) % 360

    # HSV zu RGB konvertieren
    r, g, b = hsv_to_rgb(h, s, v)

    return (r, g, b)

# Hilfsfunktionen für die Umwandlung zwischen RGB und HSV
def rgb_to_hsv(r, g, b):
    max_color = max(r, g, b)
    min_color = min(r, g, b)

    v = max_color / 255.0
    if max_color == 0:
        s = 0
    else:
        s = (max_color - min_color) / max_color

    if max_color == min_color:
        h = 0  # undefined, but commonly set to 0
    elif max_color == r:
        h = (60 * ((g - b) / (max_color - min_color)) + 360) % 360
    elif max_color == g:
        h = (60 * ((b - r) / (max_color - min_color)) + 120) % 360
    elif max_color == b:
        h = (60 * ((r - g) / (max_color - min_color)) + 240) % 360

    return int(h), int(s * 100), int(v * 100)

def hsv_to_rgb(h, s, v):
    h /= 360.0
    s /= 100.0
    v /= 100.0

    if s == 0:
        r = g = b = int(v * 255)
    else:
        h *= 6
        i = math.floor(h)
        f = h - i
        p = int(255 * v * (1 - s))
        q = int(255 * v * (1 - s * f))
        t = int(255 * v * (1 - s * (1 - f)))

        if i % 6 == 0:
            r, g, b = int(255 * v), t, p
        elif i % 6 == 1:
            r, g, b = q, int(255 * v), p
        elif i % 6 == 2:
            r, g, b = p, int(255 * v), t
        elif i % 6 == 3:
            r, g, b = p, q, int(255 * v)
        elif i % 6 == 4:
            r, g, b = t, p, int(255 * v)
        elif i % 6 == 5:
            r, g, b = int(255 * v), p, q

    return r, g, b

def dither(color: (int, int, int), dither_amount: int) -> (int, int, int):
    r, g, b = color

    # Zufälligen Dither-Wert für jeden Farbkanal generieren
    dither_r = random.randint(-dither_amount, dither_amount)
    dither_g = random.randint(-dither_amount, dither_amount)
    dither_b = random.randint(-dither_amount, dither_amount)

    # Dither auf die Farbwerte anwenden
    r = max(0, min(255, r + dither_r))
    g = max(0, min(255, g + dither_g))
    b = max(0, min(255, b + dither_b))

    return (r, g, b)