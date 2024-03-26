import requests
import os,sys,re
from Environment import env,device_list,state_list

time_template = {
    "trigger":"",
    "time":"",
    "condition":"",
    "fix":""
}

MTL = [
  "G(Lab.humidity_up -> (F[0, 60*60] !Lab.humidity_up))",
  "G(TeaRoom.humdity_up -> (F[0, 60*60] !TeaRoom.humidity_up))",
  "G(MeetingRoomOine.humidity_up -> (F[0, 60*60] !MeetingRoomOne.humidity_up))",
  "G(MeetingRoomTwo.humidity_up -> (F[0, 60*60] !MeetingRoomTwo.humidity_up))",
  "G(Corridor.humidity_up -> (F[0, 60*60] !Corridor.humidity_up))",
  
  "G((Lab.AirQuality.low & Lab.HumanState.detected) -> (F[0, 10*60] Lab.air_quality_up))",
  "G((TeaRoom.AirQuality.low & TeaRoom.HumanState.detected) -> (F[0, 10*60] TeaRoom.air_quality_up))",
  "G((MeetingRoomOne.AirQuality.low & MeetingRoomOne.HumanState.detected) -> (F[0, 10*60] MeetingRoomOne.air_quality_up))",
  "G((MeetingRoomTwo.AirQuality.low & MeetingRoomTwo.HumanState.detected) -> (F[0, 10*60] MeetingRoomTwo.air_quality_up))",
  "G((Corridor.AirQuality.low & Corridor.HumanState.detected) -> (F[0, 10*60] Corridor.air_quality_up))",
  
  
  "G(MeetingRoomOne.human_undetected -> (F[0, 30] MeetingRoomOne.Light.off))",
  "G(MeetingRoomTwo.human_undetected -> (F[0, 30] MeetingRoomTwo.Light.off))",
  
  
  "G((TeaRoom.WaterDispenser.on) -> (F[0, 2*60] !(TeaRoom.WaterDispenser.on)))",
  
  "G((Lab.Speaker.on) -> (F[0, 1*60] !(Lab.Speaker.on)))",    
  "G((Corridor.Speaker.on) -> (F[0, 1*60] !(Corridor.Speaker.on)))",    
  
]

def change(string):
  string_list = []
  iter = re.finditer(r'[a-zA-Z.!]+', string)
  for i in iter:
    value = i.group()
    if len(value.split('.')) == 2:
      return
    temp_value = value
    if '!' in value:
      symbol = '!='
    else:
      symbol = '=='
    if '!' in value:
      temp_value = value[1:]
    temp_list = temp_value.split('.')
    if temp_list[1] in device_list: 
      if temp_list[2] == 'on':
        end = 1
      else:
        end = 0
      temp = "env['space_dict']['" + temp_list[0] + "']['device_dict']['" + temp_list[1] + "'].get() "  + symbol + str(end)
    else:
      if temp_list[1] not in ['HumanState','Weather']: 
        if temp_list[2] == 'low':
          end = -1
        elif temp_list[2] == 'middle':
          end = 0
        else:
          end = 1
      elif temp_list[1] == 'HumanState':
        if temp_list[2] == 'detected':
          end = 1
        else:
          end = 0
      else:
        end = "'" + temp_list[2] + "'"
      temp = "env['space_dict']['" + temp_list[0] + "']['env_state']['" + temp_list[1] + "'].get() " +  symbol  + str(end)
    string_list.append([value,temp])
  return string_list

def getEffectList(list):
  result_list = []
  url = "http://47.101.169.122:5002/effect_node/" + list[0]+ '/effect_' + list[1]
  results = requests.get(url).json()
  for result in results:
    ltl_action = ''
    action_item = result['room'] + '.' + result['device'][0:len(result['device']) - 3] + '.' + result['action'][7:len(result['action'])]
    ltl_action = action_item
    pre_condition_item = getPreCondition(result['pre_condition'])
    if pre_condition_item != '':
      ltl_action = ltl_action + ' & ' + '(' + pre_condition_item + ')'
    result_list.append('(' + ltl_action + ')')
  return result_list

