[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) 

## To-Do

1. Add a `CONTRIBUTING.md`.
1. Add issue and pull request templates.

## What
    
This is source code for generating a graph representation of Puerto Rico municipalities as well as for running a Flask API that can retrieve useful data from the graph.
    
## Where

You can use the API at [municipios.rauln.com](https://municipios.rauln.com). There are two endpoints: `/distance` and `/adjacent`. The API is very simple and can be explained with two examples:


* `GET https://municipios.rauln.com/distance/san-juan/mayaguez`

```json
{
  "result": {
    "distance": 8,
    "path": [
      "san-juan",
      "toa-baja",
      "dorado",
      "vega-alta",
      "manati",
      "ciales",
      "utuado",
      "lares",
      "las-marias",
      "mayaguez"
    ]
  }
}
```


* `GET https://municipios.rauln.com/adjacent/san-juan?distance=1`

```json
{
  "result": [
    "aguas-buenas",
    "caguas",
    "carolina",
    "catano",
    "guaynabo",
    "toa-baja",
    "trujillo-alto"
  ]
}
```

## How

The data was obtained from from publicly available sources (see [Credits](#Credits)). Graph creation and traversal is handled by [NetworkX](https://networkx.github.io/).
The API was written using [Flask](https://palletsprojects.com/p/flask/), the code runs in [AWS Lambda](https://aws.amazon.com/lambda/) behind an [AWS API Gateway](https://aws.amazon.com/api-gateway/) and is managed via [Zappa](https://github.com/Miserlou/Zappa).

## Why

I needed to know the answer to the following type of question: What are the three municipalities nearest to Guaynabo? I'm building an [open source API](https://github.com/rnegron/cc-api) which would find that sort of information useful. I'm sharing the information via code/API in case someone else finds it useful too!


## Processes

1. Manually edit the country adjacency text file to make it easier to parse

1. Parse the text file with `utils/parse_country_adjacency.py`

1. Store the resulting JSON in `data/municipality_adjacency.json`

1. Process the JSON, generate a graph and write the graph to a file with `utils/generate_adjacency_list.py`

1. Use the resulting `data/adjacency_list.gz` in the API to calculate adjacency and distance data for municipalities.


## Credits

Municipality adjacency data obtained from publicly available [Census data](https://www.census.gov/geographies/reference-files/2010/geo/county-adjacency.html).
