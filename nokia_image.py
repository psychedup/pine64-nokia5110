#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  nokia_image.py
#  
#  Copyright 2018 Unknown <chris@pinetoo>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import time
import math
import Nokia5110 as nokia
from PIL import Image, ImageDraw, ImageFont

DC = 23
RST = 24
LED = 12
SPIDEV = "/dev/spidev0.0"
LCDCONTRAST = 65

def main(args):
	
	# setup
	disp = nokia.Nokia5110( SPIDEV, DC, RST, LED )
	
	# Initialize device, set contrast
	disp.reset()
	disp.set_contrast( LCDCONTRAST )
	
	# clear display
	disp.clear()
	disp.display()
	
	# Load image and convert to 1 bit color.
	image = Image.open( 'happycat_lcd.ppm' ).convert( '1' )
	
	# Display image.
	disp.image( image )
	disp.display()
	
	print( 'Press Ctrl-C to quit.' )
	try:
		while True:
			time.sleep( 1.0 )
	except( KeyboardInterrupt, SystemExit ):
		disp.cleanup()
		return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