def getPreCondition(preCondition):
    ltl = ''
    if preCondition != '':
        pre_condition_list = preCondition.split(' ')
        if len(pre_condition_list) == 3:
            temp_one_list = ''
            temp_two_list = ''
            if pre_condition_list[1] == '>':
                temp_one_list = pre_condition_list[0]
                temp_two_list = pre_condition_list[2]
            elif pre_condition_list[1] == '<':
                temp_one_list = pre_condition_list[2]
                temp_two_list = pre_condition_list[0]
            ltl = f'({temp_one_list}.high & {temp_two_list}.middle) | ' \
                  f'({temp_one_list}.high & {temp_two_list}.low) | ' \
                  f'({temp_one_list}.middle & {temp_two_list}.low)'
        elif len(pre_condition_list) == 5:
            temp_one_list = pre_condition_list[0]
            temp_two_list = pre_condition_list[2]
            if pre_condition_list[4] == '2':
                ltl = f'{temp_one_list}.high & {temp_two_list}.low'
            elif pre_condition_list[4] == '-2':
                ltl = f'{temp_one_list}.low & {temp_two_list}.high'
        elif len(pre_condition_list) == 7 and '&&' in pre_condition_list:
            temp_one_list = ''
            temp_two_list = ''
            if pre_condition_list[1] == '>':
                temp_one_list = pre_condition_list[0]
                temp_two_list = pre_condition_list[2]
            elif pre_condition_list[1] == '<':
                temp_one_list = pre_condition_list[2]
                temp_two_list = pre_condition_list[0]
            ltl = f'(({temp_one_list}.high & {temp_two_list}.middle) | ' \
                  f'({temp_one_list}.high & {temp_two_list}.low) | ' \
                  f'({temp_one_list}.middle & {temp_two_list}.low))'
            if pre_condition_list[6] == '0':
                ltl = ltl + f' & {pre_condition_list[4]}.off'
            elif pre_condition_list[6] == '1':
                ltl = ltl + f' & {pre_condition_list[4]}.on'
        elif len(pre_condition_list) == 11 and '&&' in pre_condition_list:
            temp_one_list = ''
            temp_two_list = ''
            if pre_condition_list[1] == '>':
                temp_one_list = pre_condition_list[0]
                temp_two_list = pre_condition_list[2]
            elif pre_condition_list[1] == '<':
                temp_one_list = pre_condition_list[2]
                temp_two_list = pre_condition_list[0]
            ltl = f'(({temp_one_list}.high & {temp_two_list}.middle) | ' \
                  f'({temp_one_list}.high & {temp_two_list}.low) | ' \
                  f'({temp_one_list}.middle & {temp_two_list}.low))'
            if pre_condition_list[6] == '0':
                ltl = ltl + f' & {pre_condition_list[4]}.off'
            elif pre_condition_list[6] == '1':
                ltl = ltl + f' & {pre_condition_list[4]}.on'
            if pre_condition_list[10] == '0':
                ltl = ltl + f' & {pre_condition_list[8]}.off'
            elif pre_condition_list[10] == '1':
                ltl = ltl + f' & {pre_condition_list[8]}.on'
    return ltl

def toSnake(strings):
  lst = []
  for i,v in enumerate(strings):
    if v.isupper() and i != 0:
      if strings[i+1:i+2] and not strings[i+1:i+2].isupper():
        lst.append("_")
    lst.append(v)
  return "".join(lst).lower()

