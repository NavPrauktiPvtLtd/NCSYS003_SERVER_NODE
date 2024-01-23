
from pynput.keyboard import Listener
from logger.logger import setup_applevel_logger
 
logger = setup_applevel_logger(__name__)



def show(key):
    print(key)

    



with Listener(on_press=show) as listener:
# with Listener(on_press = show) as listener: 
    listener.join()

    