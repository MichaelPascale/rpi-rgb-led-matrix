from time import sleep
from datetime import datetime as dt

from PIL import ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions

__author__  = "Michael Pascale"
__copyright__ = "Copyright 2024, Michael Pascale"
__credits__ = ["Henner Zeller"]
__license__ = "MIT"


# Define some configuration options.
# TODO: Extract these as command-line arguments.
XWIDTH  = 64
YHEIGHT = 32

FONT_TIME = 0
FONT_DATE = 1

fonts = [
    ImageFont.load('fonts/5x8.pil'), # Default
    ImageFont.load('fonts/4x6.pil')  # Small
]

REFRESH_RATE = 1 # Hz

STRF_HR24 = True
# STRF_TIME = "%H:%M:%S" if STRF_HR24 else "%I:%M:%S %p"
# STRF_DATE = "%A %d %b, %Y"
STRF_TIME = "%H:%M" if STRF_HR24 else "%I:%M %p"
STRF_DATE = "%a, %b %d"


options = RGBMatrixOptions()
options.rows = YHEIGHT
options.cols = XWIDTH
options.gpio_slowdown = 4 # For RPi4

matrix = RGBMatrix(options=options)


while(True):
    now = dt.now()
    str_time = now.strftime(STRF_TIME)
    str_date = now.strftime(STRF_DATE)


    fonts[FONT_TIME].getbbox(str_time)
    fonts[FONT_DATE].getbbox(str_date)

    # matrix.SetImage(image.convert('RGB'))
    sleep(REFRESH_RATE)