def getActionPre(list):
  result_list = []
  url = "http://47.101.169.122:5002/effect_node/" + list[0]+ '/effect_' + list[1]
  results = requests.get(url).json()
  for result in results:
    ltl_action = ''
    action_item = result['room'] + '.' + result['device'][0:len(result['device']) - 3] + '.' + result['action'][7:len(result['action'])]
    ltl_action = action_item
    pre_condition_item = getPreCondition(result['pre_condition'])
    result_list.append([ltl_action, pre_condition_item])
  return result_list
   
def getFix(state,flag):
  fix = []
  state_temp = state.split('.')
  room = state_temp[0]
  type = state_temp[1]
  value = state_temp[2]
  pre_value = ''
  match value:
    case 'on':
      pre_value = '1'
    case 'off':
      pre_value = '0'
    case 'high':
      pre_value = '1'
    case 'middle':
      pre_value = '0'
    case 'low':
      pre_value = '-1'
  if not flag:
    if type in device_list:
      if value == 'on':
        fix.append([room + '.' + type + '.' + 'action_off',""])
      else:
        fix.append([room + '.' + type + '.' + 'action_on',""])
    else:
      if room != 'Context' and type != 'HumanState':
        if value == 'high':
          action_list = getActionPre([room, type.lower() + '_down'])
          for action_item in action_list:
            action_temp = action_item[0].split('.')
            action = action_temp[0] + '.' + action_temp[1] + '.'  + 'action_' + action_temp[2]
            pre = action_item[1]
            pre_list = change(pre)
            for i in pre_list:
              pre = pre.replace(i[0],i[1],1)
            if action_temp[2] == 'on':
              v = '0'
            else:
              v = '1'
            if pre:
              pre = '(' + pre + ')' + ' and ' + '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            else:
              pre = '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            pre = pre.replace('&', ' and ')
            pre = pre.replace('|', ' or ')
            action_item[0] = action
            action_item[1] = pre
            fix.append(action_item)
        elif value == 'middle':
          action_list = getActionPre([room, type.lower() + '_down'])
          for action_item in action_list:
            action_temp = action_item[0].split('.')
            action = action_temp[0] + '.' + action_temp[1] + '.'  + 'action_' + action_temp[2]
            pre = action_item[1]
            pre_list = change(pre)
            for i in pre_list:
              pre = pre.replace(i[0],i[1],1)
            if action_temp[2] == 'on':
              v = '0'
            else:
              v = '1'
            if pre:
              pre = '(' + pre + ')' + ' and ' + '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            else:
              pre = '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            pre = pre.replace('&', ' and ')
            pre = pre.replace('|', ' or ')
            action_item[0] = action
            action_item[1] = pre
            fix.append(action_item)
          action_list = getActionPre([room, type.lower() + '_up'])
          for action_item in action_list:
            action_temp = action_item[0].split('.')
            action = action_temp[0] + '.' + action_temp[1] + '.'  + 'action_' + action_temp[2]
            pre = action_item[1]
            pre_list = change(pre)
            for i in pre_list:
              pre = pre.replace(i[0],i[1],1)
            if action_temp[2] == 'on':
              v = '0'
            else:
              v = '1'
            if pre:
              pre = '(' + pre + ')' + ' and ' + '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            else:
              pre = '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            pre = pre.replace('&', ' and ')
            pre = pre.replace('|', ' or ')
            action_item[0] = action
            action_item[1] = pre
            fix.append(action_item)
        else:
          action_list = getActionPre([room, type.lower() + '_up'])
          for action_item in action_list:
            action_temp = action_item[0].split('.')
            action = action_temp[0] + '.' + action_temp[1] + '.'  + 'action_' + action_temp[2]
            pre = action_item[1]
            pre_list = change(pre)
            for i in pre_list:
              pre = pre.replace(i[0],i[1],1)
            if action_temp[2] == 'on':
              v = '0'
            else:
              v = '1'
            if pre:
              pre = '(' + pre + ')' + ' and ' + '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            else:
              pre = '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            pre = pre.replace('&', ' and ')
            pre = pre.replace('|', ' or ')
            action_item[0] = action
            action_item[1] = pre
            fix.append(action_item)
  else:
    if type in device_list:
      fix.append([room + '.' + type + '.' + 'action_' + value, ""])
    else:
      if room != 'Context' and type != 'HumanState':
        if value == 'high':
          action_list = getActionPre([room, type.lower() + '_up'])
          for action_item in action_list:
            action_temp = action_item[0].split('.')
            action = action_temp[0] + '.' + action_temp[1] + '.'  + 'action_' + action_temp[2]
            pre = action_item[1]
            pre_list = change(pre)

            for i in pre_list:
              pre = pre.replace(i[0],i[1],1)
            if action_temp[2] == 'on':
              v = '0'
            else:
              v = '1'

            if pre:
              pre = '(' + pre + ')' + ' and ' + '(' +  pre_value + " != " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            else:
              pre = '(' +  pre_value + " != " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            pre = pre.replace('&', ' and ')
            pre = pre.replace('|', ' or ')
            action_item[0] = action
            action_item[1] = pre
            fix.append(action_item)
        elif value == 'middle':
          action_list = getActionPre([room, type.lower() + '_down'])
          for action_item in action_list:
            action_temp = action_item[0].split('.')
            action = action_temp[0] + '.' + action_temp[1] + '.'  + 'action_' + action_temp[2]
            pre = action_item[1]
            pre_list = change(pre)
            for i in pre_list:
              pre = pre.replace(i[0],i[1],1)
            if action_temp[2] == 'on':
              v = '0'
            else:
              v = '1'
            if pre:
              pre = '(' + pre + ')' + ' and ' + '(' +  pre_value + " != " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            else:
              pre = '(' +  pre_value + " != " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'      
            pre = pre.replace('&', ' and ')
            pre = pre.replace('|', ' or ')
            if pre:
              pre = '(' + pre + ') and ' + "env['space_dict']['" + room + "']['env_state']['" + type + "'].value == 1"
            else:
              pre = "env['space_dict']['" + room + "']['env_state']['" + type + "'].value == 1"
            action_item[0] = action
            action_item[1] = pre
            fix.append(action_item)
          action_list = getActionPre([room, type.lower() + '_up'])
          for action_item in action_list:
            action_temp = action_item[0].split('.')
            action = action_temp[0] + '.' + action_temp[1] + '.'  + 'action_' + action_temp[2]
            pre = action_item[1]
            pre_list = change(pre)
            for i in pre_list:
              pre = pre.replace(i[0],i[1],1)
            if action_temp[2] == 'on':
              v = '0'
            else:
              v = '1'
            if pre:
              pre = '(' + pre + ')' + ' and ' + '(' +  pre_value + " != " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            else:
              pre = '(' +  pre_value + " != " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            pre = pre.replace('&', ' and ')
            pre = pre.replace('|', ' or ')
            if pre:
              pre = '(' + pre + ') and ' + "env['space_dict']['" + room + "']['env_state']['" + type + "'].value == -1"
            else:
              pre = "env['space_dict']['" + room + "']['env_state']['" + type + "'].value == -1"
            action_item[0] = action
            action_item[1] = pre
            fix.append(action_item)
        else:
          action_list = getActionPre([room, type.lower() + '_down'])
          for action_item in action_list:
            action_temp = action_item[0].split('.')
            action = action_temp[0] + '.' + action_temp[1] + '.'  + 'action_' + action_temp[2]
            pre = action_item[1]
            pre_list = change(pre)
            for i in pre_list:
              pre = pre.replace(i[0],i[1],1)
            if action_temp[2] == 'on':
              v = '0'
            else:
              v = '1'
            if pre:
              pre = '(' + pre + ')' + ' and ' + '(' +  pre_value + " != " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            else:
              pre = '(' +  pre_value + " != " + "env['space_dict']['" + room + "']['env_state']['" + type + "'].get()" + ' and ' + v + " == " + "env['space_dict']['" + action_temp[0] + "']['device_dict']['" + action_temp[1] + "'].get()" + ')'
            pre = pre.replace('&', ' and ')
            pre = pre.replace('|', ' or ')
            action_item[0] = action
            action_item[1] = pre
            fix.append(action_item)  
  return fix

