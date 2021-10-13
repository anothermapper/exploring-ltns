from time import sleep
from icecream import ic
import json
import pandas as pd
from pathlib import Path
import requests

ic.enable()

route_osrm_params = {
    "alternatives": "false",
    "steps": "false",
    "annotations": "nodes",
    "geometries": "polyline",
    "overview": "false",
    "continue_straight": "default",
}

# all_results = {}


def bulk_calculate_routes(reng, route_list_gdf, results_dir):

    if not Path.exists(results_dir):
        Path.mkdir(results_dir, parents=True)

    route_summary = {
        "route_id": [],
        "verb": [],
        "distance": [],
        "duration": [],
        "weight_name": [],
        "weight": [],
    }

    all_results = {}

    for verb in reng.transport_params.key():

        reng.run_routing_server(verb)
        base_osrm_url = f"http://127.0.0.1:{host_port}/route/v1/{verb}/"

        route_all_nodes = {
            "route_id": [],
            "node_id": [],
        }

        query_counter = 0
        for route_pair in route_list_gdf.itertuples():
            # Pause every 100's route, to prevent overloading the routing server
            query_counter = 1 + query_counter
            if query_counter % 200 == 0:
                sleep(1)

            if query_counter % 1000 == 0:
                ic(verb, query_counter)

            _calculate_individual_route(
                route_pair, base_osrm_url, route_summary, verb, route_all_nodes
            )

        ic.enable()
        all_results[verb] = pd.DataFrame(route_all_nodes)
        ic(verb, all_results[verb].head())
        all_results[verb].to_csv(f"{results_dir}/{verb}.csv", index=False)

        reng.stop_routing_server()

    all_results_summary_df = pd.DataFrame(route_summary)
    all_results_summary_df.to_csv("{results_dir}/summary.csv")


def _calculate_individual_route(
    route_pair, base_osrm_url, route_summary, verb, route_all_nodes
):
    # route_osrm_url = f'{base_osrm_url}{route_pairs.start_long},{route_pairs.start_lat};{route_pairs.end_long},{route_pairs.end_lat}'
    # reverse the route
    forward_osrm_url = f"{base_osrm_url}{route_pair.start_long},{route_pair.start_lat};{route_pair.end_long},{route_pair.end_lat}"
    reverse_osrm_url = f"{base_osrm_url}{route_pair.end_long},{route_pair.end_lat};{route_pair.start_long},{route_pair.start_lat}"
    # ic(route_osrm_url)

    # ic(route_pairs.route_id)
    f_response = requests.get(forward_osrm_url, route_osrm_params)
    r_response = requests.get(reverse_osrm_url, route_osrm_params)
    # ic(response.content)
    f_route = json.loads(f_response.content)
    r_route = json.loads(r_response.content)

    # Force that either both the forward and reverse route suceed, or both fail
    # Don't a mix of one succeeding and one failing
    if (f_route["code"] == "Ok") and (r_route["code"] == "Ok"):
        _append_route_details(f_route, route_pair.route_id, verb, route_all_nodes)
        _append_route_details(r_route, -route_pair.route_id, verb, route_all_nodes)
    else:
        _append_failure_details(route_pair.route_id, route_summary, verb)
        _append_failure_details(-route_pair.route_id, route_summary, verb)


def _append_failure_details(route_id, route_summary, verb):
    route_summary["route_id"].append(route_id)
    route_summary["verb"].append(verb)
    route_summary["distance"].append(0)
    route_summary["duration"].append(0)
    route_summary["weight_name"].append("NoRoute")
    route_summary["weight"].append(0)


def _append_route_details(route, route_id, route_summary, verb, route_all_nodes):
    details = route["routes"][0]
    route_summary["route_id"].append(route_id)
    route_summary["verb"].append(verb)
    route_summary["distance"].append(details["distance"])
    route_summary["duration"].append(details["duration"])
    route_summary["weight_name"].append(details["weight_name"])
    route_summary["weight"].append(details["weight"])

    route_nodeids = []
    legs = details["legs"]
    for leg in legs:
        # ic(l['annotation']['nodes'])
        route_nodeids.extend(leg["annotation"]["nodes"])

    # ic(route_pairs.route_id, len(route_nodeids), route_pairs.straight_line_dist)
    # repeat the route id for all values
    route_all_nodes["route_id"].extend([route_id for x in route_nodeids])
    route_all_nodes["node_id"].extend(route_nodeids)
