import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import os
import serial
import threading

# Initialize I2C and OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Load font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)

# Setup RS485 (Using /dev/serial0, modify as needed)
ser = serial.Serial(
    port='/dev/serial0',  # Change to your RS485 device port
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

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

# Function to send RS485 message
def RS485_Send(bt):
    messages = {
        12: (0x123, [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]),
        16: (0x456, [0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]),
        20: (0x789, [0x10, 0xFF, 0x02, 0x03, 0xBC, 0x05, 0x06, 0x07]),
        21: (0x111, [0xFF] * 8),
    }
    if bt in messages:
        msg_id, data = messages[bt]
        payload = bytearray([msg_id >> 8, msg_id & 0xFF] + data)  # ID + Data
        ser.write(payload)  # Send over RS485
        display_text(f"Sent: ID {hex(msg_id)}", y=15)

# Function to receive, modify, and respond
def RS485_Receive_And_Respond():
    """Receives RS485 message, modifies ID & data, and sends back"""
    while True:
        received_data = ser.read(10)  # Read incoming data (max 10 bytes)
        if received_data:
            received_id = (received_data[0] << 8) | received_data[1]
            data = list(received_data[2:])  # Extract data

            # Display received message
            display_text(f"RX: ID {hex(received_id)}\nData: {received_data.hex()}", y=25)

            # Modify ID and data
            new_id = received_id + 1
            new_data = [(b + 1) & 0xFF for b in data]  # Increment data bytes

            # Send modified message
            response_payload = bytearray([new_id >> 8, new_id & 0xFF] + new_data)
            ser.write(response_payload)

            # Display updated message
            display_text(f"TX: ID {hex(new_id)}\nData: {response_payload.hex()}", y=45)

# Welcome Message
display_text("Welcome to RS485 Demo")
time.sleep(1.5)

# Start RS485 receiving and responding in a separate thread
rx_thread = threading.Thread(target=RS485_Receive_And_Respond, daemon=True)
rx_thread.start()

# Main loop for button input
try:
    while True:
        oled.fill(0)  # Clear screen
        oled.show()
        display_text("Press a Button to Send:\n1. 0x123\n2. 0x456\n3. 0x789\n4. 0x111", y=5)

        while True:
            for i, btn in enumerate(buttons, start=1):
                if GPIO.input(btn) == GPIO.LOW:  # Button pressed
                    RS485_Send(btn)  # Send RS485 message
                    time.sleep(0.5)  # Debounce delay
                    break  # Restart message display

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    ser.close()  # Properly close RS485 connection
    GPIO.cleanup()  # Clean up GPIO before exiting
    oled.fill(0)  # Clear screen
    oled.show()
