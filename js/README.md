# york-dewpoint

Dew point, frost point, ppmV and pressure dew point conversions for industrial gases and compressed air, with the ISO 8573-1:2010 water class. Python and JavaScript, no dependencies, MIT licence.

Maintained by [YORK Instrument – Middle East](https://www.yorkinstrument.ae/), manufacturer of chilled mirror hygrometers, dew point transmitters and oxygen analyzers. The same equations run the online [dew point calculator](https://www.yorkinstrument.ae/tools/dew-point-calculator/), the [dew point to ppm table](https://www.yorkinstrument.ae/guides/dew-point-to-ppm/) and the [ISO 8573-1 air class checker](https://www.yorkinstrument.ae/tools/iso-8573-1-air-class/).

## Install

```bash
pip install york-dewpoint        # Python 3.9+
npm install york-dewpoint        # Node 18+ / browsers (ES module)
```

Or copy `src/york_dewpoint/core.py` or `js/york-dewpoint.mjs` into your project: each is one file.

## Quick start

```python
from york_dewpoint import ATM_BAR, dew_point_to_ppmv, ppmv_to_dew_point, convert_dew_point, iso8573_water_class

dew_point_to_ppmv(-40)                       # 126.7 ppmV  (frost point -40 °C at 1 atm)
ppmv_to_dew_point(127)                       # -40.0 °C

p = 7 + ATM_BAR                              # 7 bar(g) in bar(a)
dew_point_to_ppmv(-40, p)                    # 16.0 ppmV   (-40 °C pressure dew point)
convert_dew_point(-40, p)                    # -57.0 °C    same air expanded to 1 atm
iso8573_water_class(-40)                     # 2
```

```js
import { ATM_BAR, dewPointToPpmv, convertDewPoint, iso8573WaterClass } from 'york-dewpoint';

dewPointToPpmv(-40);                         // 126.7
convertDewPoint(-40, 7 + ATM_BAR);           // -57.0
iso8573WaterClass(-40);                      // 2
```

## Method

**Saturation vapour pressure** – Sonntag (1990), T in kelvin, result in Pa:

- over ice (used below 0 °C, i.e. frost point):
  `ln e = −6024.5282/T + 24.7219404 + 1.0613868×10⁻²·T − 1.3198825×10⁻⁵·T² − 0.49382577·ln T` (hPa, ×100 for Pa)
- over liquid water (0 °C and above, or `over_water=True`):
  `ln e = −6096.9385/T + 21.2409642 − 2.711193×10⁻²·T + 1.673952×10⁻⁵·T² + 2.433502·ln T`

**Water content** – ideal-gas mole fraction: `ppmV = 10⁶ · f · e(Td) / P`, with P the absolute pressure at which the dew point is measured.

**Enhancement factor f** – 1 by default. Set `enhancement=True` for the Buck (1996) factor, which matters at elevated pressure (about +4 % at 8 bar(a), −40 °C).

**Pressure dew point** – the water mole fraction does not change when gas is compressed or expanded, so a dew point at one pressure is converted by computing ppmV at that pressure and solving for the dew point at the other.

**ISO 8573-1:2010 water classes** – maximum pressure dew point: class 1 ≤ −70 °C, 2 ≤ −40 °C, 3 ≤ −20 °C, 4 ≤ +3 °C, 5 ≤ +7 °C, 6 ≤ +10 °C. Classes 7–9 are defined by liquid water content and are not covered.

### Frost point or dew point below 0 °C?

Below 0 °C this library returns the **frost point** (equilibrium over ice), which is what a chilled mirror hygrometer reads once the mirror deposit has frozen. Some polymer and metal-oxide sensors and some specifications report the dew point over **supercooled water**, which is lower for the same gas: 1,019 ppmV is −20.0 °C frost point but −22.3 °C dew point over water. Pass `over_water=True` (`{ overWater: true }` in JS) when you need the latter.

## Reference tables

Dew point at 1 atm (1.01325 bar(a)), ppmV, and the pressure dew point of the same gas at 7 bar(g):

| Dew point at 1 atm (°C) | ppmV | Pressure dew point at 7 bar(g) (°C) |
|---:|---:|---:|
| −100 | 0.0138 | −89.2 |
| −90 | 0.0954 | −77.9 |
| −80 | 0.54 | −66.6 |
| −70 | 2.58 | −55.1 |
| −60 | 10.7 | −43.5 |
| −50 | 38.8 | −31.9 |
| −40 | 126.7 | −20.2 |
| −30 | 375 | −8.4 |
| −20 | 1,019 | +4.1 |
| −10 | 2,565 | +17.9 |
| 0 | 6,032 | +32.3 |

ISO 8573-1 water classes for compressed air at 7 bar(g):

| ISO 8573-1 class | Max pressure dew point | ppmV | Same air at 1 atm (°C) |
|---|---:|---:|---:|
| 1 | −70 °C | 0.33 | −83.0 |
| 2 | −40 °C | 16.0 | −57.0 |
| 3 | −20 °C | 129 | −39.9 |
| 4 | +3 °C | 946 | −20.8 |
| 5 | +7 °C | 1,250 | −17.8 |
| 6 | +10 °C | 1,530 | −15.7 |

The full table from −100 to +20 °C, with a two-way calculator, is on [yorkinstrument.ae/guides/dew-point-to-ppm](https://www.yorkinstrument.ae/guides/dew-point-to-ppm/).

## Worked examples

1. **Desiccant dryer outlet.** A portable hygrometer at atmospheric pressure reads −57 °C on air sampled from a 7 bar(g) line. `convert_dew_point(-57, ATM_BAR, 7 + ATM_BAR)` gives −40.0 °C pressure dew point: ISO 8573-1 class 2.
2. **Natural gas at line pressure.** A −60 °C dew point at 50 bar(g) is `dew_point_to_ppmv(-60, 50 + ATM_BAR)` ≈ 0.21 ppmV. (For hydrocarbon gas at pipeline pressure, use a gas-specific method such as ISO 18453; see the [natural gas water content calculator](https://www.yorkinstrument.ae/tools/natural-gas-water-content/).)
3. **Instrument sample conditioning.** A sensor rated to 4 bar(g) sees a −40 °C dew point after a pressure reducer on a 50 bar(a) gas. Converted back to line conditions, `convert_dew_point(-40, 4 + ATM_BAR, 50)` ≈ −17.7 °C.

## Limits

- Ideal-gas mole fraction; adequate for air, nitrogen and other permanent gases up to tens of bar. For natural gas, CO₂ or SF₆ at high pressure use the gas-specific tools linked above.
- Valid from −150 to +100 °C. Results are engineering estimates, not a substitute for a calibrated measurement.

## Related

- [How to calibrate a dew point sensor](https://www.yorkinstrument.ae/guides/dew-point-sensor-calibration/)
- [Chilled mirror vs TDLAS vs metal-oxide moisture analyzers](https://www.yorkinstrument.ae/guides/chilled-mirror-vs-tdlas/)
- [Single-file offline calculators](https://github.com/york-instrument/YORK-Instrument-Middle-East/tree/main/calculators)

## References

- Sonntag, D. (1990). Important new values of the physical constants of 1986, vapour pressure formulations based on the ITS-90, and psychrometer formulae. *Z. Meteorol.* 40, 340–344.
- Buck, A. L. (1996). *Buck Research CR-1A User's Manual*, Appendix 1 (enhancement factors).
- ISO 8573-1:2010 Compressed air – Part 1: Contaminants and purity classes.

## Licence

MIT. Questions or errors: open an issue, or email dubai@yorkinstrument.com.
