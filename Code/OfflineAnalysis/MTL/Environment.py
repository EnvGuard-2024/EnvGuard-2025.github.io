from OfflineAnalysis.MTL.environment.device.AC import AC
from OfflineAnalysis.MTL.environment.device.AirPurifier import AirPurifier
from OfflineAnalysis.MTL.environment.device.Curtain import Curtain
from OfflineAnalysis.MTL.environment.device.Door import Door
from OfflineAnalysis.MTL.environment.device.Heater import Heater
from OfflineAnalysis.MTL.environment.device.Humidifier import Humidifier
from OfflineAnalysis.MTL.environment.device.MicrowaveOven import MicrowaveOven
from OfflineAnalysis.MTL.environment.device.TV import TV 
from OfflineAnalysis.MTL.environment.device.Light import Light
from OfflineAnalysis.MTL.environment.device.Printer import Printer
from OfflineAnalysis.MTL.environment.device.Speaker import Speaker
from OfflineAnalysis.MTL.environment.device.WaterDispenser import WaterDispenser
from OfflineAnalysis.MTL.environment.device.Window import Window
from OfflineAnalysis.MTL.environment.state.AirQuality import AirQuality
from OfflineAnalysis.MTL.environment.state.Brightness import Brightness
from OfflineAnalysis.MTL.environment.state.HumanState import HumanState
from OfflineAnalysis.MTL.environment.state.Humidity import Humidity
from OfflineAnalysis.MTL.environment.state.Noise import Noise
from OfflineAnalysis.MTL.environment.state.Temperature import Temperature
from OfflineAnalysis.MTL.environment.state.Weather import Weather

import imp
import os
import re

device_list = []
state_list = []
def get_dir(path,type):
    try:
        file_list = os.listdir(path)
    except:
        file_list = []
    if file_list:
        for file in file_list:
            file = os.path.join(path, file)
            if os.path.isdir(file):
                get_dir(file,type)
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

def getEnvonment():
    env = dict()
    space_dict = dict()

    # context
    device_dict = dict()
    env_state = dict()
    env_state["Temperature"] = Temperature()
    env_state["Humidity"] = Humidity()
    env_state["Brightness"] = Brightness()
    env_state["AirQuality"] = AirQuality()
    env_state["Weather"] = Weather()
    room_temp = dict()
    room_temp["device_dict"] = device_dict
    room_temp["env_state"] = env_state
    space_dict["Context"] = room_temp

    # Lab
    device_dict = dict()
    env_state = dict()
    env_state["Temperature"] = Temperature()
    env_state["Brightness"] = Brightness()
    env_state["Humidity"] = Humidity()
    env_state["Noise"] = Noise()
    env_state["AirQuality"] = AirQuality()
    env_state["HumanState"] = HumanState()

    device_dict["AC"] = AC()
    device_dict["Heater"] = Heater()
    device_dict["Door"] = Door()
    device_dict["Humidifier"] = Humidifier()
    device_dict["Light"] = Light()
    device_dict["Speaker"] = Speaker()
    device_dict["Printer"] = Printer()
    device_dict["Curtain"] = Curtain()
    device_dict["AirPurifier"] = AirPurifier()
    device_dict["Window"] = Window()
    room_temp = dict()
    room_temp["device_dict"] = device_dict
    room_temp["env_state"] = env_state
    space_dict["Lab"] = room_temp

    # MeetingRoomOne
    device_dict = dict()
    env_state = dict()
    env_state["Temperature"] = Temperature()
    env_state["Brightness"] = Brightness()
    env_state["Humidity"] = Humidity()
    env_state["Noise"] = Noise()
    env_state["AirQuality"] = AirQuality()
    env_state["HumanState"] = HumanState()

    device_dict["AC"] = AC()
    device_dict["TV"] = TV()
    device_dict["Door"] = Door()
    device_dict["Heater"] = Heater()
    device_dict["Humidifier"] = Humidifier()
    device_dict["Light"] = Light()
    device_dict["Speaker"] = Speaker()
    device_dict["Curtain"] = Curtain()
    device_dict["AirPurifier"] = AirPurifier()
    device_dict["Window"] = Window()
    room_temp = dict()
    room_temp["device_dict"] = device_dict
    room_temp["env_state"] = env_state
    space_dict["MeetingRoomOne"] = room_temp

    # MeetingRoomTwo
    device_dict = dict()
    env_state = dict()
    env_state["Temperature"] = Temperature()
    env_state["Brightness"] = Brightness()
    env_state["Humidity"] = Humidity()
    env_state["Noise"] = Noise()
    env_state["AirQuality"] = AirQuality()
    env_state["HumanState"] = HumanState()

    device_dict["AC"] = AC()
    device_dict["TV"] = TV()
    device_dict["Door"] = Door()
    device_dict["Door"] = Door()
    device_dict["Heater"] = Heater()
    device_dict["Humidifier"] = Humidifier()
    device_dict["Light"] = Light()
    device_dict["Speaker"] = Speaker()
    device_dict["Curtain"] = Curtain()
    device_dict["AirPurifier"] = AirPurifier()
    device_dict["Window"] = Window()
    room_temp = dict()
    room_temp["device_dict"] = device_dict
    room_temp["env_state"] = env_state
    space_dict["MeetingRoomTwo"] = room_temp

    # TeaRoom
    device_dict = dict()
    env_state = dict()
    env_state["Temperature"] = Temperature()
    env_state["Brightness"] = Brightness()
    env_state["Humidity"] = Humidity()
    env_state["Noise"] = Noise()
    env_state["AirQuality"] = AirQuality()
    env_state["HumanState"] = HumanState()

    # device_dict["AC"] = AC()
    device_dict["WaterDispenser"] = WaterDispenser()
    device_dict["MicrowaveOven"] = MicrowaveOven()
    device_dict["Door"] = Door()
    # device_dict["Heater"] = Heater()
    device_dict["Humidifier"] = Humidifier()
    device_dict["Light"] = Light()
    # device_dict["Speaker"] = Speaker()
    device_dict["Curtain"] = Curtain()
    device_dict["AirPurifier"] = AirPurifier()
    device_dict["Window"] = Window()
    room_temp = dict()
    room_temp["device_dict"] = device_dict
    room_temp["env_state"] = env_state
    space_dict["TeaRoom"] = room_temp

    # Corridor 
    device_dict = dict()
    env_state = dict()
    env_state["Temperature"] = Temperature()
    env_state["Brightness"] = Brightness()
    env_state["Humidity"] = Humidity()
    env_state["Noise"] = Noise()
    env_state["AirQuality"] = AirQuality()
    env_state["HumanState"] = HumanState()

    device_dict["Light"] = Light()
    device_dict["Speaker"] = Speaker()
    device_dict["Door"] = Door()
    room_temp = dict()
    room_temp["device_dict"] = device_dict
    room_temp["env_state"] = env_state
    space_dict["Corridor"] = room_temp

    env["space_dict"] = space_dict
    return env

env = getEnvonment()
path = "device"
get_dir(path, 'device')
path = "state"
get_dir(path, 'state')
# print(device_list)
# print(state_list)

def getEnv():
    return env

def setEnv(e):
    global env
    env = e