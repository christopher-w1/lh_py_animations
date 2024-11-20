import random, math, time

def rand_vibrant_color(intensity: float):
    high = 255*intensity
    mid = random.randint(0, 255)*intensity
    low = 0
    lst = [low, mid, high]
    random.shuffle(lst)
    return tuple(lst)

def rand_vibrant_color2(intensity: float):
    return shift(rand_rgb_color(intensity), random.randint(0,359))

def from_float(pixel: tuple[float, float, float]):
    r, g, b = pixel
    r_int, g_int, b_int = int(r), int(g), int(b)
    rfl, gfl, bfl = r - r_int, g - g_int, b - b_int
    threshold = random.random()
    if rfl > threshold: r_int += 1
    if gfl > threshold: g_int += 1
    if bfl > threshold: b_int += 1
    
    return (r_int, g_int, b_int)

def rand_blue_color(intensity: float):
    r = 0 
    g = 0
    b = random.randint(int(200 * intensity), int(255 * intensity))  
    
    variance = random.randint(-35, 5)
    
    return shift((r, g, b), variance)

def rand_metal_color(intensity: float):
    
    metals = {
        'strontium': (255, 0, 0),
        'calcium': (255, 111, 0),
        'barium': (70, 255, 50),
        'rubidium': (102, 0, 255),
        'copper': (0, 110, 255),
        'sodium': (255, 0, 196),
    }
    
    r, g, b = random.choice(list(metals.values()))
    
    return (r * intensity, g * intensity, b * intensity)

def rand_faculty_color(intensity: float):
    faculties = {
        'theology': (86,35,129),
        'law': (228,49,23),
        'medicine': (153,194,33),
        'philosophy': (106,172,218),
        'agriculture/nutritional': (57,132,46),
        'mathematics/science': (242,148,0),
        'economics/social': (0,103,124),
        'technical': (0,61,134),
    }
    r, g, b = random.choice(list(faculties.values()))
    return (r * intensity, g * intensity, b * intensity)

def rand_rgb_color(intensity: float):
    high = 255*intensity
    mid = 0
    low = 0
    lst = [low, mid, high]
    random.shuffle(lst)
    return tuple(lst)

