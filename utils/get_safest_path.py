def abs(num):
  if num < 0:
    return -num
  return num

def get_distance(nodes_map, first_node_id, second_node_id):
  x_dist = nodes_map[first_node_id]["ui"]["x"] - nodes_map[second_node_id]["ui"]["x"]
  y_dist = nodes_map[first_node_id]["ui"]["y"] - nodes_map[second_node_id]["ui"]["y"]
  return abs(x_dist) + abs(y_dist)

def dijkstra(nodes_map, start_node_id):
  distances = {}
  previous_nodes = {}
  for nodes_id in nodes_map:
    distances[nodes_id] = float('inf')
    previous_nodes[nodes_id] = None
  
  distances[start_node_id] = 0
  queue = [(0, start_node_id)]
  while len(queue):
    current_distance, current_node_id = queue.pop()
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

def get_safest_path(floorData):
  nodes = floorData.get("nodes", [])
  nodes_map = {}
  exit_node_ids = []
  distance = {}
  previous_node = {}
  for node in nodes:
    if node["isExit"]:
      exit_node_ids.append(node["id"])
    nodes_map[node["id"]] = node
    distance[node["id"]] = float("inf")
    previous_node[node["id"]] = None
  

  for exit_node_id in exit_node_ids:
    distances, previous_nodes = dijkstra(nodes_map, exit_node_id)
    for node_id in nodes_map:
      if distance[node_id] > distances[node_id]:
        distance[node_id] = distances[node_id]
        previous_node[node_id] = previous_nodes[node_id]
  
  return distance, previous_node