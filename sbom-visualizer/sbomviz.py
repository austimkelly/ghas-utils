import sys
import json
import networkx as nx
import matplotlib.pyplot as plt

def visualize_sbom(json_file):
    try:
        # Load SBOM data from JSON file
        with open(json_file, 'r') as file:
            sbom_data = json.load(file)

        # Create a directed graph
        dependency_graph = nx.DiGraph()

        # Add nodes for each package
        for package in sbom_data['packages']:
            dependency_graph.add_node(package['SPDXID'], name=package['name'], version=package.get('versionInfo', ''))

        # Add edges for dependencies
        for relationship in sbom_data['relationships']:
            if relationship['relationshipType'] == 'DEPENDS_ON':
                dependency_graph.add_edge(relationship['spdxElementId'], relationship['relatedSpdxElement'])

        # Visualize the graph with enhanced interactivity
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(dependency_graph, seed=42)
        labels = nx.get_edge_attributes(dependency_graph, 'relationshipType')

        nx.draw_networkx_nodes(dependency_graph, pos, node_size=500, node_color='skyblue', alpha=0.8)
        nx.draw_networkx_edges(dependency_graph, pos, edge_color='gray', alpha=0.5)
        nx.draw_networkx_labels(dependency_graph, pos, labels=nx.get_node_attributes(dependency_graph, 'name'))

        nx.draw_networkx_edge_labels(dependency_graph, pos, edge_labels=labels)

        plt.title('Dependency Graph Visualization')
        plt.axis('off')

        # Add interactivity for zooming and panning
        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())

        plt.show()

    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{json_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualize_sbom.py <path_to_json_file>")
    else:
        json_file_path = sys.argv[1]
        visualize_sbom(json_file_path)
