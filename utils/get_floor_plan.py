from utils.urequest import urlopen
def get_floor_plan(floor_id, headers=None):
  if floor_id is None:
    return None

  url = "https://first-response-server-v2-0.onrender.com/graphql"
  query = """
    query($floorId: ID!){
      getFloorPlan(id: $floorId) {
        id
        name
        nodes {
          id
          name
          state
          isExit
          ui {
            x
            y
          }
          connections {
            id
            name
            direction
          }
        }
      }
    }
  """
  variables = {"floorId": floor_id}
  data = {
    "query": query,
    "variables": variables
  }
  copied_headers = headers.copy()
  copied_headers["Content-Type"] = "application/json"
  response = urlopen(url, data=data, method="POST", headers=copied_headers)
  return response