import RPi.GPIO as GPIO
import time
from can_utils import CANHandler
from oled_utils import DisplayHandler

# GPIO Setup
GPIO.setmode(GPIO.BCM)
buttons = [12, 16, 20, 21]
for btn in buttons:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize OLED and CAN handler
display_handler = DisplayHandler()
can_handler = CANHandler(display_handler.display_text)
can_handler.setup_can_interface()

# Display welcome message
display_handler.display_text("Welcome to CAN Demo")
time.sleep(1.5)

# Start CAN reception in a separate thread
can_handler.start_rx_thread()

# Main loop for button input
try:
    while True:
        display_handler.display_text("Press a Button to Send:\n1. 0x123\n2. 0x456\n3. 0x789\n4. 0x111", y=0)

        while True:
            for i, btn in enumerate(buttons, start=1):
                if GPIO.input(btn) == GPIO.LOW:
                    can_handler.send_can_message(btn)
                    time.sleep(0.5)  # Debounce delay

except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()  # Cleanup GPIO on exit