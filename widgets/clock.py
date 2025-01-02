import os
from glob import glob
from time import sleep
from datetime import datetime as dt

from PIL import Image, ImageFont, ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from weather import OpenWeather

__author__  = "Michael Pascale"
__copyright__ = "Copyright 2024, Michael Pascale"
__credits__ = ["Henner Zeller"]
__license__ = "MIT"


# Define some configuration options.
# TODO: Extract these as command-line arguments.
XWIDTH  = 64
YHEIGHT = 32

FONT_DEFAULT = 0
FONT_SMALL = 1
TEXT_COLOR = (163,255,180)

fonts = [
    ImageFont.load('fonts/5x8.pil'), # Default
    ImageFont.load('fonts/4x6.pil')  # Small
]

REFRESH_RATE = 1 # Hz

STRF_HR24 = True
# STRF_TIME = "%H:%M:%S" if STRF_HR24 else "%I:%M:%S %p"
# STRF_DATE = "%A %d %b, %Y"
STRF_TIME = "%H:%M" if STRF_HR24 else "%I:%M %p"
# STRF_DATE = "%a, %b %-d"
STRF_DATE = "%a %-m/%-d"

# Icons
iconfiles = glob('widgets/icons/*.bmp')
icons = {os.path.basename(file)[:-4]: Image.open(file).convert('RGB') for file in iconfiles}

weather = OpenWeather(OW_KEY, OW_LAT, OW_LON, freq=30)


# RGB Matrix
options = RGBMatrixOptions()
options.rows = YHEIGHT
options.cols = XWIDTH
options.gpio_slowdown = 4 # For RPi4

matrix = RGBMatrix(options=options)
image = Image.new('RGB', (XWIDTH, YHEIGHT), (0,0,0))
draw  = ImageDraw.Draw(image)

while(True):
    now = dt.now()
    str_time = now.strftime(STRF_TIME)
    str_date = now.strftime(STRF_DATE)
    str_temp = "%.0d°F" % weather.current()['temp']

    # FIXME: implement other weather types
    # Is there rain in the weather events or precipitation in the next hour?
    is_rain  = any([event['main'] == 'Rain' for event in weather.current()['weather']]) or any(weather.precipitation()[:,1] > 0)
    
    # Clear the image.
    draw.rectangle([(0,0), image.size], fill=(0,0,0))

    # Draw the time and date.

    # TIME
    _,_,text_width,text_height = fonts[FONT_DEFAULT].getbbox(str_time)
    text_x = (XWIDTH // 2 - text_width) // 2
    text_y = (YHEIGHT - text_height) // 2

    draw.text((text_x, text_y), str_time, fill=TEXT_COLOR, font=fonts[FONT_DEFAULT])

    # DATE
    offset_y = text_height + 1

    _,_,text_width,text_height = fonts[FONT_SMALL].getbbox(str_date)

    text_y = (YHEIGHT - text_height) // 2 + offset_y # keep same x as time

    draw.text((text_x, text_y), str_date, fill=TEXT_COLOR, font=fonts[FONT_SMALL])

    # Draw a vertical bar at x=32
    draw.line([(XWIDTH // 2+2, 5), (XWIDTH // 2+2, YHEIGHT-7)], fill="white")

    # TEMPERATURE
    _,_,text_width,text_height = fonts[FONT_SMALL].getbbox(str_temp)
    text_x = (XWIDTH // 2 - text_width) // 2 + XWIDTH // 2
    text_y = (YHEIGHT - text_height) // 2 + offset_y

    draw.text((text_x, text_y), str_temp, fill=TEXT_COLOR, font=fonts[FONT_SMALL])

    if is_rain:
        image.paste(icons['rain'], (41, 3))
    else:
        image.paste(icons['sun'], (41, 3))

    # image.save('out.png')


    matrix.Clear()
    matrix.SetImage(image)

    sleep(REFRESH_RATE)
