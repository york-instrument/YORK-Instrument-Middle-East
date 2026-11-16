// Dew point, ppmV and ISO 8573-1 conversions for industrial gases.
// Maintained by YORK Instrument - Middle East - https://www.yorkinstrument.ae/tools/
// Sonntag (1990) saturation vapour pressure (over ice below 0 degC unless overWater),
// optional Buck (1996) enhancement factor. Temperatures in degC, pressures in bar(a).
// MIT licence.

export const ATM_BAR = 1.01325;
const K = 273.15;
const ISO8573 = [[1, -70], [2, -40], [3, -20], [4, 3], [5, 7], [6, 10]];

const useIce = (t, overWater) => t < 0 && !overWater;

/** Saturation vapour pressure in Pa. */
export function saturationVaporPressure(tC, overWater = false) {
  const T = tC + K;
  if (useIce(tC, overWater)) {
    return 100 * Math.exp(-6024.5282 / T + 24.7219404 + 1.0613868e-2 * T
      - 1.3198825e-5 * T * T - 0.49382577 * Math.log(T));
  }
  return Math.exp(-6096.9385 / T + 21.2409642 - 2.711193e-2 * T
    + 1.673952e-5 * T * T + 2.433502 * Math.log(T));
}

/** Buck (1996) enhancement factor at pBar bar(a). */
export function enhancementFactor(pBar, tC, overWater = false) {
  const h = pBar * 1000;
  return useIce(tC, overWater)
    ? 1 + 1e-4 * (2.2 + h * (0.0383 + 6.4e-6 * tC * tC))
    : 1 + 1e-4 * (7.2 + h * (0.0320 + 5.9e-6 * tC * tC));
}

function effVp(t, p, overWater, enh) {
  const e = saturationVaporPressure(t, overWater);
  return enh ? e * enhancementFactor(p, t, overWater) : e;
}

function solveT(target, p, overWater, enh) {
  if (!(target > 0)) throw new RangeError('vapour pressure must be positive');
  let lo = -150, hi = 100;
  if (effVp(lo, p, overWater, enh) > target || effVp(hi, p, overWater, enh) < target) {
    throw new RangeError('result outside -150 to +100 degC');
  }
  for (let i = 0; i < 200 && hi - lo > 1e-9; i++) {
    const mid = (lo + hi) / 2;
    if (effVp(mid, p, overWater, enh) < target) lo = mid; else hi = mid;
  }
  return (lo + hi) / 2;
}

/** Water content (ppmV) for a dew point measured at pBar bar(a). */
export function dewPointToPpmv(dpC, pBar = ATM_BAR, { overWater = false, enhancement = false } = {}) {
  return effVp(dpC, pBar, overWater, enhancement) / (pBar * 1e5) * 1e6;
}

/** Dew/frost point (degC) at pBar bar(a) for a water content in ppmV. */
export function ppmvToDewPoint(ppmv, pBar = ATM_BAR, { overWater = false, enhancement = false } = {}) {
  if (!(ppmv > 0)) throw new RangeError('ppmV must be positive');
  return solveT(ppmv * 1e-6 * pBar * 1e5, pBar, overWater, enhancement);
}

/** Convert a dew point measured at fromBar to the dew point at toBar (bar(a)). */
export function convertDewPoint(dpC, fromBar, toBar = ATM_BAR, opts = {}) {
  return ppmvToDewPoint(dewPointToPpmv(dpC, fromBar, opts), toBar, opts);
}

/** ISO 8573-1:2010 water class (1-6) for a pressure dew point, or null above +10 degC. */
export function iso8573WaterClass(pdpC) {
  for (const [cls, lim] of ISO8573) if (pdpC <= lim) return cls;
  return null;
}
