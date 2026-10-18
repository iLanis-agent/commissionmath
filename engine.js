// Commission Math engine - flat commission, a two-tier split at a threshold, and the sales a target needs.
// Mirrored by oracle.py; keep the op order identical.
// Money is rounded to cents and rates to hundredths of a percent on the way in. Rounding is half up.

function _c(x, msg, max, allowZero) {
  if (typeof x !== "number" || !isFinite(x) || x < 0 || x > max || (!allowZero && x === 0)) throw new Error(msg);
  return Math.floor(x * 100 + 0.5);
}

function _fmt(h) {
  var whole = Math.floor(h / 100), frac = h % 100;
  if (frac === 0) return String(whole);
  var f = (frac < 10 ? "0" : "") + frac;
  if (f.charAt(1) === "0") f = f.charAt(0);
  return whole + "." + f;
}

function _money(c) {
  var whole = String(Math.floor(c / 100)), frac = c % 100;
  var out = "";
  while (whole.length > 3) { out = "," + whole.slice(-3) + out; whole = whole.slice(0, -3); }
  return whole + out + "." + (frac < 10 ? "0" : "") + frac;
}

// cents times a rate in hundredths of a percent, rounded half up to cents.
function _part(cents, rate) {
  return Math.floor((2 * cents * rate + 10000) / 20000);
}

var MAXM = 100000000;

// The flat truth: one rate on all the sales.
function flatTruth(sales, rate) {
  var s = _c(sales, "sales must be between 0 and 100000000", MAXM, true);
  var r = _c(rate, "rate must be between 0 and 100", 100, true);
  return "Commission on " + _money(s) + " of sales at " + _fmt(r) + "%: " + _money(_part(s, r)) + ".";
}

// The tier truth: one rate up to a threshold, another rate on the sales above it.
function tierTruth(sales, threshold, lowRate, highRate) {
  var s = _c(sales, "sales must be between 0 and 100000000", MAXM, true);
  var t = _c(threshold, "threshold must be above 0 and at most 100000000", MAXM, false);
  var lo = _c(lowRate, "rate below the threshold must be between 0 and 100", 100, true);
  var hi = _c(highRate, "rate above the threshold must be between 0 and 100", 100, true);
  if (s <= t) {
    return "All " + _money(s) + " is at or under the " + _money(t) + " threshold: " + _fmt(lo) + "% gives " + _money(_part(s, lo)) + ".";
  }
  var a = _part(t, lo), b = _part(s - t, hi);
  return _fmt(lo) + "% on the first " + _money(t) + " is " + _money(a) + "; " + _fmt(hi) + "% on the other " + _money(s - t) + " is " + _money(b) + "; total " + _money(a + b) + ".";
}

// The target truth: the least sales that earn a target commission at one rate.
function targetTruth(target, rate) {
  var g = _c(target, "target commission must be between 0 and 100000000", MAXM, true);
  var r = _c(rate, "rate must be above 0 and at most 100", 100, false);
  var s = 0;
  if (g > 0) {
    var n = 10000 * g;
    s = (n - (n % r)) / r + (n % r > 0 ? 1 : 0);
  }
  return "To earn " + _money(g) + " at " + _fmt(r) + "%, sales of " + _money(s) + " are needed.";
}
