import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Initialize I2C and OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Load font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)

def display_text(text, y=10):
    oled.fill(0)  # Clear screen
    oled.show()

    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((5, y), text, font=font, fill=255)

    oled.image(image)
    oled.show()
