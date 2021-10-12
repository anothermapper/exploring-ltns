from unittest import TestCase
from icecream import ic

from src import set_parameters as sp


class TestSetParameters(TestCase):
    def setUp(self):
        pass

    def test_key_directory_paths(self):
        ic(sp.download_dir)
        ic(sp.data_dir)
        ic(sp.results_dir)
        self.assertNotEqual(sp.download_dir, "downloads")
        self.assertGreater(len(sp.download_dir), len("downloads"))
        self.assertNotEqual(sp.data_dir, "data")
        self.assertGreater(len(sp.data_dir), len("data"))
        self.assertNotEqual(sp.results_dir, "results")
        self.assertGreater(len(sp.data_dir), len("results"))
