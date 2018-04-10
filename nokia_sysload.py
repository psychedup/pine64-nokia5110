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
	
	graph_value = [ 0 ] * 84

	try:
		while True:
			# Clear image buffer.
			draw.rectangle( ( 0, 0, 83, 47 ), outline = 255, fill = 255 )
			
			# Get system load
			with open( '/proc/loadavg', 'r' ) as lf:
				read_sysload = lf.read()
			
			load = read_sysload.split( " " )[ 0 : 3 ]
			
			# Write the value
			draw.text( ( 0, 0 ), load[ 0 ] + " " + load[ 1 ] + " " + load[ 2 ], 0, font = font )
			
			# add most recent value to position 83
			graph_value[ 83 ] = load[ 0 ]
			
			graph_scale = 1.0
			
			# draw graph columns
			for col in range( 84 ):
				l_height = float( graph_value[ col ] ) / graph_scale
				y_top = 48 - int( l_height )
				draw.line( ( col - 1, 48, col - 1, y_top ), fill = 0 )
				#draw.line( ( 83, 48, 83, 0 ), fill = 0 )
			
			# draw the image buffer.
			disp.image( image )
			disp.display()

			# Pause briefly before drawing next frame.
			time.sleep( 5 )
	
	except( KeyboardInterrupt, SystemExit ):
		disp.cleanup()
		return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
