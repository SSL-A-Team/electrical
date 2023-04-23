let v_batt = 22.2;
let c_delay = 10e-6;
let ratio_charge = 0.99;

let r_pulldown = 910e3;
let r_chargeLimiter = 10e3;
let r_dischargeLimiter = r_pulldown + r_chargeLimiter;

let ratio_div = r_pulldown / (r_pulldown + r_chargeLimiter);
let v_cTarget = 1.2 / ratio_div;
let v_charged = v_batt * ratio_charge;

let time_charge = -r_chargeLimiter * c_delay * Math.log(1 - ratio_charge);
let time_discharge = -r_dischargeLimiter * c_delay * Math.log(v_cTarget / v_charged);

let result = {
    "TimeToCharge": time_charge,
    "TimeToShutoff": time_discharge
};
console.table(result);
