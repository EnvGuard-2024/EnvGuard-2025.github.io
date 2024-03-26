import threading


class Weather():
    def __init__(self):
        super().__init__()
        self.value = ''

    def enable_change(self, value):
        if self.value == value:
            return 0
        else:
            return 1

    def ext_action_change(self, value):
        if self.enable_change(self, value):
            self.value = value
            
    def get(self):
        return self.value