import argparse

import mesa
import mesa_geo as mg
from src.model.model import AgentsAndNetworks
from src.visualization.server import (
    agent_draw,
    clock_element,
    friendship_chart,
    status_chart,
)


def make_parser():
    parser = argparse.ArgumentParser("Agents and Networks in Python")
    parser.add_argument("--campus", type=str, required=True)
    return parser


if __name__ == "__main__":
    args = make_parser().parse_args()

    if args.campus == "ub":
        data_file_prefix = "UB"
    elif args.campus == "gmu":
        data_file_prefix = "Mason"
    else:
        raise ValueError("Invalid campus name. Choose from ub or gmu.")

    campus_params = {
        "ub": {"data_crs": "epsg:4326", "commuter_speed": 0.5},
        "gmu": {"data_crs": "epsg:2283", "commuter_speed": 0.4},
    }
    model_params = {
        "campus": args.campus,
        "data_crs": campus_params[args.campus]["data_crs"],
        "buildings_file": f"data/{args.campus}/{data_file_prefix}_bld.zip",
        "walkway_file": f"data/{args.campus}/{data_file_prefix}_walkway_line.zip",
        "lakes_file": f"data/{args.campus}/hydrop.zip",
        "rivers_file": f"data/{args.campus}/hydrol.zip",
        "driveway_file": f"data/{args.campus}/{data_file_prefix}_Rds.zip",
        "show_walkway": True,
        "show_lakes_and_rivers": True,
        "show_driveway": True,
        "num_commuters": mesa.visualization.Slider(
            "Number of Commuters", value=50, min_value=10, max_value=150, step=10
        ),
        "commuter_speed": mesa.visualization.Slider(
            "Commuter Walking Speed (m/s)",
            value=campus_params[args.campus]["commuter_speed"],
            min_value=0.1,
            max_value=1.5,
            step=0.1,
        ),
    }
    map_element = mg.visualization.MapModule(agent_draw, map_height=600, map_width=600)
    server = mesa.visualization.ModularServer(
        AgentsAndNetworks,
        [map_element, clock_element, status_chart, friendship_chart],
        "Agents and Networks",
        model_params,
    )
    server.launch()
