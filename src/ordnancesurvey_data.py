import os
import shutil
import geopandas
from icecream import ic

from download_utils import download_latest_file
from set_parameters import download_dir, data_dir

ic.enable()

boundaries_file = f"{data_dir}/boundaries/data/bdline_gb.gpkg"
_boundaries_download_url = "https://api.os.uk/downloads/v1/products/BoundaryLine/downloads?area=GB&format=GeoPackage&redirect"
_boundaries_zip_file = "bdline_gpkg_gb.zip"
_boundaries_layer = 'district_borough_unitary_ward'
aoi_fpath = f"{data_dir}/area_of_interest.gpkg"
aoi_layer_name = "area_of_interest"


def download_boundaries_file():
    download_latest_file(_boundaries_download_url, _boundaries_zip_file)


def _unzip_boundaries_file():
    if not os.path.exists(boundaries_file):
        shutil.unpack_archive(
            f"{download_dir}/{_boundaries_zip_file}", f"{data_dir}/boundaries"
        )


def create_aoi_from_boundaries_file(city):
    _unzip_boundaries_file()
    all_wards = geopandas.read_file(boundaries_file, layer=_boundaries_layer)
    ic(city['city_name'])
    aoi_wards_gdf = all_wards[all_wards['File_Name'].isin([city['city_name']])]
    ic(len(aoi_wards_gdf))
    aoi_wards_gdf = aoi_wards_gdf[aoi_wards_gdf['Name'].isin(city['ward_list'])]
    ic(len(aoi_wards_gdf))
    aoi_wards_gdf.to_file(aoi_fpath, driver='GPKG', layer=aoi_layer_name)


def open_aoi():
    return geopandas.read_file(aoi_fpath, layer=aoi_layer_name)
