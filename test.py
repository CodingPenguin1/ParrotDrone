# This thing makes the drone jump up to 1 meter, spin for a bit, then land

import time
from Drone import Drone


if __name__ == '__main__':
    drone = Drone()
    print('takeoff')
    drone.takeoff()

    print('rotating')
    t0 = time.time()
    while time.time() - t0 < 10:
        drone.move(cw=0.5)

    print('landing')
    drone.land()

    print('mission accomplished')
