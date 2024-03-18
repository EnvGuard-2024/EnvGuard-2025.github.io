import threading


class Speaker():
    def __init__(self):
        super().__init__()
        self.on = 0
        
    def enable_on(self):
        if self.on == 1:
            return 0
        else:
            return 1

    def action_on(self):
        if self.enable_on(self):
            self.on = 1

    def enable_off(self):
        if self.on == 0:
            return 0
        else:
            return 1

    def action_off(self):
        if self.enable_off(self):
            self.on = 0
    def get(self):
        return self.on