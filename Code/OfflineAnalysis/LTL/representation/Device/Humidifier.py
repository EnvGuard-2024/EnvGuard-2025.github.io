from representation.Device.MetaType import BaseType
import requests

class Humidifier(BaseType):
    on = 0
    def __init__(self,room):
        super().__init__()
        self.room = room

    def enable_on(self):
        if self.on == 1:
            return 0
        else:
            return 1

    def action_on(self,env):
        if self.enable_on(self):
            url = "http://47.101.169.122:5002/effect_and_pre/" + self.room + "/Humidifier001/action_on"
            effect_and_pre = requests.get(url).json()
            for effect in effect_and_pre:
                temp_list = effect.split('.')
                if effect_and_pre[effect] == '':
                    # 获得action
                    state = env[temp_list[0]]["env_state"][temp_list[1]]
                    func = getattr(state, temp_list[2], None)
                    func(state,env)
                else:
                    pre_condition_list = effect_and_pre[effect].split(' ')
                    if len(pre_condition_list) == 3:
                        temp_one_list = pre_condition_list[0].split('.')
                        temp_two_list = pre_condition_list[2].split('.')
                        state_one = env[temp_one_list[0]]["env_state"][temp_one_list[1]]
                        state_two = env[temp_two_list[0]]["env_state"][temp_two_list[1]]
                        if pre_condition_list[1] == '<':
                            if (state_two.ap_high(state_two) == 1 and state_one.ap_high(state_one) == 0) or (state_two.ap_middle(state_two) == 1 and state_one.ap_low(state_one) == 1):
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)
                        elif pre_condition_list[1] == '>':
                            if (state_one.ap_high(state_one) == 1 and state_two.ap_high(state_two) == 0) or (state_one.ap_middle(state_one) == 1 and state_two.ap_low(state_two) == 1):
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)
                    elif len(pre_condition_list) == 5:
                        temp_one_list = pre_condition_list[0].split('.')
                        temp_two_list = pre_condition_list[2].split('.')
                        state_one = env[temp_one_list[0]]["env_state"][temp_one_list[1]]
                        state_two = env[temp_two_list[0]]["env_state"][temp_two_list[1]]
                        if pre_condition_list[4] == '2':
                            if state_one.ap_high(state_one) == 1 and state_two.ap_low(state_two) == 1:
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)
                        elif pre_condition_list[4] == '-2':
                            if state_one.ap_low(state_one) == 1 and state_two.ap_high(state_two) == 1:
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)
                    elif len(pre_condition_list) == 7 and ("&&" in pre_condition_list):
                        temp_one_list = pre_condition_list[0].split('.')
                        temp_two_list = pre_condition_list[2].split('.')
                        temp_three_list = pre_condition_list[4].split('.')
                        value = int(pre_condition_list[6])
                        state_one = env[temp_one_list[0]]["env_state"][temp_one_list[1]]
                        state_two = env[temp_two_list[0]]["env_state"][temp_two_list[1]]
                        device = env[temp_three_list[0]]["device_dict"][temp_three_list[1]]
                        if pre_condition_list[1] == '<':
                            if (state_two.ap_high(state_two) == 1 and state_one.ap_high(state_one) == 0 and device.ap_on(device) == value) or (state_two.ap_middle(state_two) == 1 and state_one.ap_low(state_one) == 1 and device.ap_on(device) == value):
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)
                        elif pre_condition_list[1] == '>':
                            if (state_one.ap_high(state_one) == 1 and state_two.ap_high(state_two) == 0 and device.ap_on(device) == value) or (state_one.ap_middle(state_one) == 1 and state_two.ap_low(state_two) == 1 and device.ap_on(device) == value):
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)

            self.on = 1

    def enable_off(self):
        if self.on == 0:
            return 0
        else:
            return 1

    def action_off(self,env):
        if self.enable_off(self):
            url = "http://47.101.169.122:5002/effect_and_pre/" + self.room + "/Humidifier001/action_off"
            effect_and_pre = requests.get(url).json()
            for effect in effect_and_pre:
                temp_list = effect.split('.')
                if effect_and_pre[effect] == '':
                    # 获得action
                    state = env[temp_list[0]]["env_state"][temp_list[1]]
                    func = getattr(state, temp_list[2], None)
                    func(state,env)
                else:
                    pre_condition_list = effect_and_pre[effect].split(' ')
                    if len(pre_condition_list) == 3:
                        temp_one_list = pre_condition_list[0].split('.')
                        temp_two_list = pre_condition_list[2].split('.')
                        state_one = env[temp_one_list[0]]["env_state"][temp_one_list[1]]
                        state_two = env[temp_two_list[0]]["env_state"][temp_two_list[1]]
                        if pre_condition_list[1] == '<':
                            if (state_two.ap_high(state_two) == 1 and state_one.ap_high(state_one) == 0) or (state_two.ap_middle(state_two) == 1 and state_one.ap_low(state_one) == 1):
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)
                        elif pre_condition_list[1] == '>':
                            if (state_one.ap_high(state_one) == 1 and state_two.ap_high(state_two) == 0) or (state_one.ap_middle(state_one) == 1 and state_two.ap_low(state_two) == 1):
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)
                    elif len(pre_condition_list) == 5:
                        temp_one_list = pre_condition_list[0].split('.')
                        temp_two_list = pre_condition_list[2].split('.')
                        state_one = env[temp_one_list[0]]["env_state"][temp_one_list[1]]
                        state_two = env[temp_two_list[0]]["env_state"][temp_two_list[1]]
                        if pre_condition_list[4] == '2':
                            if state_one.ap_high(state_one) == 1 and state_two.ap_low(state_two) == 1:
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)
                        elif pre_condition_list[4] == '-2':
                            if state_one.ap_low(state_one) == 1 and state_two.ap_high(state_two) == 1:
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)
                    elif len(pre_condition_list) == 7 and ("&&" in pre_condition_list):
                        temp_one_list = pre_condition_list[0].split('.')
                        temp_two_list = pre_condition_list[2].split('.')
                        temp_three_list = pre_condition_list[4].split('.')
                        value = int(pre_condition_list[6])
                        state_one = env[temp_one_list[0]]["env_state"][temp_one_list[1]]
                        state_two = env[temp_two_list[0]]["env_state"][temp_two_list[1]]
                        device = env[temp_three_list[0]]["device_dict"][temp_three_list[1]]
                        if pre_condition_list[1] == '<':
                            if (state_two.ap_high(state_two) == 1 and state_one.ap_high(state_one) == 0 and device.ap_on(device) == value) or (state_two.ap_middle(state_two) == 1 and state_one.ap_low(state_one) == 1 and device.ap_on(device) == value):
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)
                        elif pre_condition_list[1] == '>':
                            if (state_one.ap_high(state_one) == 1 and state_two.ap_high(state_two) == 0 and device.ap_on(device) == value) or (state_one.ap_middle(state_one) == 1 and state_two.ap_low(state_two) == 1 and device.ap_on(device) == value):
                                state = env[temp_list[0]]["env_state"][temp_list[1]]
                                func = getattr(state, temp_list[2], None)
                                func(state,env)


            self.on = 0

    def ap_on(self):
        return self.on
