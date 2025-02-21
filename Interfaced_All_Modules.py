import RPi.GPIO as GPIO
import can
import time
from adafruit_ssd1306 import SSD1306_I2C
import board
import busio

# GPIO Button Configuration (1x4 Membrane Switch)
BUTTON_PINS = [5, 6, 13, 19]  # Adjust based on your wiring

# I2C Display Configuration (SSD1306)
I2C_ADDR = 0x3C  # Default address for SSD1306
i2c = busio.I2C(board.SCL, board.SDA)
display = SSD1306_I2C(128, 64, i2c)

# CAN Bus Setup (RS485 CAN HAT)
can_interface = "can0"

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for pin in BUTTON_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up resistor

def send_can_message(button_index):
    """Send a CAN message with a specific button ID."""
    try:
        bus = can.interface.Bus(can_interface, bustype="socketcan")
        message = can.Message(arbitration_id=0x123, data=[button_index, 0xAA, 0xBB], is_extended_id=False)
        bus.send(message)
        print(f"Sent CAN Message: {message}")
        display_message(f"Sent: {message.data}")
    except Exception as e:
        print(f"CAN Error: {e}")

def display_message(text):
    """Display message on SSD1306 OLED."""
    display.fill(0)
    display.text(text, 10, 30, 1)
    display.show()

def button_callback(channel):
    """Callback when a button is pressed."""
    button_index = BUTTON_PINS.index(channel) + 1  # Get button number (1-4)
    print(f"Button {button_index} Pressed")
    send_can_message(button_index)

def main():
    setup_gpio()

    # Add event detection for each button
    for pin in BUTTON_PINS:
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=200)

    print("Waiting for button press...")
    try:
        while True:
            time.sleep(0.1)  # Keep script running
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Exiting...")

if __name__ == "__main__":
    main()
