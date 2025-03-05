import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import os
import can
import threading

# Initialize I2C and OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Load font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)

# Setup CAN interface
os.system('sudo ip link set can0 type can bitrate 500000')  # Set bitrate to 500kbps
os.system('sudo ifconfig can0 up')

bus = can.Bus(interface="socketcan", channel="can0", bitrate=1000000)  # Standard CAN (8-byte frames)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
buttons = [12, 16, 20, 21]
for btn in buttons:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

# Function to send CAN message
def CAN_Send(bt):
    messages = {
        12: (0x123, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]),
        16: (0x456, [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]),
        20: (0x789, [0x10, 0xFF, 0x02, 0x03, 0xBC, 0x05, 0x06, 0x07]),
        21: (0x111, [0xFF] * 8),
    }
    if bt in messages:
        msg_id, data = messages[bt]
        msg = can.Message(arbitration_id=msg_id, is_extended_id=False, data=data)
        bus.send(msg)
       #display_text(f"Sent: ID {hex(msg_id)}", y=15)
        display_text(f"Sent:\nID: {hex(msg_id)}\nData:\n{bytes(data).hex()}", y=15)
      

# Function to receive, modify, and respond
def CAN_Receive_And_Respond():
    """Receives CAN message, modifies ID & data, and sends back"""
    while True:
        msg = bus.recv()  # Wait for a message
        if msg:
            received_id = msg.arbitration_id
            data = list(msg.data)

            # Display received message
            display_text(f"Received Message:\nID {hex(received_id)}\nData: {msg.data.hex()}", y=15)
            time.sleep(1)
            # Modify ID and data
            new_id = (received_id + 1) & 0x7FF  # Keep ID within 11-bit range
            new_data = [(b + 1) & 0xFF for b in data]  # Increment data bytes

            # Send modified message
            response_msg = can.Message(arbitration_id=new_id, is_extended_id=False, data=new_data)
            bus.send(response_msg)

            # Display updated message
            display_text(f"Sent:\nID:  {hex(new_id)}\nData: {bytes(new_data).hex()}", y=15)

# Welcome Message
display_text("Welcome to CAN Demo")
time.sleep(1.5)

# Start CAN receiving and responding in a separate thread
rx_thread = threading.Thread(target=CAN_Receive_And_Respond, daemon=True)
rx_thread.start()

# Main loop for button input
try:
    while True:
        oled.fill(0)  # Clear screen
        oled.show()
        display_text("Press a Button to Send:\n1. 0x123\n2. 0x456\n3. 0x789\n4. 0x111", y=0)

        while True:
            for i, btn in enumerate(buttons, start=1):
                if GPIO.input(btn) == GPIO.LOW:  # Button pressed
                    CAN_Send(btn)  # Send CAN message
                    #display_text("Press a Button to Send:\n1. 0x123\n2. 0x456\n3. 0x789\n4. 0x111", y=0) #If we want to see the menu which message to be sent then there will be button latnecy issue
                    #time.sleep(0.5)  # Debounce delay
                    #break  # Restart message display

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    bus.shutdown()  # Properly close CAN interface
    GPIO.cleanup()  # Clean up GPIO before exiting
    oled.fill(0)  # Clear screen
    oled.show()
