let V_out = 3.3;
let V_supply = 30;
let scale = 1e3; // scale resistance range for R2 (e.g. 1000 places it in the kOhm range)
let useE96 = false; // set true if 1% (otherwise 5% tolerance)
let maxResults = 3; // gets the top n results

console.table(getResistanceValues(V_out, V_supply, scale, useE96, maxResults));


function getResistanceValues(_vOut, _vSupply, _scale, _useE96, _maxResults) {
    let ratio_V_target = _vOut / _vSupply;
    let logk = (Math.log10(ratio_V_target / (1 - ratio_V_target)));

    const e24 = [
        1.0, 1.1, 1.2, 1.3, 1.5, 1.6,
        1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
        3.3, 3.6, 3.9, 4.3, 4.7, 5.1,
        5.6, 6.2, 6.8, 7.5, 8.2, 9.1,
    ];
    const e96 = [
        1.00, 1.02, 1.05, 1.07, 1.10, 1.13,
        1.15, 1.18, 1.21, 1.24, 1.27, 1.30,
        1.33, 1.37, 1.40, 1.43, 1.47, 1.50,
        1.54, 1.58, 1.62, 1.65, 1.69, 1.74,
        1.78, 1.82, 1.87, 1.91, 1.96, 2.00,
        2.05, 2.10, 2.15, 2.21, 2.26, 2.32,
        2.37, 2.43, 2.49, 2.55, 2.61, 2.67,
        2.74, 2.80, 2.87, 2.94, 3.01, 3.09,
        3.16, 3.24, 3.32, 3.40, 3.48, 3.57,
        3.65, 3.74, 3.83, 3.92, 4.02, 4.12,
        4.22, 4.32, 4.42, 4.53, 4.64, 4.75,
        4.87, 4.99, 5.11, 5.23, 5.36, 5.49,
        5.62, 5.76, 5.90, 6.04, 6.19, 6.34,
        6.49, 6.65, 6.81, 6.98, 7.15, 7.32,
        7.50, 7.68, 7.87, 8.06, 8.25, 8.45,
        8.66, 8.87, 9.09, 9.31, 9.53, 9.76,
    ];
    let rVals = (_useE96) ? e96 : e24;

    let r_ratio = [];
    for (let i = 0; i < rVals.length; i++) {
        let r1 = rVals[i];
        let r2_guess = r1 * Math.pow(10, logk);
        let r2_exponent = Math.floor(Math.log10(r2_guess));
        let r2_coefficient = r2_guess / Math.pow(10, r2_exponent);
        let r2_candidate = [...rVals];
        r2_candidate.sort((a, b) => Math.abs(a - r2_coefficient) - Math.abs(b - r2_coefficient));
        let r2 = r2_candidate[0] * Math.pow(10, r2_exponent);

        let k = r2 / r1;
        let divRatio = r2 / (r1 + r2);
        let vOut_calc = _vSupply * r2 / (r1 + r2)
        let delta = Math.abs(vOut_calc - _vOut);
        r_ratio.push({
            r1: r1 * _scale,
            r2: r2 * _scale,
            r2_div_r1: k,
            divRatio: divRatio,
            target: ratio_V_target,
            delta: delta,
            vOut: vOut_calc,
        });
    }

    r_ratio.sort((a, b) => a.delta - b.delta);
    return r_ratio.slice(0, _maxResults);
}