def getAction(state, flag):
  actions = ''
  state_temp = state.split('.')
  room = state_temp[0]
  type = state_temp[1]
  value = state_temp[2]
  if not flag:
    if type in device_list:
      if actions:
        actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_' + value + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
      else: 
        actions = '(' + "'" + toSnake(type) + '_' + value + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
    else:
      if type == 'HumanState':
        if actions:
          actions = actions + ' or ' + '(' + "'" + 'human_' + value + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
        else: 
          actions = '(' + "'" + 'human_' + value + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
      elif type == 'Weather':
        if actions:
          actions = actions + ' or ' + '(' + "'" + 'weather_change' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
        else: 
          actions = '(' + "'" + 'weather_change' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
      else:
        if value == 'high':
          action_list = []
          url = "http://47.101.169.122:5002/effect_node/" + room+ '/effect_' + toSnake(type) + '_up'
          results = requests.get(url).json()
          for result in results:
            ltl_action = ''
            action_item = result['room'] + '.' + result['device'][0:len(result['device']) - 3] + '.' + result['action'][7:len(result['action'])]
            ltl_action = action_item
            action_list.append(ltl_action)
          for action in action_list:
            temp_action = action.split('.')
            if '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
              if actions:
                actions = actions + ' or ' + '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
              else: 
                actions = '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
          if '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
            if actions:
              actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
            else: 
              actions = '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
        elif value == 'middle':
          action_list = []
          url = "http://47.101.169.122:5002/effect_node/" + room+ '/effect_' + toSnake(type) + '_up'
          results = requests.get(url).json()
          for result in results:
            ltl_action = ''
            action_item = result['room'] + '.' + result['device'][0:len(result['device']) - 3] + '.' + result['action'][7:len(result['action'])]
            ltl_action = action_item
            action_list.append(ltl_action)
          for action in action_list:
            temp_action = action.split('.')
            if '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
              if actions:
                actions = actions + ' or ' + '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
              else: 
                actions = '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
          if '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
            if actions:
              actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
            else: 
              actions = '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
          action_list = []
          url = "http://47.101.169.122:5002/effect_node/" + room+ '/effect_' + toSnake(type) + '_down'
          results = requests.get(url).json()
          for result in results:
            ltl_action = ''
            action_item = result['room'] + '.' + result['device'][0:len(result['device']) - 3] + '.' + result['action'][7:len(result['action'])]
            ltl_action = action_item
            action_list.append(ltl_action)
          for action in action_list:
            temp_action = action.split('.')
            if '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
              if actions:
                actions = actions + ' or ' + '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
              else: 
                actions = '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
          if '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
            if actions:
              actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
            else:
              actions = '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
        else:
          action_list = []
          url = "http://47.101.169.122:5002/effect_node/" + room+ '/effect_' + toSnake(type) + '_down'
          results = requests.get(url).json()
          for result in results:
            ltl_action = ''
            action_item = result['room'] + '.' + result['device'][0:len(result['device']) - 3] + '.' + result['action'][7:len(result['action'])]
            ltl_action = action_item
            action_list.append(ltl_action)
          for action in action_list:
            temp_action = action.split('.')
            if '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
              if actions:
                actions = actions + ' or ' + '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
              else: 
                actions = '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
          if '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
            if actions:
              actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
            else: 
              actions = '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
  else:
    if type in device_list:
      if value == 'on':
        if actions:
          actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_off' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
        else: 
          actions = '(' + "'" + toSnake(type) + '_off' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
      else:
        if actions:
          actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_on' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
        else: 
          actions = '(' + "'" + toSnake(type) + '_on' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
    else:
      if type == 'HumanState':
        if value == 'detected':
          if actions:
            actions = actions + ' or ' + '(' + "'" + 'human_undetected' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
          else: 
            actions = '(' + "'" + 'human_undetected' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
        else:
          if actions:
            actions = actions + ' or ' + '(' + "'" + 'human_detected' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
          else: 
            actions = '(' + "'" + 'human_detected' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
      elif type == 'Weather':
        if actions:
          actions = actions + ' or ' + '(' + "'" + 'weather_change' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
        else: 
          actions = '(' + "'" + 'weather_change' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
      else:
        if value == 'high':
          action_list = []
          url = "http://47.101.169.122:5002/effect_node/" + room+ '/effect_' + toSnake(type) + '_down'
          results = requests.get(url).json()
          for result in results:
            ltl_action = ''
            action_item = result['room'] + '.' + result['device'][0:len(result['device']) - 3] + '.' + result['action'][7:len(result['action'])]
            ltl_action = action_item
            action_list.append(ltl_action)
          for action in action_list:
            temp_action = action.split('.')
            if '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
              if actions:
                actions = actions + ' or ' + '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
              else: 
                actions = '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
          if '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
            if actions:
              actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
            else: 
              actions = '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
        elif value == 'middle':
          action_list = []
          url = "http://47.101.169.122:5002/effect_node/" + room+ '/effect_' + toSnake(type) + '_up'
          results = requests.get(url).json()
          for result in results:
            ltl_action = ''
            action_item = result['room'] + '.' + result['device'][0:len(result['device']) - 3] + '.' + result['action'][7:len(result['action'])]
            ltl_action = action_item
            action_list.append(ltl_action)
          for action in action_list:
            temp_action = action.split('.')
            if '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
              if actions:
                actions = actions + ' or ' + '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
              else: 
                actions = '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
          if '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
            if actions:
              actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
            else: 
              actions = '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
          
          action_list = []
          url = "http://47.101.169.122:5002/effect_node/" + room+ '/effect_' + toSnake(type) + '_down'
          results = requests.get(url).json()
          for result in results:
            ltl_action = ''
            action_item = result['room'] + '.' + result['device'][0:len(result['device']) - 3] + '.' + result['action'][7:len(result['action'])]
            ltl_action = action_item
            action_list.append(ltl_action)
          for action in action_list:
            temp_action = action.split('.')
            if '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
              if actions:
                actions = actions + ' or ' + '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
              else: 
                actions = '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
          if '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
            if actions:
              actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
            else:
              actions = '(' + "'" + toSnake(type) + '_down' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
        else:
          action_list = []
          url = "http://47.101.169.122:5002/effect_node/" + room+ '/effect_' + toSnake(type) + '_up'
          results = requests.get(url).json()
          for result in results:
            ltl_action = ''
            action_item = result['room'] + '.' + result['device'][0:len(result['device']) - 3] + '.' + result['action'][7:len(result['action'])]
            ltl_action = action_item
            action_list.append(ltl_action)
          for action in action_list:
            temp_action = action.split('.')
            if '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
              if actions:
                actions = actions + ' or ' + '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
              else: 
                actions = '(' + "'" + toSnake(temp_action[1]) + '_' + temp_action[2] + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + temp_action[0]  + "'" + '==' + 'df.iat[index, 2]' + ')'
          if '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')' not in actions:
            if actions:
              actions = actions + ' or ' + '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
            else: 
              actions = '(' + "'" + toSnake(type) + '_up' + "'" + '==' + 'df.iat[index, 0]' + ' and '  + "'" + room  + "'" + '==' + 'df.iat[index, 2]' + ')'
  return actions

