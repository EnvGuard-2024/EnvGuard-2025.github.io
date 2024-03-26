import imp
import os
import re
from sre_parse import State
import requests

from environment.Device import Device
from environment.StateHumanState import HumanState
from environment.StateWeather import Weather

device_list = []
state_list = []
def get_dir():
    url = "http://47.101.169.122:5002/room_list"
    room_list = requests.get(url).json()
    for room in room_list:
        url = "http://47.101.169.122:5002/room_device/" + room
        devices = requests.get(url).json()
        for device in devices:
            if device[:-3] not in device_list:
                device_list.append(device[:-3])
        
        url = "http://47.101.169.122:5002/room_state/" + room
        states = requests.get(url).json()
        for state in states:
            if state not in state_list:
                state_list.append(state)

def getEnvonment():
    ip = "http://47.101.169.122:5002"
    env = dict()
    space_dict = dict()
    url = ip + "/room_list"
    room_list = requests.get(url).json()
    for room in room_list:
        device_dict = dict()
        env_state = dict()
        
        url = ip + "/room_state/" + room
        room_state = requests.get(url).json()

        for state in room_state:
            if state == "HumanState":
                env_state[state] = HumanState()
            elif state == "Weather":
                env_state[state] = Weather()
            else:
                env_state[state] = State()

        url = ip + "/room_device/" + room
        room_device = requests.get(url).json()

        for device in room_device:
            device_dict[device[:-3]] = Device()

        room_temp = dict()
        room_temp["device_dict"] = device_dict
        room_temp["env_state"] = env_state
        space_dict[room] = room_temp

    env["space_dict"] = space_dict
    return env

env = getEnvonment()
get_dir()
# print(device_list)
# print(state_list)

def getEnv():
    return env

def setEnv(e):
    global env
    env = e

print(env)