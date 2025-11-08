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
            return {"error": "Unsupported file type. Please upload .json or .csv"}

        num_nodes = len(active_graph.nodes)
        return {
            "message": f"{file_type} file uploaded successfully.",
            "filename": file.filename,
            "num_nodes": num_nodes
        }

    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}


@app.get("/solve_shortest_path/start_node_id={start_node_id}&end_node_id={end_node_id}")
async def get_shortest_path(start_node_id: str, end_node_id: str):
    # TODO: implement this function
    global active_graph 

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
        return {"shortest_path": [], "total_distance": None, "message": "No path found"}

    return {
        "shortest_path": path,
        "total_distance": total_distance
    }

if __name__ == "__main__":
    print("Server is running at http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
    