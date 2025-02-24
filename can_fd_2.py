import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import os
import can

# Function to display text on OLED
def display_text(text, y=25):
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

# Function to send CAN message
def CAN_Send(bt):
    messages = {
        12: (0x123, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]),
        16: (0x456, [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x09, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]),
        20: (0x789, [0x10, 0xFF, 0x02, 0x03, 0xBC, 0x05, 0x06, 0x07, 0x08, 0x09, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]),
        21: (0x111, [0xFF] * 16),
    }
    if bt in messages:
        arbitration_id, data = messages[bt]
        msg = can.Message(arbitration_id=arbitration_id, is_extended_id=False, is_fd=True, data=bytearray(data))
        bus.send(msg)

# Initialize I2C and OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Load font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)

# Setup CAN interface
os.system('sudo ip link set can0 type can bitrate 1000000')  # Ensure correct bitrate
os.system('sudo ifconfig can0 up')
bus = can.Bus(interface="socketcan", channel="can0", bitrate=1000000, fd=True)

# Welcome Message
display_text("Welcome\nDemo on RaspberryPi")
time.sleep(1.5)

# Set up GPIO once
GPIO.setmode(GPIO.BCM)
buttons = [12, 16, 20, 21]
for btn in buttons:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Main loop
try:
    while True:
        oled.fill(0)  # Clear screen
        oled.show()
        display_text("Select a CAN msg:\n1. CAN ID: 0x123\n2. CAN ID: 0x456\n3. CAN ID: 0x789\n4. CAN ID: 0x111")

        while True:
            for i, btn in enumerate(buttons, start=1):
                if GPIO.input(btn) == GPIO.LOW:  # Button pressed
                    CAN_Send(btn)
                    display_text(f"{i} Pressed\nMessage Sent\nCheck in PCAN")
                    time.sleep(0.5)  # Debounce delay
                    break  # Exit inner loop to restart message display

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    bus.shutdown()  # Properly close CAN interface
    GPIO.cleanup()  # Clean up GPIO before exiting
    oled.fill(0)  # Clear screen
    oled.show()
