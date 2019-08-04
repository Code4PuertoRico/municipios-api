import re
import json
from pathlib import Path


def parse_municipality(municipality_string):
    split_string = re.split(r"Municipio", municipality_string)

    # Municipality is the first set of words before "Municipio" in the data
    return split_string[0].lower().strip()


def main():

    # List of dictionaries for each municipality
    results = []

    working_dir = Path().absolute()

    adjecency_file = working_dir.joinpath("data", "county_adjacency.txt")
    with adjecency_file.open() as file_data:

        # Data for each municipality is separated by two newlines
        data = file_data.read().split("\n\n")

        # Each data set contains the municipality itself along with adjacent municipalities
        for municipality_group in data:

            # Parse the data, removing quotes and whitespace
            municipality_info = [
                municipality.strip().replace('"', "")
                for municipality in municipality_group.split("\n")
            ]

            # Get the municipality as well as the adjacent municipalities from the parsed info
            municipality = parse_municipality(municipality_info[0])
            adjacent_municipalities = [
                parse_municipality(municipality)
                for municipality in municipality_info[1:]
            ]

            # Do not count the municipality itself as adjacent to itself
            adjacent_municipalities.remove(municipality)

            # Add the data to the results list
            results.append(
                dict(municipality=municipality, adjacent=adjacent_municipalities)
            )

    result_file = working_dir.joinpath("data", "municipality_adjacency.json")

    # Write the result to disk
    json.dump(results, result_file.open("w"))


if __name__ == "__main__":
    main()
