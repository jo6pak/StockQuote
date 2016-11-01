#!/usr/bin/env python

import time
import ystockquote

from termcolor import colored
from datetime import datetime

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP

import logging

#####################################################################
# MCP23017 not working as advertised. Shows up as i2C device 
# but lcd functions dont work properly. Investigate later, use gpios to 
# drive LCD for now
#####################################################################

# Define MCP pins connected to the LCD.
#lcd_rs        = 0
#lcd_en        = 1
#lcd_d4        = 2
#lcd_d5        = 3
#lcd_d6        = 4
#lcd_d7        = 5
#lcd_backlight = 6

# Optionally if the backlight is not controllable then set:
# lcd_backlight = None

# Define LCD column and row size for 16x2 LCD.
#lcd_columns = 16
#lcd_rows    = 2

# Initialize MCP23017 device using its default 0x20 I2C address.
#gpio = MCP.MCP23017()

# Initialize the LCD using the pins
#lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
#                           lcd_columns, lcd_rows, lcd_backlight, gpio=gpio)

##############################################################################

# Default: Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()

lcd.clear()

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

empty_space = '                '
##############################################################################

def post_quote(quote, price, change):
	
	# Clear LCD, reset cursor
	lcd.clear()

	# Set LCd backlight color to red or green 
	try:
		if float(change) < 0:
        		lcd.set_color(1.0,0.0,0.0)
			#print colored(elem + ": " + price + " " + change, 'red')
		else:
			lcd.set_color(0.0,1.0,0.0)
			#print colored(elem + ": " + price + " " + change, 'green')
	except Exception: 
		print("Debug: Post Quote exception")
		pass
	# Quote on first line + price info on second line
	lcd.message(empty_space + quote + '\n' + empty_space + price + ' ' + change)
	
	for i in range(lcd_columns):
        	time.sleep(0.35)
		lcd.move_left()
       
        return 0

##############################################################################

# Run in a loop
while 1:
	with open('/home/pi/StockQuote/quotelist') as f:
		tickerSymbol = f.read().splitlines()

	# parse the ticker symbol list for individual symbols and print out current price and change since previous days close.
	for elem in tickerSymbol:	
		try: allInfo = ystockquote.get_all(elem)
		except Exception:
			print("Debug: Hit Exception...ignore")
			pass
		post_quote(elem, allInfo["price"], allInfo["change"])
	
