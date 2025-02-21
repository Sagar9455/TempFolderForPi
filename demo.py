import RPi.GPIO as GPIO
import time

BUTTON_PINS = [12, 16, 20, 21]

GPIO.setmode(GPIO.BCM)
for pin in BUTTON_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press a button...")

try:
    while True:
        for pin in BUTTON_PINS:
            if GPIO.input(pin) == GPIO.LOW:
                print(f"Button on GPIO {pin} pressed!")
                time.sleep(0.2)  # Debounce
except KeyboardInterrupt:
    GPIO.cleanup()
