import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define button pins
buttons = [12, 16, 20, 21]

# Set up buttons as input with pull-up resistors
for btn in buttons:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize I2C and OLED
#i2c = busio.I2C(board.SCL, board.SDA, frequency=400000
i2c = busio.I2C(board.SCL, board.SDA)

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Load small font (adjust size for readability)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)

def display_text(text):
    """Function to display text on OLED"""
    oled.fill(0)  # Clear screen
    oled.show()

    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    # Draw text at the top
    draw.text((5, 25), text, font=font, fill=255)

    # Display image on OLED
    oled.image(image)
    oled.show()

# Continuous loop to check for button presses
try:
    while True:
        for i, btn in enumerate(buttons, start=1):
            if GPIO.input(btn) == GPIO.LOW:  # Button pressed
                display_text(f"Button {i} Pressed")
        time.sleep(0.2)  # Small debounce delay

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.cleanup()  # Clean up GPIO before exiting
