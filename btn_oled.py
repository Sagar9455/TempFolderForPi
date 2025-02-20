import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button

# Define buttons (use correct variable names)
button1 = Button(12)
button2 = Button(16)
button3 = Button(20)
button4 = Button(21)

# Initialize I2C and OLED
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
        if button1.is_pressed:
            display_text("Button 1 Pressed")
        elif button2.is_pressed:
            display_text("Button 2 Pressed")
        elif button3.is_pressed:
            display_text("Button 3 Pressed")
        elif button4.is_pressed:
            display_text("Button 4 Pressed")
        time.sleep(0.2)  # Small debounce delay

except KeyboardInterrupt:
    print("\nExiting...")
