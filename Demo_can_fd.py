#imports
import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import os
import can

#function definitions
def display_text(text, y):
    """Function to display text on OLED"""
    oled.fill(0)  # Clear screen
    oled.show()

    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    # Draw text at the top
    draw.text((5, y), text, font=font, fill=255)

    # Display image on OLED
    oled.image(image)
    oled.show()


def CAN_Send(bt):
	match bt:
		case 12:
			msg = can.Message(arbitration_id=0x123,  is_extended_id=False, is_fd=True,data=bytearray([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]))
			bus.send(msg)
		case 16:
			msg = can.Message(arbitration_id=0x456,  is_extended_id=False, is_fd=True,data=bytearray([0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x09, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]))
			bus.send(msg)
		case 20:
			msg = can.Message(arbitration_id=0x789,  is_extended_id=False, is_fd=True,data=bytearray([0x10, 0xFF, 0x02, 0x03, 0xBC, 0x05, 0x06, 0x07, 0x08, 0x09, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]))
			bus.send(msg)
		case 21:
			msg = can.Message(arbitration_id=0x111,  is_extended_id=False, is_fd=True,data=bytearray([0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF]))
			bus.send(msg)

bt = False

# Initialize I2C and OLED
#i2c = busio.I2C(board.SCL, board.SDA, frequency=400000
i2c = busio.I2C(board.SCL, board.SDA)

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Load small font (adjust size for readability)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)

# CAN channel Up
os.system('sudo ip link set can0 type can bitrate 100000')
os.system('sudo ifconfig can0 up')
bus=can.Bus(interface="socketcan",channel="can0",bitrate=1000000,fd=True)

#Welcome note and Menu
y = 25
display_text(f"Welcome\nDemo on RaspberryPi",y)
time.sleep(1.5)
while 1:
	# Set up GPIO mode
	GPIO.setmode(GPIO.BCM)


	# Define button pins
	buttons = [12, 16, 20, 21]

	# Set up buttons as input with pull-up resistors
	for btn in buttons:
		GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	a = True
	oled.fill(0)  # Clear screen
	oled.show()
	time.sleep(0.5)
	y = 0

	display_text(f"Select a CAN msg:\n1. CAN ID: 0x123\n2. CAN ID: 0x456\n3. CAN ID: 0x789\n4. CAN ID: 0x111",y)
	#time.sleep(0.5)
	#input

	try:
		while a==True:
			for i, btn in enumerate(buttons, start=1):
				if GPIO.input(btn) == GPIO.LOW:  # Button pressed
					bt = btn
					CAN_Send(bt)
					display_text(f"{i} Pressed\nMessage is Sent\nCheck in PCAN",y)
					a = False
					time.sleep(0.5)  # Small debounce delay

	except KeyboardInterrupt:
		print("\nExiting...")

	finally:
		GPIO.cleanup()  # Clean up GPIO before exiting



y = False
display_text("Msg sent on CAN\nCheck in PCAN Viewer",y)
bus.shutdown

oled.fill(0)  # Clear screen
oled.show()
