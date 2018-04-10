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

import time
import math
import Nokia5110 as nokia
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

DC = 23
RST = 24
LED = 12
SPIDEV = "/dev/spidev0.0"
LCDCONTRAST = 70

def main(args):
	
	# setup
	disp = nokia.Nokia5110( SPIDEV, DC, RST, LED )
	
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
	
	draw.rectangle( ( 0, 0, nokia.LCDWIDTH-1, nokia.LCDHEIGHT-1 ), outline = 1, fill = 1 )
		
	while True:
		try:
			draw.ellipse( ( 18, 0, 65, 47 ), outline = 0, fill = 0 )
			
			clk_hr = time.localtime().tm_hour
			if clk_hr > 12:
				clk_hr -= 12
			
			clk_min = time.localtime().tm_min
			
			center_x = 42
			center_y = 24
			
			hr_end_x = 10 * math.cos( math.radians( clk_hr * 5 * 6 ) - math.radians( 90 ) ) + center_x
			hr_end_y = 10 * math.sin( math.radians( clk_hr * 5 * 6 ) - math.radians( 90 ) ) + center_y
			
			min_end_x = 15 * math.cos( math.radians( clk_min * 6 ) - math.radians( 90 ) ) + center_x
			min_end_y = 15 * math.sin( math.radians( clk_min * 6 ) - math.radians( 90 ) ) + center_y
			
			draw.line( ( center_x, center_y, hr_end_x, hr_end_y ), 1 )
			draw.line( ( center_x, center_y, min_end_x, min_end_y ), 1 )
			
			disp.image( image )
			disp.display()
			
			time.sleep( 60 )
		
		except( KeyboardInterrupt, SystemExit ):
			disp.cleanup()
			return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
