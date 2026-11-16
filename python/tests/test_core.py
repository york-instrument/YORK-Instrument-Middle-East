"""Reference values: Sonntag (1990) at 1.01325 bar(a), as published on
https://www.yorkinstrument.ae/guides/dew-point-to-ppm/ (7 bar(g) table)."""

import math
import unittest

from york_dewpoint import (
    ATM_BAR,
    convert_dew_point,
    dew_point_to_ppmv,
    iso8573_water_class,
    ppmv_to_dew_point,
    saturation_vapor_pressure,
)

P7G = 7 + ATM_BAR


class SaturationPressure(unittest.TestCase):
    def test_triple_point(self):
        # Both branches give ~611.2 Pa at 0 degC
        self.assertAlmostEqual(saturation_vapor_pressure(0.0), 611.2, delta=0.5)
        self.assertAlmostEqual(saturation_vapor_pressure(-1e-9), 611.2, delta=0.5)

    def test_boiling_point(self):
        self.assertAlmostEqual(saturation_vapor_pressure(100.0), 101325, delta=200)

    def test_ice_below_water(self):
        self.assertLess(saturation_vapor_pressure(-20), saturation_vapor_pressure(-20, over_water=True))


class Ppmv(unittest.TestCase):
    def test_minus40(self):
        self.assertAlmostEqual(dew_point_to_ppmv(-40), 126.7, delta=0.05)

    def test_inverse(self):
        self.assertAlmostEqual(ppmv_to_dew_point(127), -40.0, delta=0.05)

    def test_round_trip(self):
        for dp in (-100, -80, -60, -40, -20, -1, 0, 5, 20):
            for p in (ATM_BAR, P7G, 50.0):
                ppm = dew_point_to_ppmv(dp, p)
                self.assertAlmostEqual(ppmv_to_dew_point(ppm, p), dp, places=6)

    def test_pressure_reduces_ppmv(self):
        self.assertAlmostEqual(dew_point_to_ppmv(-40, P7G), 16.0, delta=0.05)


class PressureDewPoint(unittest.TestCase):
    # ISO 8573-1 class limits at 7 bar(g) -> atmospheric dew point
    def test_table(self):
        for pdp, atm in ((-70, -83.0), (-40, -57.0), (-20, -39.9), (3, -20.8)):
            self.assertAlmostEqual(convert_dew_point(pdp, P7G), atm, delta=0.1)

    def test_enhancement_increases_ppmv(self):
        self.assertGreater(dew_point_to_ppmv(-40, P7G, enhancement=True), dew_point_to_ppmv(-40, P7G))


class Iso8573(unittest.TestCase):
    def test_classes(self):
        self.assertEqual(iso8573_water_class(-75), 1)
        self.assertEqual(iso8573_water_class(-70), 1)
        self.assertEqual(iso8573_water_class(-40), 2)
        self.assertEqual(iso8573_water_class(-25), 3)
        self.assertEqual(iso8573_water_class(3), 4)
        self.assertEqual(iso8573_water_class(5), 5)
        self.assertEqual(iso8573_water_class(10), 6)
        self.assertIsNone(iso8573_water_class(12))


class Errors(unittest.TestCase):
    def test_bad_ppmv(self):
        with self.assertRaises(ValueError):
            ppmv_to_dew_point(0)
        self.assertTrue(math.isfinite(ppmv_to_dew_point(1e-3)))


if __name__ == "__main__":
    unittest.main()
