import configparser
from py2neo import Graph, Node, Relationship
from flask import Flask, render_template
import json

config = configparser.ConfigParser()
config.read("config.ini")

host = "47.101.169.122"
port = "7690"
username = "neo4j"
password = "12345678"

graph = Graph(f"neo4j://{host}:{port}", auth=(username, password))


def get_room():
    res = []
    data = graph.run("match (n:Space) return n").data()
    for i in data:
        res.append(i["n"]["name"])
    return res


def get_device_by_room(room_name):
    res = []
    data = graph.run("match (n:Device)-[r:BELONG_TO]->(nn) where nn.name='" + room_name + "' return n").data()
    for i in data:
        res.append(i["n"]["name"])
    return res


def get_effect_by_room(room_name):
    res = []
    data = graph.run("match (n:Effect) where n.room='" + room_name + "' return n").data()
    for i in data:
        res.append(i["n"]["name"])
    result = []
    for item in res:
        if item not in result:
            result.append(item)
    return result


def get_event_by_room(room_name):
    res = []
    data = graph.run("match (n:Event) where n.room='" + room_name + "' return n").data()
    for i in data:
        res.append(i["n"]["name"])
    result = []
    for item in res:
        if item not in result:
            result.append(item)
    return result


def get_state_by_room(room_name):
    res = []
    data = graph.run("match (m)-[r:HAS]->(n:EnvState) where m.name='" + room_name + "' return n").data()
    for i in data:
        res.append(i["n"]["name"])
    return res


def get_device(room_name, device_name):
    res = {}
    data = graph.run("match (n:Device)-[r:BELONG_TO]->(nn) where n.name='" + device_name +
                     "' and nn.name='" + room_name + "' return n").data()[0]["n"]
    res["name"] = data["name"]
    res["state"] = data["state"]
    res["type"] = data["type"]
    res["adjacent"] = data["adjacent"]
    return res


def get_state(room_name, state_name):
    res = {}
    data = graph.run("match (m)-[r:HAS]->(n:EnvState) where m.name='" + room_name + "' and n.name='" + state_name + "' return n").data()[0]["n"]
    res["name"] = data["name"]
    res["value"] = data["value"]
    return res


def get_action_by_device(room_name, device_name):
    res = []
    actions = graph.run("match (n:Action)<-[:CAN]-(m:Device)-[:BELONG_TO]->(nn) where m.name='" +
                        device_name + "' and nn.name='" + room_name + "' return n").data()
    for i in actions:
        res.append(i["n"]["name"])
    return res


def get_action_by_room(room_name):
    res = []
    data = graph.run("match (n:Action) where n.device is not null and n.room='" + room_name + "' return n").data()
    for i in data:
        action = i["n"]["name"][7:]
        device = i["n"]["device"][:len(i["n"]["device"])-3]
        temp = device + '.' + action
        res.append(temp)
    result = []
    for item in res:
        if item not in result:
            result.append(item)
    return result


def get_action_by_state(room_name, state_name):
    res = []
    actions = graph.run("match (nn)-[:HAS]->(m:EnvState)-[:CAN]->(n:Action) where m.name='" +
                        state_name + "' and nn.name='" + room_name + "' return n").data()
    for i in actions:
        res.append(i["n"]["name"])
    return res


def get_effect_and_pre(room_name, device_name, action_name):
    res = {}
    data = graph.run("match (p)<-[:DEPENDING_ON]-(e:Effect)<-[:HAS]-(a:Action)<-[:CAN]-(d:Device) where e.room='" +
                     room_name + "' and  a.name='" + action_name + "' and d.name='" + device_name + "' return e, p").data()
    if len(data) == 0:
        data = graph.run("match (e:Effect)<-[:HAS]-(a:Action)<-[:CAN]-(d:Device) where e.room='" + room_name +
                         "' and  a.name='" + action_name + "' and d.name='" + device_name + "' return e").data()
    for i in data:
        effect_value = i["e"]["value"]
        if effect_value in res:
            res[effect_value] = (i["e"]["pre_condition"])
            continue
        res[effect_value] = []
        res[effect_value] = (i["e"]["pre_condition"])
    return res


