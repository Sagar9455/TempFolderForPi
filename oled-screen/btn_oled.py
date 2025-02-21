import time
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image,ImageDraw,ImageFont
from gpiozero import Button



button1 = Button(12)
button2 = Button(16)
button3 = Button(20)
button4 = Button(21)


i2c=busio.I2C(board.SCL,board.SDA)
oled=SSD1306_I2C(128,64,i2c,addr=0x3C)


oled.fill(0)
oled.show()
image=Image.new("1",(oled.width,oled.height))
draw=ImageDraw.Draw(image)

font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",9)
#font=ImageFont.load_default()
if button1.is_pressed or button2.is_pressed or button3.is_pressed or button4.is_pressed :
		print("The button was pressed")
		draw.text((0,0),"The button was pressed",font=font,fill=7)
		



#draw.text((0,0),"Select what to do:,\n1 Test Case Execution\n2 ECU Updation\n3 Exit",font=font,fill=7)


oled.image(image)
oled.show()

time.sleep(10)

oled.fill(0)
oled.show()


