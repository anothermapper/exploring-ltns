import shutil
import geopandas
import pandas as pd
from icecream import ic

from download_utils import download_latest_file
from set_parameters import download_dir, data_dir, crs_bng

ic.enable()

boundaries_file = f"{data_dir}/boundaries/data/bdline_gb.gpkg"
_boundaries_download_url = "https://api.os.uk/downloads/v1/products/BoundaryLine/downloads?area=GB&format=GeoPackage&redirect"
_boundaries_zip_file = "bdline_gpkg_gb.zip"
_boundaries_layer = "district_borough_unitary_ward"
_address_download_url = "https://api.os.uk/downloads/v1/products/OpenUPRN/downloads?area=GB&format=CSV&redirect"
_address_zip_fpath = f"{download_dir}/uprn_address.zip"
address_lyr_name = "uprn_address"
address_fpath = f"{data_dir}/uprn_address.gpkg"
aoi_fpath = f"{data_dir}/area_of_interest.gpkg"
aoi_layer_name = "area_of_interest"


def download_boundaries_file():
    download_latest_file(_boundaries_download_url, _boundaries_zip_file)


def _unzip_file(source_zip, destination_dir):
    shutil.unpack_archive(source_zip, destination_dir)


def create_aoi_from_boundaries_file(city):
    _unzip_file(f"{download_dir}/{_boundaries_zip_file}", f"{data_dir}/boundaries")
    all_wards = geopandas.read_file(boundaries_file, layer=_boundaries_layer)
    ic(city["city_name"])
    aoi_wards_gdf = all_wards[all_wards["File_Name"].isin([city["city_name"]])]
    ic(len(aoi_wards_gdf))
    aoi_wards_gdf = aoi_wards_gdf[aoi_wards_gdf["Name"].isin(city["ward_list"])]
    ic(len(aoi_wards_gdf))
    aoi_wards_gdf.to_file(aoi_fpath, driver="GPKG", layer=aoi_layer_name)


def open_aoi():
    return geopandas.read_file(aoi_fpath, layer=aoi_layer_name)


def download_address_point_file():
    download_latest_file(_address_download_url, _address_zip_fpath)


def create_address_aoi(aoi_gdf):
    ic.enable()
    # aoi_osopenuprn_path = 'osopenuprn_202108_csv/aoi_uprn.shp'
    ic("unzipping address file")
    _unzip_file(_address_zip_fpath, download_dir)

    _address_csv_fpath = f"{download_dir}/osopenuprn_202107.csv"
    csv_df = pd.read_csv(_address_csv_fpath)
    ic(len(csv_df))
    ic(csv_df.head())
    x_min, y_min, x_max, y_max = aoi_gdf.copy().to_crs(crs_bng).total_bounds

    # Crude clip for speed. In fact clipping to the bounding box if sufficent. There is no need to clip to the exact
    # outline of the AOI.
    # clip north/south first, then east/west
    csv_df = csv_df[(csv_df.Y_COORDINATE > y_min) & (csv_df.Y_COORDINATE < y_max)]
    ic(len(csv_df))
    csv_df = csv_df[(csv_df.X_COORDINATE > x_min) & (csv_df.X_COORDINATE < x_max)]
    ic(len(csv_df))

    aoi_uprn_gdf = geopandas.GeoDataFrame(
        csv_df,
        crs=crs_bng,
        geometry=geopandas.points_from_xy(csv_df.X_COORDINATE, csv_df.Y_COORDINATE),
    )
    ic(len(aoi_uprn_gdf))
    ic(aoi_uprn_gdf.head())
    aoi_uprn_gdf.to_file(address_fpath, driver="GPKG", layer=address_lyr_name)


def open_address_points():
    return geopandas.read_file(address_fpath, layer=address_lyr_name)
