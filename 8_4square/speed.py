from maestro import Controller
import time

if "__name__" == "__main__":
    tango = Controller()
    tango.setTarget(1, 5800)
    tango.setTarget(0, 6600)
    time.sleep(1)
    tango.setTarget(1, 6000)
    tango.setTarget(0, 6000)

