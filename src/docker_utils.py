import subprocess
import shutil
from pathlib import Path
from icecream import ic
from src import set_parameters as sp
from time import sleep


class RoutingEngine:
    def __init__(self, transport_params, city) -> None:
        self.transport_params = transport_params
        self.city = city
        self._container_id = None

    def _run_docker_sync(self, cmd_str):
        """
        Runs a docker command synchronisly.
        returns the exist code of the command
        """
        ic(cmd_str)
        cmd_ary = cmd_str.split()
        subprocess.run(cmd_ary, check=True)

    def _run_docker_background(self, cmd_str):
        """
        Runs a docker command synchronisly.
        returns the CONTAINER ID
        """
        # `-d` arg
        ic(cmd_str)
        if (" -d " not in cmd_str) and ("--detach" not in cmd_str):
            raise ValueError(
                "Docker command called as background process, but does not include the `--detach/-d` switch. Command=`{cmd_str}"
            )

        cmd_ary = cmd_str.split()

        completed_process = subprocess.run(cmd_ary, check=True)
        # Allow at five secounds for the OSRM to start
        sleep(5)
        completed_process.check_returncode()
        self._container_id = completed_process.stdout
        ic(self._container_id)

    def stop_routing_server(self):
        if self._container_id:
            cmd_stop = f"docker stop {self._container_id}"
            self._run_docker_sync(cmd_stop)
            self._container_id = None

    def _copy_routing_data(self, osm_dir, osm_fname):
        if not Path(osm_dir).exists():
            Path(osm_dir).mkdir(parents=True)

        shutil.copyfile(f"{sp.download_dir}/{osm_fname}", f"{osm_dir}/{osm_fname}")

    def _get_osrm_filename(self, osm_fname=None):
        if not osm_fname:
            osm_fname = self.city["osm_fname"]
        base_fname = osm_fname.removesuffix(".osm.pbf")
        return f"{base_fname}.osrm"

    def preprocess_routing_data(self):

        for verb, t_params in self.transport_params.items():
            data_path = t_params["data_path"]
            profile_path = t_params["osrm_profile"]
            # Use `map` and `route` as prefixes here becuase `osm` and `osrm` look too simular
            map_fname = self.city["osm_fname"]
            route_fname = self._get_osrm_filename(map_fname)
            ic(verb, data_path, profile_path, map_fname, route_fname)

            self._copy_routing_data(data_path, map_fname)

            cmd_extract = f'docker run -t -v "{data_path}:/data" osrm/osrm-backend osrm-extract -p {profile_path} /data/{map_fname}'
            cmd_partition = f'docker run -t -v "{data_path}:/data" osrm/osrm-backend osrm-partition /data/{route_fname}'
            cmd_customize = f'docker run -t -v "{data_path}:/data" osrm/osrm-backend osrm-customize /data/{route_fname}'
            self._run_docker_sync(cmd_extract)
            self._run_docker_sync(cmd_partition)
            self._run_docker_sync(cmd_customize)

    def run_routing_server(self, verb):
        data_path = self.transport_params[verb]["data_path"]
        # Use `map` and `route` as prefixes here becuase `osm` and `osrm` look too simular
        map_fname = self.city["osm_fname"]
        route_fname = self._get_osrm_filename(map_fname)

        cmd = f'docker run --detach -t -i -p 5000:5000 -v "{data_path}:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/{route_fname}'
        self._run_docker_background(cmd)
