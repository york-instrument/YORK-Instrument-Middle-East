"""Dew point, ppmV and ISO 8573-1 conversions for industrial gases.

Maintained by YORK Instrument - Middle East (https://www.yorkinstrument.ae/).
Same equations as the online calculators at https://www.yorkinstrument.ae/tools/.
"""

from .core import (
    ATM_BAR,
    enhancement_factor,
    saturation_vapor_pressure,
    dew_point_from_vapor_pressure,
    dew_point_to_ppmv,
    ppmv_to_dew_point,
    convert_dew_point,
    iso8573_water_class,
)

__all__ = [
    "ATM_BAR",
    "enhancement_factor",
    "saturation_vapor_pressure",
    "dew_point_from_vapor_pressure",
    "dew_point_to_ppmv",
    "ppmv_to_dew_point",
    "convert_dew_point",
    "iso8573_water_class",
]

__version__ = "0.1.0"
