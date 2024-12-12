'''from graphviz import Digraph
import os

# Define a fixed directory for the output
output_dir = "C:/diagrams"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Define the output path for the PNG file
output_path = os.path.join(output_dir, "Search_Application_DFD")

# Create a Digraph object for the DFD
dfd = Digraph(format='png', graph_attr={'rankdir': 'LR'}, name="Data Flow Diagram")

# Add nodes for external entities, processes, and data stores
dfd.node("User", shape="rectangle", style="filled", color="lightblue", label="User")
dfd.node("API", shape="rectangle", style="filled", color="lightblue", label="External API")
dfd.node("Search Engine", shape="ellipse", style="filled", color="lightgreen", label="Search Engine (Elasticsearch)")
dfd.node("Database", shape="cylinder", style="filled", color="lightgrey", label="Catalog Database")
dfd.node("Frontend", shape="ellipse", style="filled", color="lightyellow", label="Frontend (UI)")

# Processes
dfd.node("P1", shape="ellipse", style="filled", color="orange", label="Process Search Query")
dfd.node("P2", shape="ellipse", style="filled", color="orange", label="Apply Filters and Sort")
dfd.node("P3", shape="ellipse", style="filled", color="orange", label="Retrieve and Index Data")
dfd.node("P4", shape="ellipse", style="filled", color="orange", label="Display Results")

# Connect nodes with labeled edges
dfd.edge("User", "Frontend", label="Input: Search Query, Filters")
dfd.edge("Frontend", "P1", label="Send Query")
dfd.edge("P1", "Search Engine", label="Query Search Engine")
dfd.edge("Search Engine", "P2", label="Filtered Results")
dfd.edge("P2", "Database", label="Retrieve Data")
dfd.edge("Database", "P3", label="Raw Data")
dfd.edge("P3", "P4", label="Processed Data")
dfd.edge("P4", "Frontend", label="Formatted Results")
dfd.edge("Frontend", "User", label="Output: Search Results")
dfd.edge("P3", "API", label="Fetch External Data")
dfd.edge("API", "Database", label="Store Retrieved Data")

# Render the diagram
try:
    dfd.render(output_path, format="png", cleanup=True)
    print(f"Diagram saved successfully at: {output_path}.png")
except Exception as e:
    print(f"An error occurred while saving the diagram: {e}")

# To make independent change on this data flow diagram 
# Please download Graphviz and add the path 
# If you are using vs code before you run this code and enter pip install graphviz 
# when you run this program it will save PNG in your Local C drive in the diagram folder for eg C/ diagram / Diagram.png
'''
import json
import os

from graphviz import Digraph

# Configuration for dynamic diagram creation
config = {
    "output_dir": "C:/diagrams",
    "output_filename": "Search_Application_DFD",
    "nodes": [
        {"id": "User", "shape": "rectangle", "color": "lightblue", "label": "User"},
        {"id": "API", "shape": "rectangle", "color": "lightblue", "label": "External API"},
        {"id": "Search Engine", "shape": "ellipse", "color": "lightgreen", "label": "Search Engine (Elasticsearch)"},
        {"id": "Database", "shape": "cylinder", "color": "lightgrey", "label": "Catalog Database"},
        {"id": "Frontend", "shape": "ellipse", "color": "lightyellow", "label": "Frontend (UI)"},
        {"id": "P1", "shape": "ellipse", "color": "orange", "label": "Process Search Query"},
        {"id": "P2", "shape": "ellipse", "color": "orange", "label": "Apply Filters and Sort"},
        {"id": "P3", "shape": "ellipse", "color": "orange", "label": "Retrieve and Index Data"},
        {"id": "P4", "shape": "ellipse", "color": "orange", "label": "Display Results"}
    ],
    "edges": [
        {"src": "User", "dest": "Frontend", "label": "Input: Search Query, Filters"},
        {"src": "Frontend", "dest": "P1", "label": "Send Query"},
        {"src": "P1", "dest": "Search Engine", "label": "Query Search Engine"},
        {"src": "Search Engine", "dest": "P2", "label": "Filtered Results"},
        {"src": "P2", "dest": "Database", "label": "Retrieve Data"},
        {"src": "Database", "dest": "P3", "label": "Raw Data"},
        {"src": "P3", "dest": "P4", "label": "Processed Data"},
        {"src": "P4", "dest": "Frontend", "label": "Formatted Results"},
        {"src": "Frontend", "dest": "User", "label": "Output: Search Results"},
        {"src": "P3", "dest": "API", "label": "Fetch External Data"},
        {"src": "API", "dest": "Database", "label": "Store Retrieved Data"}
    ]
}

# Create output directory if it doesn't exist
os.makedirs(config["output_dir"], exist_ok=True)

# Define the output path for the PNG file
output_path = os.path.join(config["output_dir"], config["output_filename"])

# Create a Digraph object for the DFD
dfd = Digraph(format='png', graph_attr={'rankdir': 'LR'}, name="Data Flow Diagram")

# Add nodes dynamically from configuration
for node in config["nodes"]:
    dfd.node(node["id"], shape=node["shape"], style="filled", color=node["color"], label=node["label"])

# Add edges dynamically from configuration
for edge in config["edges"]:
    dfd.edge(edge["src"], edge["dest"], label=edge["label"])

# Render the diagram
try:
    dfd.render(output_path, format="png", cleanup=True)
    print(f"Diagram saved successfully at: {output_path}.png")
except Exception as e:
    print(f"An error occurred while saving the diagram: {e}")

# Optional: Save configuration to JSON for reproducibility
config_path = os.path.join(config["output_dir"], "diagram_config.json")
with open(config_path, "w") as config_file:
    json.dump(config, config_file, indent=4)
    print(f"Configuration saved at: {config_path}")
