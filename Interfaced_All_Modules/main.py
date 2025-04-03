import time
import RPi.GPIO as GPIO
from can_utils import CANHandler
from oled_utils import display_text

# GPIO Setup
GPIO.setmode(GPIO.BCM)
buttons = [12, 16, 20, 21]
for btn in buttons:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

can_handler=CANHandler(display_callback=display_text)
# Welcome Message
display_text("Welcome to CAN Demo")
time.sleep(1.5)

# Start CAN receiving and responding in a separate thread
can_handler.start_rx_thread()

# Main loop for button input
try:
    while True:
        
        display_text("Press a Button to Send:\n1. 0x123\n2. 0x456\n3. 0x789\n4. 0x111", y=0)

        while True:
            for i, btn in enumerate(buttons, start=1):
                if GPIO.input(btn) == GPIO.LOW:  # Button pressed
                    can_handler.CAN_Send(btn)  # Send CAN message
                    
                   

except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()
