import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

class DisplayHandler:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c, addr=0x3C)
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)

    def display_text(self, text, y=10):
        """Display text on OLED"""
        self.oled.fill(0)
        self.oled.show()

        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)

        draw.text((5, y), text, font=self.font, fill=255)

        self.oled.image(image)
        self.oled.show()