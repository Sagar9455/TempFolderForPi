import board
import time
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Initialize I2C and OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display
oled.fill(0)
oled.show()

# Create a blank image
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load small font (adjust size for readability)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",9)

# Define multi-line text
text = """Hello Pi!
Line 2 text
Line 3 here
Line 4 display
Line 5 OLED
Line 6 tes
Line 7 trt"""

# Split text into lines
lines = text.split("\n")

# Starting Y position
y_pos = 0

# Draw each line on the display
for line in lines:
    draw.text((2, y_pos), line, font=font, fill=255)
    y_pos += 11  # Move down for next line (10 px font + 1 px spacing)


oled.image(image)
oled.show()
time.sleep(10)
oled.fill(0)
oled.show()