def clip(color: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = color
    return (max(0, min(r, 255)), max(0, min(g, 255)), max(0, min(b, 255)))

def normalize(color: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = color
    color_max = max(r, g, b)
    if color_max < 1:
        return color
    r *= (255/color_max)
    g *= (255/color_max)
    b *= (255/color_max)
    return (r, g, b)

def wash(color: tuple[int, int, int], keep_color=None) -> tuple[int, int, int]:
    r, g, b = color
    
    max_val = max(r, g, b)

    if max_val > 255:
        diff = max_val - 255
        diff_half = diff // 2

        r = min(255, r + diff_half)
        g = min(255, g + diff_half)
        b = min(255, b + diff_half)

        if keep_color:
            normalized = normalize(color)
            return(interpolate(normalized, (r, g, b), keep_color))
            
    return (r, g, b)

def color_average(colors: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    r, g, b = 0, 0, 0
    for lr, lg, lb in colors:
        r+=lr
        g+=lg
        b+=lb
    r/= len(colors)
    g/= len(colors)
    b/= len(colors)
    return (r, g, b)
        

def wash_firy(color: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = color
    
    max_val = max(r, g, b)

    if max_val > 255:
        diff = max_val - 255
        diff_half = diff // 2

        r = min(255, r + diff_half)
        g = min(255, g + diff_half)
        b = min(255, b + (diff_half // 2))
            
    return (r, g, b)

def tint_rgb(original_color, tint_color):
    """
    This function takes an original color and a tint color and returns the recolored RGB tuple,
    while preserving brightness and saturation.
    
    Parameters:
    original_color (tuple): The original RGB tuple (e.g., (128, 0, 0)).
    tint_color (tuple): The tint color as an RGB tuple (e.g., (0, 255, 0)).
    
    Returns:
    tuple: The recolored RGB tuple.
    """
    original_r, original_g, original_b = original_color
    tint_r, tint_g, tint_b = tint_color
    
    # Calculate brightness of the original color
    brightness = (original_r + original_g + original_b) / 3
    
    # Calculate saturation of the original color
    saturation = max(original_r, original_g, original_b) - min(original_r, original_g, original_b)
    
    # Calculate brightness of the tint color
    tint_brightness = (tint_r + tint_g + tint_b) / 3
    
    # Calculate saturation of the tint color
    tint_saturation = max(tint_r, tint_g, tint_b) - min(tint_r, tint_g, tint_b)
    
    # Check if the tint color is pure white or black
    if tint_brightness == 255 or tint_brightness == 0:
        return original_color
    
    # Scale the tint color to maintain brightness and saturation
    scaled_tint_r = int((tint_r / tint_brightness) * brightness)
    scaled_tint_g = int((tint_g / tint_brightness) * brightness)
    scaled_tint_b = int((tint_b / tint_brightness) * brightness)
    
    # Check if the tint color has lower saturation than the original color
    if tint_saturation < saturation:
        recolored_rgb = (original_r - (original_r - scaled_tint_r), 
                         original_g - (original_g - scaled_tint_g), 
                         original_b - (original_b - scaled_tint_b))
    else:
        recolored_rgb = (original_r + (scaled_tint_r - original_r), 
                         original_g + (scaled_tint_g - original_g), 
                         original_b + (scaled_tint_b - original_b))
    
    # Ensure the values are within the valid range (0-255)
    recolored_rgb = tuple(min(max(0, x), 255) for x in recolored_rgb)
    
    return recolored_rgb

def interpolate(color2, color1, factor):
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    return (r, g, b)

def gamma(color: tuple[int, int, int], gamma: float) -> tuple[int, int, int]:
    r, g, b = color

    rf = (r + 1) / 256.0
    gf = (g + 1) / 256.0
    bf = (b + 1) / 256.0

    r = int((rf ** gamma) * 256 - 1)
    g = int((gf ** gamma) * 256 - 1)
    b = int((bf ** gamma) * 256 - 1)

    return (r, g, b)

def decay(color: tuple[int, int, int], decay_factor: float) -> tuple[int, int, int]:
    r, g, b = color
    threshold = 1
    if r <= threshold and g <= threshold and b <= threshold: 
        return (0, 0, 0)

    decay_factor *= random.uniform(0.99, 1.01)

    # Decay-Faktor sollte im Bereich [0, 1] liegen
    decay_factor = max(0.0, min(1.0, decay_factor))

    # Abdunkeln der Farbwerte
    r = int(r * (1 - decay_factor))
    g = int(g * (1 - decay_factor))
    b = int(b * (1 - decay_factor))

    return (r, g, b)


def brighten(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> tuple[int, int, int]:
    r = max(color1[0], color2[0])
    g = max(color1[1], color2[1])
    b = max(color1[2], color2[2])
    return (r, g, b)


def shift(color: tuple[int, int, int], shift_amount: int) -> tuple[int, int, int]:
    r, g, b = color

    # RGB zu HSV konvertieren
    h, s, v = rgb_to_hsv(r, g, b)

    # Hue verschieben (im Bereich [0, 360])
    h = (h + shift_amount) % 360

    # HSV zu RGB konvertieren
    r, g, b = hsv_to_rgb(h, s, v)

    return (r, g, b)

# Hilfsfunktionen für die Umwandlung zwischen RGB und HSV
def rgb_to_hsv(r: int, g: int, b: int):
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

    return (int(h), int(s * 100), int(v * 100))

def hsv_to_rgb(h: int, s: int, v: int):
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

    return (r, g, b)

def dither(color: tuple[int, int, int], dither_amount: int) -> tuple[int, int, int]:
    r, g, b = color

    # Zufälligen Dither-Wert für jeden Farbkanal generieren
    dt = (random.randint(-dither_amount, dither_amount) / 255) + 1

    # Dither auf die Farbwerte anwenden
    r = max(0, min(255, r * dt))
    g = max(0, min(255, g * dt))
    b = max(0, min(255, b * dt))

    return (r, g, b)

def middither(color: tuple[int, int, int], intensity) -> tuple[int, int, int]:
    r, g, b = color
    
    def capdiff(n):
        if n > 127:
            return 255-n
        else:
            return n

    # Zufälligen Dither-Wert für jeden Farbkanal generieren
    factor = random.uniform(-1, 1.0) * intensity
    dither_r = int(capdiff(r) * factor)
    dither_g = int(capdiff(g) * factor)
    dither_b = int(capdiff(b) * factor)

    # Dither auf die Farbwerte anwenden
    r = max(0, r + dither_r)
    g = max(0, g + dither_g)
    b = max(0, b + dither_b)

    return (r, g, b)

def flicker_color(base_color, flicker_frequency = 20):
    
    flicker_interval = 1000 / flicker_frequency
    current_time = time.monotonic() * 1000
    elapsed_time = current_time % flicker_interval

    # Use a sine function to soften the curve
    flicker_factor = math.sin(elapsed_time * (2 * math.pi) / 1000)

    r, g, b = base_color
    x = 1
    new_color = (
        max(0, min(1024, r + int(flicker_factor * r * x))),
        max(0, min(1024, g + int(flicker_factor * g * x))),
        max(0, min(1024, b + int(flicker_factor * b * x)))
    )

    return new_color

def cycle(base_color, amount = 360, frequency = 5):
    
    flicker_interval = 1000 / frequency
    current_time = time.monotonic() * 1000
    elapsed_time = current_time % flicker_interval

    # Use a sine function to soften the curve
    factor = math.sin(elapsed_time * (2 * math.pi) / 1000) * amount
    new_color = shift(base_color, factor)
    return new_color

def add(color1: tuple[int, int, int], color2: tuple[int, int, int]):
    
    result_color = (
        color1[0] + color2[0],
        color1[1] + color2[1],
        color1[2] + color2[2]
    )

    return result_color

def multiply_val(color: tuple[int, int, int], value):
    r, g, b = color
    return (r*value, g*value, b*value)