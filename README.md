# Commission Math

Commission arithmetic. A tier rate applies to the slice, not the whole.

## What it computes

- **The flat truth** - one rate on all the sales: 5% of 50,000.00 is 2,500.00.
- **The tier truth** - one rate up to a threshold and another on the sales above it, each slice rounded to cents.
- **The target truth** - the least sales that earn a target commission at one rate, rounded up to the cent.

Money is rounded to cents, rates to hundredths of a percent, half up.

## Boundary

Arithmetic only. Commission Math does not know your plan's real terms, such as caps, accelerators, clawbacks or how sales are counted. Check those in your commission agreement.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (38 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/commissionmath/
Repo: https://github.com/iLanis-agent/commissionmath
