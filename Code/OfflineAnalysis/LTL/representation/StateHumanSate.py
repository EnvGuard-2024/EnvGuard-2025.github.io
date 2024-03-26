
from MetaType import BaseType
import requests

class HumanState(BaseType):
    detected = 0

    def __init__(self, room):
        super().__init__()
        self.room = room

    def enable_increase(self):
        if self.detected == 1:
            return 0
        else:
            return 1

    def ext_action_increase(self,env):
        if self.enable_increase(self):
            self.detected = 1

    def enable_decrease(self):
        if self.detected == 0:
            return 0
        else:
            return 1

    def ext_action_decrease(self,env):
        if self.enable_decrease(self):
            self.detected = 0

    def ap_detected(self):
        return self.detected
