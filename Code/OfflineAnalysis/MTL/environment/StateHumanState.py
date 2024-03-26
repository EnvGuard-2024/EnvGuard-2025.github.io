import threading


class HumanState():
    def __init__(self):
        super().__init__()
        self.value = 0

    def enable_decrease(self):
        if self.value == 0:
            return 0
        else:
            return 1

    def enable_increase(self):
        if self.value == 1:
            return 0
        else:
            return 1

    def ext_action_decrease(self, env):
        if self.enable_decrease(self):
            self.value = 0
            
    def ext_action_increase(self, env):
        if self.enable_increase(self):
            self.value = 1
            
    def get(self):
        return self.value