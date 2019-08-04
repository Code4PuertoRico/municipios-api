from pathlib import Path

import networkx as nx
from flask import Flask, escape, redirect, request, jsonify, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


ALL_MUNICIPALITIES = [
    "adjuntas",
    "aguada",
    "aguadilla",
    "aguas-buenas",
    "aibonito",
    "anasco",
    "arecibo",
    "arroyo",
    "barceloneta",
    "barranquitas",
    "bayamon",
    "cabo-rojo",
    "caguas",
    "camuy",
    "canovanas",
    "carolina",
    "catano",
    "cayey",
    "ceiba",
    "ciales",
    "cidra",
    "coamo",
    "comerio",
    "corozal",
    "culebra",
    "dorado",
    "fajardo",
    "florida",
    "guanica",
    "guayama",
    "guayanilla",
    "guaynabo",
    "gurabo",
    "hatillo",
    "hormigueros",
    "humacao",
    "isabela",
    "jayuya",
    "juana-diaz",
    "juncos",
    "lajas",
    "lares",
    "las-marias",
    "las-piedras",
    "loiza",
    "luquillo",
    "manati",
    "maricao",
    "maunabo",
    "mayaguez",
    "moca",
    "morovis",
    "naguabo",
    "naranjito",
    "orocovis",
    "patillas",
    "penuelas",
    "ponce",
    "quebradillas",
    "rincon",
    "rio-grande",
    "sabana-grande",
    "salinas",
    "san-german",
    "san-juan",
    "san-lorenzo",
    "san-sebastian",
    "santa-isabel",
    "toa-alta",
    "toa-baja",
    "trujillo-alto",
    "utuado",
    "vega-alta",
    "vega-baja",
    "vieques",
    "villalba",
    "yabucoa",
    "yauco",
]


def get_adjacency_graph():
    data_path = Path().absolute().joinpath("data", "muni_adj.gpickle.gz")
    return nx.read_gpickle(data_path)


def get_distance_between(first_node, second_node):
    graph = get_adjacency_graph()
    shortest_path = nx.shortest_path(graph, source=first_node, target=second_node)

    # Distance has a minus two to subtract the source node and the target node from the list
    return dict(path=shortest_path, distance=len(shortest_path) - 2)


def get_n_adjacent_municipalities(source_node, n):
    graph = get_adjacency_graph()
    distance_dict = nx.shortest_path_length(graph, source=source_node)

    return [
        municipality
        for municipality, distance in distance_dict.items()
        if distance == n
    ]


@app.route("/distancia/<first_municipality>/<second_municipality>")
@app.route("/distance/<first_municipality>/<second_municipality>")
def distance(first_municipality, second_municipality):

    if first_municipality not in ALL_MUNICIPALITIES:
        return jsonify(error=f"{escape(first_municipality)} is invalid"), 404

    if second_municipality not in ALL_MUNICIPALITIES:
        return jsonify(error=f"{escape(second_municipality)} is invalid"), 404

    distance = get_distance_between(first_municipality, second_municipality)

    return jsonify(result=distance)


@app.route("/adjacent/<municipality>")
@app.route("/adjacente/<municipality>")
def adjacent(municipality):
    if municipality not in ALL_MUNICIPALITIES:
        return jsonify(error=f"{escape(municipality)} is invalid"), 404

    distance = request.args.get("distance", request.args.get("distancia"))

    if not distance or not distance.isdigit():
        distance = 1

    adjacent = get_n_adjacent_municipalities(municipality, int(distance))
    return jsonify(result=adjacent)


@app.route("/")
def hello():
    return redirect(url_for("adjacent", municipality="dorado", distance=1))
