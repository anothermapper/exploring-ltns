import overpy
import pandas as pd
import geopandas
from icecream import ic
import requests
from osgeo import ogr
import gdal
import os

import download_utils as du
from set_parameters import crs_long_lat, data_dir, download_dir

# Get URLs to download OSM data from Geofabrik
ic.enable()

_overpass_url = "http://overpass-api.de/api/interpreter?"
street_nodes_fpath = f"{data_dir}/street_nodes.gpkg"
street_nodes_lyr_name = "street_nodes"
landuse_fpath = f"{data_dir}/landuse.gpkg"
landuse_lyr_name = "landuse"


def download_latest_osm_file(city):
    osm_fname = city["osm_fname"]
    nation = city["nation"]
    osm_download_url = (
        f"https://download.geofabrik.de/europe/great-britain/{nation}/{osm_fname}"
    )
    osm_lastest_md5sum_url = (
        f"https://download.geofabrik.de/europe/great-britain/{nation}/{osm_fname}.md5"
    )
    du.download_latest_file(osm_download_url, osm_fname, osm_lastest_md5sum_url)


def _get_bounding_box_lat_long(aoi_gdf):
    # Make a tempory copy of the AOI
    aoi_latlong = aoi_gdf.copy()
    # Reproject it into Lat,Long
    aoi_latlong = aoi_latlong.to_crs(crs_long_lat)
    bbox = aoi_latlong.total_bounds
    # GeoFrameFrame report Long, Lat
    # Overpass requires Lat, Long - joy!
    lats = bbox[1], bbox[3]
    longs = bbox[0], bbox[2]
    ic(lats)
    ic(longs)
    return f"( {min(lats)}, {min(longs)}, {max(lats)}, {max(longs)})"


def _get_point_data_from_overpass(overpass_query, output_fpath, output_lyr_name):
    api = overpy.Overpass()
    # fetch all ways and nodes
    result = api.query(overpass_query)
    ic(result)
    ic(len(result.nodes))
    ic(result.nodes[0])

    coords_list = {
        "id": [n.id for n in result.nodes],
        "lon": [n.lon for n in result.nodes],
        "lat": [n.lat for n in result.nodes],
    }

    temp_df = pd.DataFrame(coords_list)
    ic(temp_df.head())
    ic(temp_df.dtypes)

    point_gdf = geopandas.GeoDataFrame(
        temp_df.id,
        crs=crs_long_lat,
        geometry=geopandas.points_from_xy(temp_df.lon, temp_df.lat),
    )
    ic(point_gdf.head())
    ic(point_gdf.dtypes)

    point_gdf.to_file(output_fpath, driver="GPKG", layer=output_lyr_name)


def _get_polygon_data_from_overpass(overpass_query, output_fpath, output_lyr_name):
    """
    Unfortuantly there doesn't seem to be a way to load a XML string directly with OGR.
    As a results a the least-worst way to do this is to:
    1) Get the data directly using requests.
    2) Save it as a tempory XML file.
    3) Open the XML file using OGR.
    4) Save the data as a GPKG (which we actually want) using OGR.
    """
    # Get the data directly using requests
    chunk_size = 1024
    parameters = {"data": overpass_query}
    response = requests.get(_overpass_url, stream=True, params=parameters)
    ic(response)
    response.raise_for_status()

    # Save it as an XML file
    xml_path = f"{download_dir}/{output_lyr_name}.xml"
    with open(xml_path, "wb") as xml_fb:
        for chunk in response.iter_content(chunk_size=chunk_size):
            xml_fb.write(chunk)

    # Open the XML file using OGR
    in_ds = ogr.Open(xml_path)

    # Save the data as a GPKG using OGR.
    out_driver = ogr.GetDriverByName("GPKG")
    gdal.SetConfigOption("OSM_USE_CUSTOM_INDEXING", "NO")
    # Delete if previously exists
    if os.path.exists(output_fpath):
        out_driver.DeleteDataSource(output_fpath)

    out_ds = out_driver.CreateDataSource(output_fpath)
    in_lyr = in_ds.GetLayerByName("multipolygons")
    out_lyr = out_ds.CopyLayer(
        in_lyr, output_lyr_name, options=["OVERWRITE=YES", "ENCODING=UTF-8"]
    )
    out_lyr.SyncToDisk()


def download_street_nodes(aoi_gdf):
    bbox_str = _get_bounding_box_lat_long(aoi_gdf)

    # We require the nodes for each streets (eg the individual points that make
    # up the street, not the lines of the streets themselves). The extra nested
    # level on the overpass query achieves this.
    streets_node_query = f"""[timeout:25][out:xml];
    (
        way["highway"]{bbox_str};
        relation["highway"]{bbox_str};
    );
    (
        node(w);
        node(r);
    );
    out;"""

    _get_point_data_from_overpass(
        streets_node_query, street_nodes_fpath, street_nodes_lyr_name
    )


def open_street_nodes():
    return geopandas.read_file(street_nodes_fpath, layer=street_nodes_lyr_name)


def download_landuse(aoi_gdf):
    bbox_str = _get_bounding_box_lat_long(aoi_gdf)

    residential_landuse_query = f"""[out:xml] [timeout:25];
    (
        node["landuse"="residential"]{bbox_str};
        way["landuse"="residential"]{bbox_str};
        relation["landuse"="residential"]{bbox_str};
    );
    (._;>;);
    out body;
    """

    _get_polygon_data_from_overpass(
        residential_landuse_query, landuse_fpath, landuse_lyr_name
    )


def open_landuse():
    return geopandas.read_file(landuse_fpath, layer=landuse_lyr_name)
