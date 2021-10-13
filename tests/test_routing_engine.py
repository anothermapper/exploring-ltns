from unittest import TestCase
import unittest
from icecream import ic
from src import docker_utils as docker
from src import set_parameters as sp


class TestRoutingEngine(TestCase):
    def setUp(self):
        self.city = sp.locality["Gosforth"]
        self.reng = docker.RoutingEngine(sp.transport_params, self.city)

    def test_get_osrm_filename(self):
        # Passing cases
        # Based on values from self.city
        self.assertEqual(self.reng._get_osrm_filename(), "tyne-and-wear-latest.osrm")
        self.assertEqual(self.reng._get_osrm_filename("a.osm.pbf"), "a.osrm")

        # Failing cases
        failing_cases = [
            ("a.pbf", "a.osrm"),
            ("a.osm", "a.osrm"),
            ("a.xml.osm.pbf", "a.osrm"),
            ("a.osm.xml.pbf", "a.osrm"),
        ]
        for test_val, expected_val in failing_cases:
            ic(test_val, expected_val)
            self.assertNotEqual(self.reng._get_osrm_filename(test_val), expected_val)

    @unittest.skip("Not ready yet")
    def test_stop_docker(self):
        # If reng._container_id is None, then `subprocess.run` should NOT be called

        # If reng._container_id is not None, then `subprocess.run` should be called
        # and `_container_id` should be contained in the cmd to `subprocess.run`.
        pass

    @unittest.skip("Not ready yet")
    def test_run_docker_background(self):
        # This command should raise a ValueError due to a lack of `--detach/-d` switch.
        # cmd = "abcde"
        pass

    @unittest.skip("Not ready yet")
    def test_run_docker_sync(self):
        pass

    @unittest.skip("Not ready yet")
    def test_run_routing_server(self):
        # Test if docker is alreay running?
        self.reng.run_routing_server("driving")
        self.reng.run_routing_server("cycling")
