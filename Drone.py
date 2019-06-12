from time import sleep
from pyardrone import ARDrone, at, video
import pyardrone


class Drone(ARDrone):
    def __init__(self):
        super().__init__()
        super().navdata_ready.wait()
        super().send(at.CONFIG('general:navdata_demo', True))
        sleep(1)
        self.navData = super().navdata.demo
        self.video_ready.wait()

    def takeoff(self):
        print('Taking off')
        while not self.state.fly_mask:
            super().takeoff()
        sleep(5)

    def land(self):
        print('Landing')
        while self.state.fly_mask:
            super().land()

    def getNavData(self):
        self.navData = super().navdata.demo
        return self.navData

    def isFlying(self):
        return self.state.fly_mask