def get_room_related(room_name):
    res = []
    data = graph.run("match (n)-[:ADJACENT_TO]->(m) where m.name='" + room_name + "' return n").data()
    for i in data:
        res.append(i["n"]["name"])
    return res


def get_effect_node(room, effect):
    result = []
    res = []
    data = graph.run("match (n:Effect) where n.name='" + effect + "' and n.room='" +
                     room + "' and n.value STARTS WITH '" + room + "' return n").data()
    for i in data:
        res.append(i["n"])
    for item in res:
        if item not in result:
            result.append(item)

    adjcent = get_room_related(room)
    for item in adjcent:
        res = []
        data = graph.run("match (n:Effect) where n.name='" + effect + "' and n.room='" +
                         item + "' and n.value STARTS WITH '" + room + "' return n").data()
        for i in data:
            res.append(i["n"])
        for item in res:
            if item not in result:
                result.append(item)
    return result


def modify_device_value(room_name, device_name, new_state):
    query = "MATCH (d:Device)-[:BELONG_TO]->(r) WHERE r.name = $room_name AND d.name = $device_name SET d.state = $new_state"
    graph.run(query, room_name=room_name, device_name=device_name, new_state=new_state)
    result = graph.run("MATCH (d:Device)-[:BELONG_TO]->(r) WHERE r.name = $room_name AND d.name = $device_name RETURN d",
                       room_name=room_name, device_name=device_name)
    result_list = list(result)
    
    return result_list

def modify_state_value(room_name, state_name, new_value):
    query = "MATCH (d:EnvState)<-[:HAS]-(r) WHERE r.name = $room_name AND d.name = $state_name SET d.value = $new_value"
    graph.run(query, room_name=room_name, state_name=state_name, new_value=new_value)
    result = graph.run("MATCH (d:EnvState)<-[:HAS]-(r) WHERE r.name = $room_name AND d.name = $state_name RETURN d.value",
                       room_name=room_name, state_name=state_name)
    result_list = list(result)
    
    return result_list
    
app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the homepage!"

@app.route('/set_device_value/<room_name>/<device_name>/<new_state>', methods=['POST'])
def set_device_value(room_name, device_name, new_state):
    return modify_device_value(room_name, device_name, new_state)

@app.route('/set_state_value/<room_name>/<state_name>/<new_value>', methods=['POST'])
def set_state_value(room_name, state_name, new_value):
    return modify_state_value(room_name, state_name, new_value)


@app.route('/room_list')
def room_list():
    return get_room()


@app.route('/effect_list/<room_name>')
def effect_list(room_name):
    return get_effect_by_room(room_name)


@app.route('/event_list/<room_name>')
def event_list(room_name):
    return get_event_by_room(room_name)


@app.route('/effect_node/<room_name>/<effect_name>')
def effect_node(room_name, effect_name):
    return get_effect_node(room_name, effect_name)


@app.route('/room_device/<room_name>')
def room_device(room_name):
    return get_device_by_room(room_name)


@app.route('/room_state/<room_name>')
def room_state(room_name):
    return get_state_by_room(room_name)


@app.route('/action_list_by_device/<room_name>/<device_name>')
def action_list_by_device(room_name, device_name):
    return get_action_by_device(room_name, device_name)


@app.route('/action_list_by_state/<room_name>/<state_name>')
def action_list_by_state(room_name, state_name):
    return get_action_by_state(room_name, state_name)


@app.route('/effect_and_pre/<room_name>/<device_name>/<action_name>')
def effect_and_pre(room_name, device_name, action_name):
    return get_effect_and_pre(room_name, device_name, action_name)


@app.route('/room_relation/<room_name>')
def room_relation(room_name):
    return get_room_related(room_name)


@app.route('/room_device_info/<room_name>/<device_name>')
def room_device_info(room_name, device_name):
    return get_device(room_name, device_name)


@app.route('/room_state_info/<room_name>/<state_name>')
def room_state_info(room_name, state_name):
    return get_state(room_name, state_name)


@app.route('/room_action/<room_name>')
def room_action(room_name):
    return get_action_by_room(room_name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
