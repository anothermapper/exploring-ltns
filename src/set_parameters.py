from pathlib import Path

# Well known indentifers for the two coordinate systems used here.
# Unprojected, WGS1984, Long, Lat - This is required by the routing engine
# Projected, British National Grid - A projected coordinate system is required for
# distance calculations and BNG is an appropriate choice
crs_long_lat = "EPSG:4326"
crs_bng = "EPSG:27700"

# Directory Structure
_root_dir = Path(__file__).parent.parent
download_dir = str(_root_dir.joinpath("downloads"))
data_dir = str(_root_dir.joinpath("data"))
results_dir = str(_root_dir.joinpath("results"))

# Different transport types
transport_params = {
    "driving": {"data_path": f"{data_dir}/osm/car", "osrm_profile": "/opt/car.lua"},
    "cycling": {
        "data_path": f"{data_dir}/osm/bike",
        "osrm_profile": "/opt/bicycle.lua",
    },
    "walking": {"data_path": f"{data_dir}/osm/walk", "osrm_profile": "/opt/foot.lua"},
}


locality = {
    "Gosforth": {
        "osm_fname": "tyne-and-wear-latest.osm.pbf",
        "nation": "england",
        "city_name": "NEWCASTLE_UPON_TYNE_DISTRICT_(B)",
        "ward_list": [
            "Kenton Ward",
            "Parklands Ward",
            "Dene & South Gosforth Ward",
            "Fawdon & West Gosforth Ward",
            "North Jesmond Ward",
            "Gosforth Ward",
        ],
    },
    "Oxford": {
        "osm_fname": "oxfordshire-latest.osm.pbf",
        "nation": "england",
        "city_name": "OXFORDSHIRE_COUNTY",
        "ward_list": [
            "Botley & Sunningwell Ward",
            "Walton Manor Ward",
            "Hinksey Park Ward",
            "Lye Valley Ward",
            "Wolvercote Ward",
            "Barton & Sandhills Ward",
            "Holywell Ward",
            "Littlemore Ward",
            "Rose Hill & Iffley Ward",
            "St. Clement's Ward",
            "Churchill Ward",
            "Quarry & Risinghurst Ward",
            "Marston Ward",
            "Headington Hill & Northway Ward",
            "St. Mary's Ward",
            "Osney & St Thomas Ward",
            "Headington Ward",
            "Summertown Ward",
            "Carfax & Jericho Ward",
            "Temple Cowley Ward",
            "Cowley Ward",
            "Cutteslowe & Sunnymead Ward",
            "Donnington Ward",
        ],
    },
}
