#!/usr/bin/env python

# PIL raster font compiler
# https://github.com/python-pillow/pillow-scripts/blob/main/Scripts/pilfont.py
#
# The Python Imaging Library (PIL) licensed under the PIL Software License
#
# Copyright © 1997-2011 by Secret Labs AB
# Copyright © 1995-2011 by Fredrik Lundh
# Copyright © 2010-2017 by Alex Clark and contributors
#
# history:
# 1997-08-25 fl   created
# 2002-03-10 fl   use "from PIL import"

from __future__ import print_function

import glob
import sys

# drivers
from PIL import BdfFontFile
from PIL import PcfFontFile

VERSION = "0.4"

if len(sys.argv) <= 1:
    print("PILFONT", VERSION, "-- PIL font compiler.")
    print()
    print("Usage: pilfont fontfiles...")
    print()
    print("Convert given font files to the PIL raster font format.")
    print("This version of pilfont supports X BDF and PCF fonts.")
    sys.exit(1)

files = []
for f in sys.argv[1:]:
    files = files + glob.glob(f)

for f in files:

    print(f + "...", end=' ')

    try:

        fp = open(f, "rb")

        try:
            p = PcfFontFile.PcfFontFile(fp)
        except SyntaxError:
            fp.seek(0)
            p = BdfFontFile.BdfFontFile(fp)

        p.save(f)

    except (SyntaxError, IOError):
        print("failed")

    else:
        print("OK")
