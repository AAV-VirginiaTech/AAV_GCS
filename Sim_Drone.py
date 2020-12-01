#Simple simulated drone initiation.
#Note Dronekit simulation launches ArduCopter 3.3 for testing - which is a very old version. Since we only use this to test interop operations - the firmware version doesn't matter for now.
#However, if there were to a large overhaul to the platform in the future (in terms of comms) - a different method of simulation may be required.

import dronekit_sitl
from time import sleep

if __name__ == '__main__':
    sitl = dronekit_sitl.start_default(lat=38.145206, lon=-76.428473)
    print("Connection String:", sitl.connection_string())

    try:
        while True:
            sleep(1)
    except:
        sitl.stop()
