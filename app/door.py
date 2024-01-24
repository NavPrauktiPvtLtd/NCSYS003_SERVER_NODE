import RPi.GPIO as GPIO
import time
from logger.logger import setup_applevel_logger


logger = setup_applevel_logger(__name__)


OUTPUT_PIN = 3
INPUT_PIN = 4

class DoorController:
    def __init__(self,mqtt_client):
        self.OUTPUT_PIN = OUTPUT_PIN
        self.INPUT_PIN = INPUT_PIN
        self.mqtt_client = mqtt_client
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.OUTPUT_PIN, GPIO.OUT)
        GPIO.setup(self.INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def unlock_door(self):
        GPIO.output(self.OUTPUT_PIN, GPIO.LOW)

    def lock_door(self):
        GPIO.output(self.OUTPUT_PIN, GPIO.HIGH)

    def check_input_pin(self):
        return GPIO.input(self.INPUT_PIN) == GPIO.LOW

    def run(self):
        try:
            while True:
                self.lock_door()
                status = self.check_input_pin()

                if status:
                    print("Door locked")
                else:
                    self.unlock_door()
                    print("Unlocked")

                time.sleep(0.5)

        except KeyboardInterrupt as err:
            logger.error(err)
