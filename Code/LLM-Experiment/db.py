from neo4j import GraphDatabase
from py2neo import Graph, Node, Relationship
from utils import Space, Device, Action, Effect

finished_uri = "Bolt://47.101.169.122:7687"
llm_uri = "Bolt://47.101.169.122:7098"
username = "neo4j"
password = "12345678"

def create_driver(uri: str=finished_uri, username: str=username, password: str=password) -> GraphDatabase:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        driver.verify_connectivity()
        print("Connection to the database was successful.")
        return driver
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def create_graph(uri: str=llm_uri, username: str=username, password: str=password) -> Graph:
 return Graph(uri, auth=(username, password))


def get_all_labels(driver) -> list:
    with driver.session() as session:
        query = "CALL db.labels()"
        result = session.run(query)
        labels = [record["label"] for record in result]
        return labels

def get_all_relationship_types(driver) -> list:
    with driver.session() as session:
        query = "CALL db.relationshipTypes()"
        result = session.run(query)
        relationship_types = [record["relationshipType"] for record in result]
        return relationship_types

def query_node_properties(driver, node_label) -> None:
    query = f"""
    MATCH (n:{node_label})
    RETURN n, keys(n) AS properties
    """
    
    with driver.session() as session:
        result = session.run(query)
        print(f"\nProperties for nodes with label '{node_label}':")
        for record in result:
            node = record['n']
            properties = record['properties']
            print(f"Node: {node}, Properties: {properties}")



def get_all_spaces(driver) -> list[Space]:
    query = """
    MATCH (space:Space)
    OPTIONAL MATCH (space)-[:HAS]->(envstate:EnvState)
    OPTIONAL MATCH (space)<-[:BELONG_TO]-(device:Device)-[:CAN]->(action:Action)
    RETURN space, collect(DISTINCT envstate) AS envstates, 
           collect(DISTINCT {name: device.name, type: device.type, action: action.name, state: device.state}) AS device_actions
    """
    
    with driver.session() as session:
        result = session.run(query)
        spaces = []
        for record in result:
            space_name = record['space']['name']
            envstates = [envstate['name'] for envstate in record['envstates'] if envstate is not None]
            
            devices = {}
            for d in record['device_actions']:
                if d['name'] is not None:
                    if d['name'] not in devices:
                        devices[d['name']] = Device(d['name'], d['type'], d['state'])
                    devices[d['name']].add_action(d['action'])
                    # print(d['action'])
            
            space = Space(space_name, envstates, list(devices.values()))
            spaces.append(space)
        
        return spaces

def add_effect_node(graph:Graph, effect: Effect) -> Node:
    assert effect is not None, "Effect is None"
    effect_node = Node("Effect", name=effect.name)
    graph.create(effect_node)
    return effect_node

def add_action_node(graph: Graph, action: Action) -> Node:
    assert action is not None, "Action is None"
    action_node = Node("Action", name=action.name)
    for effect in action.effects:
        effect_node = add_effect_node(graph, effect)
        graph.create(Relationship(action_node, "HAS", effect_node))
    graph.create(action_node)
    return action_node

def add_device_node(graph: Graph, device: Device) -> Node:
    assert device is not None, "Device is None"
    device_node = Node("Device", name=device.name, type=device.type, state=device.state)
    for action in device.actions:
        action_node = add_action_node(graph, action)
        graph.create(Relationship(device_node, "CAN", action_node))
    graph.create(device_node)
    return device_node

def add_space_node(graph: Graph, space: Space) -> None:
    assert space is not None, "Space is None"
    space_node = Node("Space", name=space.name)
    for envstate in space.envstate:
        envstate_node = Node("EnvState", name=envstate)
        graph.create(envstate_node)
        graph.create(Relationship(space_node, "HAS", envstate_node))
    for device in space.devices:
        device_node = add_device_node(graph, device)
        graph.create(Relationship(device_node, "BELONG_TO", space_node))
    graph.create(space_node)

def delete_all_nodes(graph: Graph) -> None:
    query = """
    MATCH (n)
    DETACH DELETE n
    """
    graph.run(query)