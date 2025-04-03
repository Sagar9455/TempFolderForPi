import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont


# Initialize I2C and OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Load font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)


# Function to display text on OLED
def display_text(text, y=10):
    """Function to display text on OLED"""
    oled.fill(0)  # Clear screen
    oled.show()

    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    # Draw text on OLED
    draw.text((5, y), text, font=font, fill=255)

    # Display image on OLED
    oled.image(image)
    oled.show()
