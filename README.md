# Gas analysis engineering calculators

Free, single-file engineering calculators for moisture, dew point and oxygen measurement in industrial gases, natural gas, compressed air and SF₆ switchgear. Each calculator is one HTML file with no dependencies: open it in any browser, online or offline.

Maintained by [YORK Instrument – Middle East](https://www.yorkinstrument.ae/), manufacturer of dew point, moisture and oxygen analyzers. The online versions, with method notes and worked examples, are at **[yorkinstrument.ae/tools](https://www.yorkinstrument.ae/tools/)**.

## Calculators

| Calculator | What it does | Online version |
|---|---|---|
| [Dew point calculator](calculators/dew-point-calculator.html) | Converts pressure dew point to atmospheric dew point, ppmV, mg/m³ and lb/MMscf, with a pipe condensation check | [Open online](https://www.yorkinstrument.ae/tools/dew-point-calculator/) |
| [Natural gas water content](calculators/natural-gas-water-content.html) | Water dew point at line pressure ↔ lb/MMscf, mg/Sm³ and ppmV, checked against a pipeline specification | [Open online](https://www.yorkinstrument.ae/tools/natural-gas-water-content/) |
| [SF₆ moisture calculator](calculators/sf6-moisture-calculator.html) | SF₆ dew point to ppmV and mg/kg, dew point at filling pressure, IEC 60376 / IEC 60480 checks | [Open online](https://www.yorkinstrument.ae/tools/sf6-moisture-calculator/) |
| [ISO 8573-1 air class checker](calculators/iso-8573-1-air-class.html) | ISO 8573-1 water class of compressed air from a dew point reading at any pressure | [Open online](https://www.yorkinstrument.ae/tools/iso-8573-1-air-class/) |
| [Nitrogen purge calculator](calculators/nitrogen-purge-calculator.html) | Time, nitrogen volume and cost to purge a vessel or pipeline to a target O₂ (flow-through, pressure-cycle, pipeline) | [Open online](https://www.yorkinstrument.ae/tools/nitrogen-purge-calculator/) |
| [Hydrogen purity checker (ISO 14687)](calculators/hydrogen-purity-iso-14687.html) | Checks water, oxygen and other impurities against ISO 14687 Grade D for fuel-cell hydrogen | [Open online](https://www.yorkinstrument.ae/tools/hydrogen-purity-iso-14687/) |
| [Sample line response time](calculators/sample-line-response-time.html) | Transport time and T95 response of a gas sample line from tubing size, length, flow and pressure | [Open online](https://www.yorkinstrument.ae/tools/sample-line-response-time/) |
| [Moisture and oxygen unit converter](calculators/moisture-oxygen-unit-converter.html) | ppmV, ppmW, mg/m³, mg/Sm³, lb/MMscf and dew point; %, ppm, ppb and partial pressure for oxygen | [Open online](https://www.yorkinstrument.ae/tools/moisture-oxygen-unit-converter/) |
| [Analyzer selector](calculators/analyzer-selector.html) | Five questions to pick a moisture, oxygen or CO₂ analyzer type for an application | [Open online](https://www.yorkinstrument.ae/tools/analyzer-selector/) |

## Libraries for your own code

**[york-dewpoint](python/)** – the dew point equations behind these calculators as a small Python and JavaScript library (Sonntag 1990, optional Buck 1996 enhancement factor, ISO 8573-1 water class). No dependencies, unit-tested against the published tables.

```python
from york_dewpoint import dew_point_to_ppmv, convert_dew_point, ATM_BAR
dew_point_to_ppmv(-40)              # 126.7 ppmV at 1 atm
convert_dew_point(-40, 7 + ATM_BAR) # -57.0 °C: a -40 °C pressure dew point at 7 bar(g), expanded to 1 atm
```

Python: [`python/`](python/) · JavaScript: [`js/`](js/) · Method, reference tables and worked examples: [python/README.md](python/README.md)

## How to use

Download any `.html` file from the `calculators` folder and open it in a browser. Nothing is installed and no data leaves your computer.

## Methods and limits

The equations, assumptions and limits of each calculator are explained on its online page. Results are engineering estimates for planning and checking. They are not a substitute for a measurement, a project specification or a site safety procedure.

## Related guides

- [How to calibrate a dew point sensor](https://www.yorkinstrument.ae/guides/dew-point-sensor-calibration/)
- [Molecular sieve breakthrough and dryer outlet moisture](https://www.yorkinstrument.ae/guides/molecular-sieve-breakthrough/)
- [Chilled mirror vs TDLAS vs metal-oxide moisture analyzers](https://www.yorkinstrument.ae/guides/chilled-mirror-vs-tdlas/)

## Feedback

Found an error or want another calculator? Open an issue, or email dubai@yorkinstrument.com.

## Licence

MIT. See [LICENSE](LICENSE).
