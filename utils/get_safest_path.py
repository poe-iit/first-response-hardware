def abs(num):
  if num < 0:
    return -num
  return num

def get_distance(nodes_map, first_node_id, second_node_id):
  x_dist = nodes_map[first_node_id]["ui"]["x"] - nodes_map[second_node_id]["ui"]["x"]
  y_dist = nodes_map[first_node_id]["ui"]["y"] - nodes_map[second_node_id]["ui"]["y"]
  return abs(x_dist) + abs(y_dist)

def dijkstra(nodes_map, start_node_id, ignore_compromised=False):
  distances = {}
  previous_nodes = {}
  for nodes_id in nodes_map:
    distances[nodes_id] = float('inf')
    previous_nodes[nodes_id] = None
  
  distances[start_node_id] = 0
  queue = [(0, start_node_id)]
  while len(queue):
    current_distance, current_node_id = queue.pop()
    if ignore_compromised and nodes_map[current_node_id]["state"] == "compromised":
      continue
    if current_distance > distances[current_node_id]:
      continue
    
    for neighbor in nodes_map[current_node_id]['connections']:
      neighbor_id = neighbor['id']
      distance = current_distance + get_distance(nodes_map, current_node_id, neighbor_id)

      if distance < distances[neighbor_id]:
        distances[neighbor_id] = distance
        previous_nodes[neighbor_id] = current_node_id
        queue.append((distance, neighbor_id))
        queue.sort(key=lambda x: x[0], reverse=True)
  return distances, previous_nodes

def get_safest_path(node_id, floorData):
  nodes = floorData.get("nodes", [])
  nodes_map = {}
  exit_node_ids = []
  distance = {}
  previous_node = {}
  for node in nodes:
    if node["isExit"] and node["state"] != "compromised":
      exit_node_ids.append(node["id"])
    nodes_map[node["id"]] = node
    distance[node["id"]] = float("inf")
    previous_node[node["id"]] = None
  
  # exit, or safe, or compromised or stuck

  # return color and direction
  if nodes_map[node_id]["isExit"] and nodes_map[node_id]["state"] == "safe":
    return (76, 175, 80), "all"
  distance = float("inf")
  safest_node_id = None
  # Can't be a safe exit if it got here
  for exit_node_id in exit_node_ids:
    distances, previous_nodes = dijkstra(nodes_map, exit_node_id, True)
    if distance > distances[node_id]:
      distance = distances[node_id]
      safest_node_id = previous_nodes[node_id]
      if nodes_map[node_id]["state"] == "safe":
        color = (2, 119, 189)
      elif nodes_map[node_id]["state"] == "compromised":
        color = (230, 57, 70)
  
  if distance == float("inf"):
    # Can't be safe if it got here
    if nodes_map[node_id]["state"] == "compromised":
      color = (230, 57, 70)
    else:
      color = (255, 136, 0)
    for exit_node_id in exit_node_ids:
      distances, previous_nodes = dijkstra(nodes_map, exit_node_id)
      if distance > distances[node_id]:
        distance = distances[node_id]
        safest_node_id = previous_nodes[node_id]
  
  for connection in nodes_map[node_id]["connections"]:
    if connection["id"] == safest_node_id:
      node = nodes_map[node_id]
      safest_node = nodes_map[safest_node_id]
      if connection["direction"] == "xy":
        if node["ui"]["x"] > safest_node["ui"]["x"]:
          direction = "left"
        else:
          direction = "right"
      else:
        if node["ui"]["y"] > safest_node["ui"]["y"]:
          direction = "up"
        else:
          direction = "down"
  if direction is None:
    direction = "all"
  return color, direction