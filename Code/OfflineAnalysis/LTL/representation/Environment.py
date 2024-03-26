import requests
import re
import os
import imp
from State import State
from StateHumanSate import HumanState
from StateWeather import Weather
from Device import Device

device_list = []
state_list = []

def toSnake(strings):
  lst = []
  for i,v in enumerate(strings):
    if v.isupper() and i != 0:
      if strings[i+1:i+2] and not strings[i+1:i+2].isupper():
        lst.append("_")
    lst.append(v)
  return "".join(lst).lower()

def get_dict(space_name, space):
    temp = dict()
    temp["action_dict"] = dict()
    temp["enable_dict"] = dict()
    temp["ap_dict"] = dict()
    temp["state_dict"] = dict()
    temp["ext_action_list"] = list()
    for key, value in sorted(space["device_dict"].items()):
        for k, v in value.action_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["action_dict"][name] = v
        for k, v in value.enable_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["enable_dict"][name] = v
        for k, v in sorted(value.ap_dict.items()):
            name = space_name + '.' + key + '.' + k
            temp["ap_dict"][name] = v
        for k, v in value.state_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["state_dict"][name] = v
        for item in value.ext_action_list:
            temp["ext_action_list"].append(space_name + '.' + key + '.' + item)
    for key, value in sorted(space["env_state"].items()):
        for k, v in value.action_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["action_dict"][name] = v
        for k, v in value.enable_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["enable_dict"][name] = v
        for k, v in sorted(value.ap_dict.items()):
            name = space_name + '.' + key + '.' + k
            temp["ap_dict"][name] = v
        for k, v in value.state_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["state_dict"][name] = v
        for item in value.ext_action_list:
            temp["ext_action_list"].append(space_name + '.' + key + '.' + item)
    return temp

def get_type():
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
        

def setEnvironment(ltl):
    env = dict()
    space_dict = dict()

    pattern = r'\b[a-zA-Z]+\.[a-zA-Z]+\.[a-zA-Z]+\b'
    matches = re.findall(pattern, ltl)
    stack = list()
    for item in matches:
        temp = item.split('.')[0] + "." + item.split('.')[1]
        if temp not in stack:
            stack.append(temp)
            if item.split('.')[1] in state_list:
                url = "http://47.101.169.122:5002/effect_node/" + item.split('.')[0] + "/effect_" + toSnake(item.split('.')[1]) + "_up"
                effect_list = requests.get(url).json()
                for effect in effect_list:
                    temp_state = effect["room"] + '.' + effect["device"][:-3]
                    if temp_state not in stack:
                        stack.append(temp_state)
    while stack:
        item = stack.pop()
        room = item.split('.')[0]
        deviceOrState = item.split('.')[1]
        if room not in space_dict:
            space_dict[room] = dict()
            space_dict[room]["device_dict"] = dict()
            space_dict[room]["env_state"] = dict()
        if deviceOrState in device_list and deviceOrState not in space_dict[room]["device_dict"]:
            space_dict[room]["device_dict"][deviceOrState] = Device(room, deviceOrState)
            
            url = "http://47.101.169.122:5002/action_list_by_device/" + room + "/" + deviceOrState + "001"
            action_list = requests.get(url).json()
            for act in action_list:
                url = "http://47.101.169.122:5002/effect_and_pre/" + room + "/" + deviceOrState + "001/" + act
                effect_list = requests.get(url).json()
                for effect in effect_list:
                    effect_temp = effect.split('.')[0] + "." + effect.split('.')[1]
                    if effect_temp not in stack:
                        stack.append(effect_temp)
                    pattern = r'\b[a-zA-Z]+\.[a-zA-Z]+\b'
                    preCondition_state_list = re.findall(pattern, effect_list[effect])
                    for preCondition in preCondition_state_list:
                        if preCondition not in stack:
                            stack.append(preCondition)
        elif deviceOrState in state_list and deviceOrState not in space_dict[room]["env_state"]:
            if deviceOrState == "HumanState":
                space_dict[room]["env_state"][deviceOrState] = HumanState(room)
            elif deviceOrState == "Weather":
                space_dict[room]["env_state"][deviceOrState] = Weather(room)
            else:
                space_dict[room]["env_state"][deviceOrState] = State(room)
                    
    for room in space_dict:
        temp = get_dict(room, space_dict[room])
        space_dict[room]["action_dict"] = temp["action_dict"]
        space_dict[room]["enable_dict"] = temp["enable_dict"]
        space_dict[room]["ap_dict"] = temp["ap_dict"]
        space_dict[room]["state_dict"] = temp["state_dict"]
        space_dict[room]["ext_action_list"] = temp["ext_action_list"]   

    env["space_dict"] = space_dict
    global environment
    environment = env

def getEnvironment():
    return environment

get_type()  

environment = dict()
