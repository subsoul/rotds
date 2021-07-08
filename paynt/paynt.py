"""
This paints, THis is for my fun only
Author: Adewale Azeez
"""

import sys
import time
import numpy
from math import sqrt
from PIL import Image
import win32api, win32con, win32ui, win32gui, win32process

COLORS = (
    (0, 0, 0),
    (127, 127, 127),
    (136, 0, 21),
    (237, 28, 36),
    (255, 127, 39),
    (255, 242, 0),
    (34, 177, 76),
    (0, 162, 232),
    (63, 72, 204),
    (163, 73, 164),
    (255, 255, 255),
    (195, 195, 195),
    (136, 0, 21),
    (237, 28, 36),
    (255, 127, 39),
    (255, 242, 0),
    (34, 177, 76),
    (0, 162, 232),
    (63, 72, 204),
    (163, 73, 164),
)

COLOR_PALETTE_MAP = {
    "#000000": (765, 62), #(0, 0, 0)
    "#7f7f7f": (785, 62), #(127, 127, 127)
    "#880015": (805, 62), #(136, 0, 21)
    "#ed1c24": (825, 62), #(237, 28, 36)
    "#ff7f27": (850, 62), #(255, 127, 39)
    "#fff200": (870, 62), #(255, 242, 0)
    "#22b14c": (895, 62), #(34, 177, 76)
    "#00a2e8": (915, 62), #(0, 162, 232)
    "#3f48cc": (940, 62), #(63, 72, 204)
    "#a349a4": (960, 62), #(163, 73, 164)
    "#ffffff": (765, 85), #(255, 255, 255)
    "#c3c3c3": (785, 85), #(195, 195, 195)
    "#880015": (805, 85), #(136, 0, 21)
    "#ed1c24": (825, 85), #(237, 28, 36)
    "#ff7f27": (850, 85), #(255, 127, 39)
    "#fff200": (870, 85), #(255, 242, 0)
    "#22b14c": (895, 85), #(34, 177, 76)
    "#00a2e8": (915, 85), #(0, 162, 232)
    "#3f48cc": (940, 85), #(63, 72, 204)
    "#a349a4": (960, 85), #(163, 73, 164)
}

PAYNT_MOUSE_LEFT_CLICK = 0
PAYNT_MOUSE_MIDDLE_CLICK = 1
PAYNT_MOUSE_RIGHT_CLICK = 2

def move_cursor(x, y):
    win32api.SetCursorPos((x, y))


move_cursor(960, 62)

def send_click_event(x, y, button = PAYNT_MOUSE_LEFT_CLICK):
    win32api.SetCursorPos((x, y))
    time.sleep(0.0001)
    if button == PAYNT_MOUSE_LEFT_CLICK:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    elif button == PAYNT_MOUSE_MIDDLE_CLICK:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, x, y, 0, 0)
    elif button == PAYNT_MOUSE_RIGHT_CLICK:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

def send_double_click_event(x, y, button = PAYNT_MOUSE_LEFT_CLICK):
    send_click_event(x, y, button)
    send_click_event(x, y, button)

def find_paint_window():
    window = win32ui.FindWindow(None, "Untitled - Paint")
    return window

def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, "r")
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == "RGB":
        channels = 3
    elif image.mode == "L":
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values

def read_image_pixel_array(image_path):
    im = Image.open(image_path) # Can be many different formats.
    pix = im.load()
    width, height = im.size
    return (width, height, list(im.getdata()))

def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

def get_color_pos_is_palette(r, g, b):
    ccolor = closest_color((r, g, b))
    hex_value = '#%02x%02x%02x' % (ccolor[0], ccolor[1], ccolor[2])
    if hex_value not in COLOR_PALETTE_MAP:
        print("Cannot find closest for ", (r, g, b))
        exit(0)
    return COLOR_PALETTE_MAP[hex_value]

def select_color(r, g, b):
    color_tuple = get_color_pos_is_palette(r, g, b)
    send_click_event(color_tuple[0], color_tuple[1])

def select_pencil_tool():
    send_click_event(245, 75)

def prepare_paint_window():
    window = find_paint_window()
    window.SetActiveWindow()
    window.SetForegroundWindow()
    window.SetWindowPos(win32con.HWND_DESKTOP, (0, 0, 0, 0), win32con.SWP_NOZORDER | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
    send_double_click_event(150, 10)
    select_pencil_tool()

def begin_draw(pixel_values):
    xindex = pixel_values.shape[0]
    yindex = 0
    for pixel_value in (pixel_values):
        xindex = pixel_values.shape[0]
        for sub_pixel_value in (pixel_value):
            print(sub_pixel_value)
            select_color(sub_pixel_value[0], sub_pixel_value[1], sub_pixel_value[2])
            send_click_event(13 + xindex, 152 + yindex)
            xindex -= 1
        yindex += 1

def main(argc, argv):
    #image = get_image("C:/Users/azeez/Pictures/Screenshots/Screenshot (1) - Copy.jpg")
    #prepare_paint_window()
    #begin_draw(image)
    #print(image.shape)
    pass

main(len(sys.argv), sys.argv)