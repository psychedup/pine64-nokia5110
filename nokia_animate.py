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
LCDCONTRAST = 70

def main(args):
	
	# setup
	disp = nokia.Nokia5110( SPIDEV, DC, RST, LED )
	
	# Initialize device, set contrast
	disp.reset()
	disp.set_contrast( LCDCONTRAST )
	
	# clear display
	disp.clear()
	disp.display()
	
	# Create image buffer.
	# Make sure to create image with mode '1' for 1-bit color.
	image = Image.new( '1', ( nokia.LCDWIDTH, nokia.LCDHEIGHT ) )
	
	# Load default font.
	font = ImageFont.load_default()
	
	# Create drawing object.
	draw = ImageDraw.Draw( image )
	
	# Define text and get total width.
	text = 'NOKIA 5110: NOT JUST FOR SNAKE ANYMORE. THIS IS AN OLD SCHOOL DEMO SCROLLER!! GREETZ TO: LADYADA & THE ADAFRUIT CREW, TRIXTER, FUTURE CREW, AND FARBRAUSCH'
	maxwidth, height = draw.textsize( text, font = font )
	
	# Set starting position
	startpos = 83
	pos = startpos
	
	# Animate text moving in sine wave.
	print( 'Press Ctrl-C to quit.' )

	
	try:
		while True:
			# Clear image buffer.
			draw.rectangle( ( 0, 0, 83, 47 ), outline = 255, fill = 255 )
			
			# Enumerate characters and draw them offset vertically based on a sine wave.
			x = pos
			for i, c in enumerate( text ):
				# Stop drawing if off the right side of screen.
				if x > 83:
					break
				# Calculate width but skip drawing if off the left side of screen.
				if x < -10:
					width, height = draw.textsize( c, font = font )
					x += width
					continue
				# Calculate offset from sine wave.
				y = ( 24 - 8 ) + math.floor( 10.0 * math.sin( x / 83.0 * 2.0 * math.pi ) )
				# Draw text
				draw.text( ( x, y ), c, font = font, fill = 0 )
				# Increment x position based on character width.
				width, height = draw.textsize( c, font = font )
				x += width
				# draw the image buffer.
				disp.image( image )
				disp.display()
				# Move position for next frame.
				pos -= 2
				# Start over if text has scrolled completely off left side of screen.
				if pos < -maxwidth:
					pos = startpos
			# Pause briefly before drawing next frame.
			time.sleep( 0.2 )
	
	except( KeyboardInterrupt, SystemExit ):
		disp.cleanup()
		return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