def getRegulation():
  regulation = []
  for mtl in MTL:
    trigger = ''
    condition = ''
    fix = []
    temp_mtl = mtl.replace(" ", "")
    temp_mtl = temp_mtl[2:-1]
    item_list = temp_mtl.split('->')
    front = item_list[0]
    end = item_list[1][1:-1]
    time_temp = re.search(r"[FG]\[[0-9,*]+\]",end).group()
    time = time_temp[2:-1].split(',')[1]
    end = end[len(time_temp):]
    if len(front.split('.')) == 2:
      if len(end.split('.')) == 2: 
        effect_list = getEffectList(front.split('.'))
        for item in effect_list:
          fix = []
          item = item.replace(' ','')
          action = re.search(r"[a-zA-Z.]+",item).group()
          room = action.split('.')[0]
          type = action.split('.')[1]
          value = action.split('.')[2]
          condition = item
          trigger_temp = change(condition)
          for i in trigger_temp:
            condition = condition.replace(i[0],i[1],1)
          condition = condition.replace("&", " and ")
          condition = condition.replace("|", " or ")
          pre_temp = change(item[2+len(action):-1])
          pre = item[2+len(action):-1]
          for i in pre_temp:
            pre = pre.replace(i[0],i[1],1)
          pre = pre.replace("&", " and ")
          pre = pre.replace("|", " or ")  
          if '!' in end: 
            match value:
              case 'on':
                action = room + '.' + type + '.' + 'action_off'
              case 'off':
                action = room + '.' + type + '.' + 'action_on'
            trigger = "'" + toSnake(type) + '_' + value + "'" + '==' + 'df.iat[index, 0]' +  ' and ' + "'" + room + "'" + '==' + 'df.iat[index, 2]'
            fix.append([action,pre])
            regulation.append({
              "mtl":mtl,
              "trigger":trigger,
              "time":time,
              "condition":condition,
              "fix":fix,
              "flag":'G',
              "contact": 'or',
              'undo': action
            })  
          else:
            condition = ' not ' + '(' + condition + ')'
            action = room + '.' + type + '.' + 'action_' + value
            trigger = "'" + toSnake(type) + '_' + value + "'" + '==' + 'df.iat[index, 0]' +  ' and ' + "'" + room + "'" + '==' + 'df.iat[index, 2]'
            fix.append([action, pre])
            regulation.append({
              "mtl":mtl,
              "trigger":trigger,
              "time":time,
              "condition":condition,
              "fix":fix,
              "flag":'F',
              "contact": 'or',
              'undo': action
            })     
      else: 
        temp = front.split('.')
        trigger = "df.iat[index, 2] == " + "'"  + temp[0] + "'" + " and " + "df.iat[index, 0] == " + "'"  + temp[1] + "'"
        if '!' in end:
          undo = ''
          fix = getFix(end[1:],False)
          flag = 'F'
          condition = end[1:]
          state_temp = change(condition)
        else:
          undo = 'Undo'
          fix = getFix(end,True)
          flag = 'G'
          condition = end
          state_temp = change(condition)
        for i in state_temp:
          condition = condition.replace(i[0],i[1],1)
        if '!' not in end:
          condition = ' not ' + '(' + condition + ')'
        condition = condition.replace("&", " and ")
        condition = condition.replace("|", " or ")
        
        regulation.append({
          "mtl":mtl,
          "trigger":trigger,
          "time":time,
          "condition":condition,
          "fix":fix,
          "flag":flag,
          "contact": 'or',
          "undo": undo
        })      
    else:  
      if len(end.split('.')) == 2:        
        for item in front[1:-1].split('&'):
          if trigger:
            f = getAction(item,False)
            if f not in trigger:
              trigger = trigger + ' or ' + f
          else:
            trigger = getAction(item,False)
        condition_pre = front[1:-1]
        condition_pre_temp = change(condition_pre)
        for i in condition_pre_temp:
          condition_pre = condition_pre.replace(i[0],i[1],1)
        condition_pre = condition_pre.replace("&", " and ")
        condition_pre = condition_pre.replace("|", " or ")
        if '!' in end:
          undo = ''
          effect_list = getEffectList(end[1:].split('.'))
        else:
          undo = 'Undo'
          effect_list = getEffectList(end.split('.'))
        condition = ''
        fix = []
        for item in effect_list:
          item_condition = item
          item = item.replace(' ','')
          action = re.search(r"[a-zA-Z.]+",item).group()
          room = action.split('.')[0]
          type = action.split('.')[1]
          value = action.split('.')[2]          
          pre_temp = change(item[2+len(action):-1])
          pre = item[2+len(action):-1]
          for i in pre_temp:
            pre = pre.replace(i[0],i[1],1)
          pre = pre.replace("&", " and ")
          pre = pre.replace("|", " or ")  
          if '!' in end: 
            flag = 'F'
            contact = 'and'
            pre_value = ''
            match value:
              case 'on':
                pre_value = '1'
              case 'off':
                pre_value = '0'
            if value == 'on':
              action = room + '.' + type + '.' + 'action_off'
            else:
              action = room + '.' + type + '.' + 'action_on'
            if type in device_list:
              if pre:
                pre = '(' + pre + ')' + ' and ' + '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['device_dict']['" + type + "'].get()" + ')'
              else:
                pre = '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['device_dict']['" + type + "'].get()" + ')'
            fix.append([action,pre])
          else:
            flag= 'G'
            contact = 'or'
            pre_value = ''
            match value:
              case 'on':
                pre_value = '0'
              case 'off':
                pre_value = '1'
            if type in device_list:
              if pre:
                pre = '(' + pre + ')' + ' and ' + '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['device_dict']['" + type + "'].get()" + ')'
              else:
                pre = '(' +  pre_value + " == " + "env['space_dict']['" + room + "']['device_dict']['" + type + "'].get()" + ')'
            action = room + '.' + type + '.' + 'action_' + value
            fix.append([action, pre])   
        
          condition_temp = change(item_condition)
          for i in condition_temp:
            item_condition = item_condition.replace(i[0],i[1],1)
          item_condition = item_condition.replace("&", " and ")
          item_condition = item_condition.replace("|", " or ")
          if condition:
            condition = '(' + item_condition + ')' + ' or ' + '(' +  condition + ')'
          else:
            condition = item_condition
        if '!' not in end:
          condition = ' not ' + '(' + condition + ')'
        condition = '(' + condition_pre + ')' + ' and ' + '(' +  condition + ')'
        regulation.append({
          "mtl":mtl,
          "trigger":trigger,
          "time":time,
          "condition":condition,
          "fix":fix,
          "flag":flag,
          "contact":contact,
          "undo":undo
        })  
      else: 
        trigger = ''
        condition = ''
        fix = []
        for item in front[1:-1].split('&'):
          if trigger:
            trigger = trigger + ' or ' + getAction(item,False)
          else:
            trigger = getAction(item,False)
        if end[0] == '!' :
          contact = 'or'
          undo = 'trigger'
          flag = 'G'
          condition = end[1:]
          temp_condition = change(end[1:])
          for state in end[2:-1].split('&'):
            for fix_item in getFix(state,False):
              fix.append(fix_item)
        else:
          undo = ''
          flag = 'F'
          contact = 'and'
          condition = end
          temp_condition = change(end)
          for state in end[1:-1].split('&'):
            for fix_item in getFix(state,True):
              fix.append(fix_item)
        for i in temp_condition:
          condition = condition.replace(i[0],i[1],1)
        if end[0] != '!' :  
          condition = ' not ' + '(' + condition + ')'
        condition = condition.replace('&', ' and ')
        condition = condition.replace('|', ' or ')
        regulation.append({
          "mtl":mtl,
          "trigger":trigger,
          "time":time,
          "condition":condition,
          "fix":fix,
          "flag":flag,
          "contact":contact,
          "undo":undo
        })  
  return regulation

