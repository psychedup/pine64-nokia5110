#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  nokia_test.py
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

import math
import time
import Nokia5110 as nokia
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

DC = 23
RST = 24
LED = 12
SPIDEV = "/dev/spidev0.0"
LCDCONTRAST = 65

def main(args):
	
	# setup
	disp = nokia.Nokia5110( SPIDEV, DC, RST, LED, 0 )
		
	# initialize device, set contrast
	disp.reset()
	disp.set_contrast( LCDCONTRAST )
	
	# Clear display
	disp.clear()
	disp.display()
	
	# Create blank image for drawing
	# Make sure to create new image with mode '1' for 1-bit color.
	image = Image.new( '1', ( nokia.LCDWIDTH, nokia.LCDHEIGHT ) )
	
	# Get drawing object to draw on image.
	draw = ImageDraw.Draw( image )
	
	# Draw a white filled box to clear the image.
	draw.rectangle( ( 0, 0, nokia.LCDWIDTH-1, nokia.LCDHEIGHT-1 ), outline = 1, fill = 1 )
	
	# Draw some shapes.
	draw.ellipse( ( 2, 2, 22, 22 ), outline = 0, fill = 1 )
	draw.rectangle( ( 24, 2, 44, 22 ), outline = 0, fill = 1 )
	draw.polygon( [ ( 46, 22 ), ( 56, 2 ), ( 66,22 ) ], outline = 0, fill = 1 )
	draw.line( ( 68,22, 81, 2 ), fill = 0 )
	draw.line( ( 68, 2, 81, 22 ), fill = 0 )
	
	# Load default font.
	font = ImageFont.load_default()	
	
	# Alternatively load a TTF font.
	# some nice fonts to try: http://www.dafont.com/bitmap.php
	# font = ImageFont.truetype( 'Minecraftia.ttf', 8 )
	
	# Write some text.
	draw.text( ( 8, 30 ), 'Hello World!', 0, font = font )
	
	# Display image
	disp.image( image )
	disp.display()
	
	# fade brightness in
	for t in range( 0, 101 ):
		disp.brightness( t )
		time.sleep( 0.1 )
	
	# now fade out
	for t in range( 100, -1, -1 ):
		disp.brightness( t )
		time.sleep( 0.1 )
	
	disp.clear()
	disp.display()

	disp.cleanup()
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
