from colorsys import hsv_to_rgb

__all__ = ['from_html',
           'from_hsv']


def from_html(html_color):
    """ Converts an HTML color string like FF7F00 or #c0ffee to RGB. """
    num = int(html_color.lstrip('#'), 16)
    return [num // 65536, (num // 256) % 256, num % 256]


def from_hsv(h: float, s: float, v: float):
    """ Converts HSV (float values between 0 and 1) colors to RGB. """
    r, g, b = hsv_to_rgb(h, s, v)
    return [int(r*255), int(g*255), int(b*255)]
