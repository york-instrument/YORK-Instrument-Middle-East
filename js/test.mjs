import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { ATM_BAR, dewPointToPpmv, ppmvToDewPoint, convertDewPoint, iso8573WaterClass, saturationVaporPressure } from './york-dewpoint.mjs';

const P7G = 7 + ATM_BAR;
const near = (a, b, d) => assert.ok(Math.abs(a - b) <= d, `${a} not within ${d} of ${b}`);

test('triple point', () => near(saturationVaporPressure(0), 611.2, 0.5));
test('-40 degC = 126.7 ppmV', () => near(dewPointToPpmv(-40), 126.7, 0.05));
test('127 ppmV = -40.0 degC', () => near(ppmvToDewPoint(127), -40, 0.05));
test('round trip', () => {
  for (const dp of [-100, -60, -20, 0, 20]) for (const p of [ATM_BAR, P7G, 50]) {
    near(ppmvToDewPoint(dewPointToPpmv(dp, p), p), dp, 1e-6);
  }
});
test('7 bar(g) table', () => {
  for (const [pdp, atm] of [[-70, -83.0], [-40, -57.0], [-20, -39.9], [3, -20.8]]) near(convertDewPoint(pdp, P7G), atm, 0.1);
});
test('ISO 8573-1 classes', () => {
  assert.equal(iso8573WaterClass(-70), 1);
  assert.equal(iso8573WaterClass(-40), 2);
  assert.equal(iso8573WaterClass(3), 4);
  assert.equal(iso8573WaterClass(12), null);
});
