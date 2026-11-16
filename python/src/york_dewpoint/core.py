"""Core equations.

Saturation vapour pressure: Sonntag (1990), over ice below 0 degC (frost point)
and over liquid water at and above 0 degC. Optional enhancement factor: Buck (1996).
These are the same equations used by the calculators on yorkinstrument.ae.

Conventions
-----------
* Temperatures in degC.
* Pressures in bar absolute (bar(a)). 1 atm = 1.01325 bar(a).
  To use gauge pressure, add ATM_BAR: p_abs = p_gauge + ATM_BAR.
* ppmV is the water vapour mole fraction x 1e6 (ideal gas).
"""

from __future__ import annotations

import math
from typing import Optional

ATM_BAR = 1.01325
_K = 273.15

# ISO 8573-1:2010 water classes 1-6, as maximum pressure dew point in degC.
_ISO8573_PDP_LIMITS = ((1, -70.0), (2, -40.0), (3, -20.0), (4, 3.0), (5, 7.0), (6, 10.0))


def _use_ice(t_c: float, over_water: bool) -> bool:
    return t_c < 0.0 and not over_water


def saturation_vapor_pressure(t_c: float, over_water: bool = False) -> float:
    """Saturation vapour pressure in Pa at temperature ``t_c`` (degC).

    Below 0 degC the value over ice is returned (frost point), unless
    ``over_water=True`` (supercooled water, e.g. for comparison with
    instruments that report dew point over water).
    """
    t = t_c + _K
    if _use_ice(t_c, over_water):
        # Sonntag 1990, over ice, hPa -> Pa
        return 100.0 * math.exp(
            -6024.5282 / t
            + 24.7219404
            + 1.0613868e-2 * t
            - 1.3198825e-5 * t * t
            - 0.49382577 * math.log(t)
        )
    # Sonntag 1990, over liquid water, Pa
    return math.exp(
        -6096.9385 / t
        + 21.2409642
        - 2.711193e-2 * t
        + 1.673952e-5 * t * t
        + 2.433502 * math.log(t)
    )


def enhancement_factor(p_bar: float, t_c: float, over_water: bool = False) -> float:
    """Buck (1996) enhancement factor for moist air at ``p_bar`` bar(a) and ``t_c`` degC."""
    h = p_bar * 1000.0  # bar -> hPa
    if _use_ice(t_c, over_water):
        return 1.0 + 1e-4 * (2.2 + h * (0.0383 + 6.4e-6 * t_c * t_c))
    return 1.0 + 1e-4 * (7.2 + h * (0.0320 + 5.9e-6 * t_c * t_c))


def _effective_vp(t_c: float, p_bar: float, over_water: bool, enhancement: bool) -> float:
    e = saturation_vapor_pressure(t_c, over_water)
    if enhancement:
        e *= enhancement_factor(p_bar, t_c, over_water)
    return e


def _solve_t(target_pa: float, p_bar: float, over_water: bool, enhancement: bool) -> float:
    """Temperature (degC) at which the effective vapour pressure equals ``target_pa``."""
    if target_pa <= 0:
        raise ValueError("vapour pressure must be positive")
    lo, hi = -150.0, 100.0
    if not (_effective_vp(lo, p_bar, over_water, enhancement) <= target_pa
            <= _effective_vp(hi, p_bar, over_water, enhancement)):
        raise ValueError("result outside -150 to +100 degC")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _effective_vp(mid, p_bar, over_water, enhancement) < target_pa:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-9:
            break
    return 0.5 * (lo + hi)


def dew_point_from_vapor_pressure(e_pa: float, over_water: bool = False) -> float:
    """Dew/frost point (degC) for a water vapour partial pressure in Pa (no enhancement)."""
    return _solve_t(e_pa, ATM_BAR, over_water, False)


def dew_point_to_ppmv(
    dew_point_c: float,
    p_bar: float = ATM_BAR,
    over_water: bool = False,
    enhancement: bool = False,
) -> float:
    """Water content in ppmV for a dew point ``dew_point_c`` measured at ``p_bar`` bar(a).

    >>> round(dew_point_to_ppmv(-40), 1)
    126.7
    """
    e = _effective_vp(dew_point_c, p_bar, over_water, enhancement)
    return e / (p_bar * 1e5) * 1e6


def ppmv_to_dew_point(
    ppmv: float,
    p_bar: float = ATM_BAR,
    over_water: bool = False,
    enhancement: bool = False,
) -> float:
    """Dew/frost point (degC) at ``p_bar`` bar(a) for a water content in ppmV.

    >>> round(ppmv_to_dew_point(127), 1)
    -40.0
    """
    if ppmv <= 0:
        raise ValueError("ppmV must be positive")
    target = ppmv * 1e-6 * p_bar * 1e5
    return _solve_t(target, p_bar, over_water, enhancement)


def convert_dew_point(
    dew_point_c: float,
    from_bar: float,
    to_bar: float = ATM_BAR,
    over_water: bool = False,
    enhancement: bool = False,
) -> float:
    """Convert a dew point measured at ``from_bar`` to the dew point at ``to_bar`` (both bar(a)).

    Water content (mole fraction) is constant, so only the dew point changes.

    >>> round(convert_dew_point(-40, 7 + ATM_BAR))   # -40 degC PDP at 7 bar(g)
    -57
    """
    ppm = dew_point_to_ppmv(dew_point_c, from_bar, over_water, enhancement)
    return ppmv_to_dew_point(ppm, to_bar, over_water, enhancement)


def iso8573_water_class(pressure_dew_point_c: float) -> Optional[int]:
    """ISO 8573-1:2010 water class (1-6) for a pressure dew point in degC.

    Returns ``None`` when the pressure dew point is above +10 degC (classes 7-9
    are defined by liquid water content, not dew point).
    """
    for cls, limit in _ISO8573_PDP_LIMITS:
        if pressure_dew_point_c <= limit:
            return cls
    return None
