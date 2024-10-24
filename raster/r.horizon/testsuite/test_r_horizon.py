"""
TEST:    test_r_horizon.py

AUTHOR(S): Anna Petrasova <kratochanna at gmail>

PURPOSE:   Test r.horizon

COPYRIGHT: (C) 2015 Anna Petrasova

           This program is free software under the GNU General Public
           License (>=v2). Read the file COPYING that comes with GRASS
           for details.
"""

from grass.gunittest.case import TestCase
from grass.gunittest.main import test
from grass.gunittest.gmodules import SimpleModule


ref1 = """azimuth,horizon_height
180.000000,0.023101
"""

ref2 = """azimuth,horizon_height
180.000000,0.023101
200.000000,0.034850
220.000000,0.050549
240.000000,0.048211
260.000000,0.053101
280.000000,0.039774
300.000000,0.032360
320.000000,0.014804
340.000000,-0.001438
360.000000,0.004724
20.000000,0.012612
40.000000,0.015207
60.000000,0.014344
80.000000,0.011044
100.000000,0.012192
120.000000,0.007462
140.000000,0.004071
160.000000,0.015356
"""

ref3 = """azimuth,horizon_height
180.000000,0.023101
200.000000,0.034850
220.000000,0.050549
240.000000,0.048211
260.000000,0.053101
280.000000,0.039774
300.000000,0.032360
320.000000,0.014804
340.000000,-0.001438
360.000000,0.004724
20.000000,0.012612
40.000000,0.015207
60.000000,0.014344
80.000000,0.011044
100.000000,0.012192
120.000000,0.007462
140.000000,0.004071
160.000000,0.015356
"""


class TestHorizon(TestCase):
    horizon = "test_horizon_from_elevation"
    horizon_output = "test_horizon_output_from_elevation"

    @classmethod
    def setUpClass(cls):
        cls.use_temp_region()
        cls.runModule("g.region", raster="elevation")

    @classmethod
    def tearDownClass(cls):
        cls.del_temp_region()

    def tearDown(self):
        """Remove horizon map after each test method"""
        self.runModule("g.remove", flags="f", type="raster", name=self.horizon)
        self.runModule(
            "g.remove", flags="f", type="raster", pattern=self.horizon_output + "*"
        )

    def test_point_mode_one_direction(self):
        """Test mode with 1 point and 1 direction"""
        module = SimpleModule(
            "r.horizon",
            elevation="elevation",
            coordinates=(634720, 216180),
            output=self.horizon,
            direction=180,
            step=0,
        )
        self.assertModule(module)
        stdout = module.outputs.stdout
        self.assertMultiLineEqual(first=ref1, second=stdout)

    def test_point_mode_multiple_direction(self):
        """Test mode with 1 point and multiple directions"""
        module = SimpleModule(
            "r.horizon",
            elevation="elevation",
            coordinates=(634720, 216180),
            output=self.horizon,
            direction=180,
            step=20,
        )
        self.assertModule(module)
        stdout = module.outputs.stdout
        self.assertMultiLineEqual(first=ref2, second=stdout)

    def test_raster_mode_one_direction(self):
        """Test mode with 1 point and one direction"""
        module = SimpleModule(
            "r.horizon", elevation="elevation", output=self.horizon_output, direction=50
        )
        self.assertModule(module)
        ref = {
            "min": -1.57079637050629,
            "max": 0.70678365230560,
            "stddev": 0.0708080140468585,
        }
        self.assertRasterFitsUnivar(
            raster="test_horizon_output_from_elevation_050",
            reference=ref,
            precision=1e6,
        )

    def test_raster_mode_multiple_direction(self):
        module = SimpleModule(
            "r.horizon",
            elevation="elevation",
            output=self.horizon_output,
            start=10,
            end=50,
            step=15.512,
        )
        self.assertModule(module)
        module_list = SimpleModule(
            "g.list", type="raster", pattern=self.horizon_output + "*"
        )
        self.runModule(module_list)
        stdout = module_list.outputs.stdout.strip()
        self.assertMultiLineEqual(
            first="test_horizon_output_from_elevation_010_000\ntest_horizon_output_from_elevation_025_512",
            second=stdout,
        )

    def test_raster_mode_multiple_direction_offset(self):
        module = SimpleModule(
            "r.horizon",
            elevation="elevation",
            output=self.horizon_output,
            start=10,
            end=50,
            step=15.512,
            direction=80,
        )
        self.assertModule(module)
        module_list = SimpleModule(
            "g.list", type="raster", pattern=self.horizon_output + "*"
        )
        self.runModule(module_list)
        stdout = module_list.outputs.stdout.strip()
        self.assertMultiLineEqual(
            first="test_horizon_output_from_elevation_090_000\ntest_horizon_output_from_elevation_105_512",
            second=stdout,
        )


if __name__ == "__main__":
    test()
