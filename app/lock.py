import RPi.GPIO as GPIO
import time
from logger.logger import setup_applevel_logger


logger = setup_applevel_logger(__name__)

class LockController:
    def __init__(self):
        self.RELAY_PIN = 23
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


     