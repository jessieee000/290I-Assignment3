from fastapi import FastAPI, File, UploadFile
from typing_extensions import Annotated
import uvicorn
from utils import *
from dijkstra import dijkstra

# create FastAPI app
app = FastAPI()

# global variable for active graph
active_graph = None

@app.get("/")
async def root():
    return {"message": "Welcome to the Shortest Path Solver!"}


@app.post("/upload_graph_json/")
async def create_upload_file(file: UploadFile):
    # TODO: implement this function
    global active_graph

    filename = file.filename.lower()

    try:
        if filename.endswith(".json"):
            active_graph = create_graph_from_json(file)
            file_type = "JSON"
        elif filename.endswith(".csv"):
            active_graph = create_graph_from_csv(file)
            file_type = "CSV"
        else:
            return {"Upload Error":"Invalid file type"}

        num_nodes = len(active_graph.nodes)
        return { "Upload Success":"<file_name>"}

    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}


@app.get("/solve_shortest_path/start_node_id={start_node_id}&end_node_id={end_node_id}")
async def get_shortest_path(start_node_id: str, end_node_id: str):
    global active_graph

    if active_graph is None:
        return {"Solver Error": "No active graph, please upload a graph first."}

    if start_node_id not in active_graph.nodes or end_node_id not in active_graph.nodes:
        return {"Solver Error": "Invalid start or end node ID."}

    # --- Dijkstra ---
    start_node = active_graph.nodes[start_node_id]
    result_graph = dijkstra(active_graph, start_node)

    path = []
    current = active_graph.nodes[end_node_id]
    total_distance = current.dist

    while current is not None:
        path.insert(0, current.id)
        current = current.prev

    if len(path) == 1 and path[0] != start_node_id:
        return {"Solver Error": "No path found between the given nodes."}

    return {
        "shortest_path": path,
        "total_distance": total_distance
    }

if __name__ == "__main__":
    print("Server is running at http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
    