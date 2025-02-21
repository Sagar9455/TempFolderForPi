import time
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image,ImageDraw,ImageFont

i2c=busio.I2C(board.SCL,board.SDA)
oled=SSD1306_I2C(128,64,i2c,addr=0x3C)


oled.fill(0)
oled.show()
image=Image.new("1",(oled.width,oled.height))
draw=ImageDraw.Draw(image)

font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",9)
#font=ImageFont.load_default()
draw.text((0,0),"Select what to do:,\n1 Test Case Execution\n2 ECU Updation\n3 Exit",font=font,fill=7)


oled.image(image)
oled.show()

time.sleep(10)

oled.fill(0)
oled.show()
