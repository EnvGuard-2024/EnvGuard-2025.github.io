from MetaType import BaseType

class Weather(BaseType):
    raining = 0
    sunny = 1
    snowing = 0
    cloudy = 0

    def __init__(self, room):
        super().__init__()
        self.room = room
                                                                                               
    def _only_one(*nums):
        count = 0
        for num in nums:
            count += num & 1  # 判断最低位是否为1
            if count > 1:
                return False
        return count == 1

    def enable_raining(self):
        assert self._only_one(self.raining,self.sunny,self.snowing,self.cloudy)
        if self.raining == 1:
            return 0
        else:
            return 1
    
    def enable_sunny(self):
        assert self._only_one(self.raining,self.sunny,self.snowing,self.cloudy)
        if self.sunny == 1:
            return 0
        else:
            return 1
    
    def enable_snowing(self):
        assert self._only_one(self.raining,self.sunny,self.snowing,self.cloudy)
        if self.snowing == 1:
            return 0
        else:
            return 1

    def enable_cloudy(self):
        assert self._only_one(self.raining,self.sunny,self.snowing,self.cloudy)
        if self.cloudy == 1:
            return 0
        else:
            return 1

    def ext_action_raining(self,env):
        assert self._only_one(self.raining,self.sunny,self.snowing,self.cloudy)
        if self.enable_raining(self):
          self.raining = 1
          self.sunny = 0
          self.snowing = 0
          self.cloudy = 0


    def ext_action_sunny(self,env):
        assert self._only_one(self.raining,self.sunny,self.snowing,self.cloudy)
        if self.enable_sunny(self):
          self.raining = 0
          self.sunny = 1
          self.snowing = 0
          self.cloudy = 0
    
    def ext_action_snowing(self,env):
        assert self._only_one(self.raining,self.sunny,self.snowing,self.cloudy)
        if self.enable_snowing(self):
          self.raining = 0
          self.sunny = 0
          self.snowing = 1
          self.cloudy = 0

    def ext_action_cloudy(self,env):
        assert self._only_one(self.raining,self.sunny,self.snowing,self.cloudy)
        if self.enable_cloudy(self):
          self.raining = 0
          self.sunny = 0
          self.snowing = 0
          self.cloudy = 1

    def ap_raining(self):
        return self.raining
        
    def ap_sunny(self):
        return self.sunny

    def ap_snowing(self):
        return self.snowing
    
    def ap_cloudy(self):
        return self.cloudy