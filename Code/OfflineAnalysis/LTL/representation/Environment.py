import requests
from representation.Device.MetaType import BaseType
from representation.Device.AC import AC
from representation.Device.Curtain import Curtain
from representation.Device.Door import Door
from representation.Device.Heater import Heater
from representation.Device.Humidifier import Humidifier
from representation.Device.Light import Light
from representation.Device.MicrowaveOven import MicrowaveOven
from representation.Device.Printer import Printer
from representation.Device.AirPurifier import AirPurifier
from representation.Device.Speaker import Speaker
from representation.Device.TV import TV
from representation.Device.WaterDispenser import WaterDispenser
from representation.Device.Window import Window
from representation.state.Brightness import Brightness
from representation.state.HumanState import HumanState
from representation.state.AirQuality import AirQuality
from representation.state.Humidity import Humidity
from representation.state.Noise import Noise
from representation.state.Weather import Weather
from representation.state.Temperature import Temperature
import re
import os
import imp

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

def get_type(path,type):
    try:
        file_list = os.listdir(path)
    except:
        file_list = []
    if file_list:
        for file in file_list:
            file = os.path.join(path, file)
            if os.path.isdir(file):
                get_type(file,type)
            else:
                if file.endswith(".py"):
                    with open(file, encoding="utf-8") as f:
                        for line in f.readlines():
                            cls_match = re.match(r"class\s(.*?)[\(:]", line)
                            if cls_match:
                                cls_name = cls_match.group(1)
                                try:
                                    module = imp.load_source('mycl', file)
                                    cls_a = getattr(module, cls_name)
                                    if cls_a:
                                        if type == 'device':
                                            device_list.append(cls_name)
                                        else:
                                            state_list.append(cls_name)
                                except:
                                    pass

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
            space_dict[room]["device_dict"][deviceOrState] = globals()[deviceOrState](room)  
            
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
            space_dict[room]["env_state"][deviceOrState] = globals()[deviceOrState](room)
                    
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

path = "./representation/Device"
get_type(path, 'device')
path = "./representation/state"
get_type(path, 'state')   

environment = dict()
