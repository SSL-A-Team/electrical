let V_out = 3.3;
let V_supply = 30;
let scale = 1e3; // scale resistance range for R2 (e.g. 1000 places it in the kOhm range)
let useE96 = true; // set true if 1% (otherwise 5% tolerance)
let maxResults = 10; // gets the top n results


let ratio_V_target = V_out / V_supply;
let logk = Math.floor(Math.log10(ratio_V_target / (1 - ratio_V_target)));

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
let rVals = (useE96) ? e96 : e24;

let r_ratio = [];
for (let i = 0; i < rVals.length; i++) {
    let r1 = Math.round(Math.pow(10, -logk) * rVals[i] * scale);
    for (let j = 0; j < rVals.length; j++) {
        let r2 = Math.round(rVals[j] * scale);
        let k = r2 / r1;
        let divRatio = r2 / (r1 + r2);
        let delta = Math.abs(divRatio - ratio_V_target);
        r_ratio.push({
            r1: r1,
            r2: r2,
            r2_div_r1: k,
            divRatio: divRatio,
            target: ratio_V_target,
            delta: delta,
            vOut: divRatio * V_supply,
        });
    }
}

r_ratio.sort((a, b) => a.delta - b.delta);
console.table(r_ratio.slice(0, maxResults));
