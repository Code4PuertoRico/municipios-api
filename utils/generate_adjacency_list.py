import json
from pathlib import Path
from itertools import product

import networkx as nx
from slugify import slugify


def main():
    """
    Read a parsed municipality-adjacency JSON, load the data 
    into a graph and then write the graph to the disk 
    """

    municipality_data = []

    working_dir = Path().absolute()

    # Find the JSON data file and read it
    municipality_file = working_dir.joinpath("data", "municipality_adjacency.json")

    with municipality_file.open() as file_data:
        municipality_data = json.load(file_data)

    # Create a new graph
    graph = nx.Graph()

    # Get the graph nodes (municipality names)
    municipality_nodes = [data.get("municipality") for data in municipality_data]

    # Get the graph edges
    municipality_edges = []

    # Garaph edges are: [(municipality, adjacent_1), (municipality, adjacent_2), ...]
    for data in municipality_data:
        municipality = [slugify(data.get("municipality"))]
        adjacent_list = [slugify(municipality) for municipality in data.get("adjacent")]

        pairs = product(municipality, adjacent_list)

        municipality_edges.extend(list(pairs))

    # Set up the graph
    graph.add_nodes_from(municipality_nodes)
    graph.add_edges_from(municipality_edges)

    # Write the resulting graph to disk
    data_path = working_dir.joinpath("data", "muni_adj.gpickle.gz")
    nx.write_gpickle(graph, data_path.absolute())


if __name__ == "__main__":
    main()
