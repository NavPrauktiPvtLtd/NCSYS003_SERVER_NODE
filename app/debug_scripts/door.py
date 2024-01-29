import RPi.GPIO as GPIO
import time

output = 5
input_pin = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(output, GPIO.OUT)
GPIO.output(output, GPIO.HIGH)
time.sleep(1)

GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def check_input_pin():

    return GPIO.input(input_pin)


try:
    while True:
        status=check_input_pin()
        print(status)
        if(status):
            print("door_locked")
        else:
            print("unlocked")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("stopped")
finally:
    GPIO.cleanup()

check_input_pin()