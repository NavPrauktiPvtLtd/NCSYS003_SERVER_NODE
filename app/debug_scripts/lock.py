import argparse
import RPi.GPIO as GPIO
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LockController:
    def __init__(self, relay_pin):
        self.RELAY_PIN = relay_pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)
        GPIO.output(self.RELAY_PIN, GPIO.LOW)

    def open(self):
        try:
            logger.debug("unlocked")
            GPIO.output(self.RELAY_PIN, GPIO.HIGH)
        except Exception as e:
            logger.error(f"Error unlocking: {e}")

    def close(self):
        try:
            logger.debug("locked")
            GPIO.output(self.RELAY_PIN, GPIO.LOW)
        except Exception as e:
            logger.error(f"Error locking: {e}")

def main():
    parser = argparse.ArgumentParser(description="Control a lock using a relay.")
    parser.add_argument("action", choices=["open", "close"], help="Specify the action to perform (open or close)")
    parser.add_argument("--pin", type=int, default=11, help="Specify the GPIO pin for the relay (default: 11)")

    args = parser.parse_args()

    lock_controller = LockController(args.pin)

    if args.action == "open":
        lock_controller.open()
    elif args.action == "close":
        lock_controller.close()
    else:
        print("Invalid action specified. Use 'open' or 'close'.")

if __name__ == "__main__":
    main()