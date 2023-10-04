#!/usr/bin/env python

import eseries
from UliEngineering.Electronics import VoltageDivider

LIPO_CELL_MIN = 3.2
LIPO_CELL_NOMINAL = 3.7
LIPO_CELL_MAX = 4.2
NUM_LIPO_CELLS = 6

Vin_min = NUM_LIPO_CELLS * LIPO_CELL_MIN
Vin_nominal = NUM_LIPO_CELLS * LIPO_CELL_NOMINAL
Vin_max = NUM_LIPO_CELLS * LIPO_CELL_MAX

Vout_1 = 12.0  # LT3757 drive, IGBT gate driver
Vout_2 = 3.3   # Digital
Vout_3 = 5.0   # Digital,  Dotstar
Vout_4 = 6.2   # Future Servo Motor

Iout_1 = 1.0
Iout_2 = 1.0
Iout_3 = 1.0
Iout_4 = 1.0

Vout_1_ss_us = 0
Vout_2_ss_us = 0
Vout_3_ss_us = 0
Vout_4_ss_us = 0

Vdiode_f = 0.4
Idiode_f = 1.0
Vdiode_standoff = 40.0

# internal switching frequency
f_sw_internal = 1.5e6


def calc_feedback_resistor(desired_Vout: float) -> (float, float):
    # R1 = R2 * ((Vout / 0.8V) - 1)
    # R_fb_upper = R_fb_lower * ((Vout / 0.8) - 1.0)
    # R_fb_lower_recommended = 10000
    # R_fb_upper = 10000 * ((Vout / 0.8) - 1.0)

    R_fb_lower_recommended = 10e3 # 10k
    R_fb_lower_E96 = eseries.find_greater_than_or_equal(eseries.E96, R_fb_lower_recommended)
    R_fb_upper_precise = R_fb_lower_E96 * ((desired_Vout / 0.8) - 1.0)
    R_fb_upper_E96 = eseries.find_greater_than_or_equal(eseries.E96, R_fb_upper_precise)


    return (R_fb_upper_E96, R_fb_lower_E96) 


def calc_regulator_L(Vout: float) -> float:
    return 2.0 * (Vout + Vdiode_f) / f_sw_internal


def calc_decoupling_out(Vout: float) -> float:
    return 33 / (Vout * f_sw_internal)


if Vin_max > 40:
    print("Vin upper bound exceeded")

# L_sky = 20.5e-6 / f_sw_internal
I_sky = ((Iout_1 * Vout_1) + (Iout_2 * Vout_2) + (Iout_3 * Vout_3) + (Iout_4 * Vout_4)) / (50 * Vin_min) # select Vin_min anatagonistically
I_sky = round(I_sky, 4)
print(f"I_sky: {I_sky}")

DC5 = 5.0 / (Vin_nominal + 5.0)
L_sky = (Vin_max * DC5) / (2 * f_sw_internal * (0.3 * (1 - 0.25 * DC5) - I_sky))
L_sky_uH = round(L_sky * 1e6, 2)
print(f"L_sky: {L_sky_uH} uH")

L_Vout1 = round(calc_regulator_L(Vout_1) * 1e6, 2)
R_Vout1_upper, R_Vout1_lower = calc_feedback_resistor(Vout_1)
C_Vout1 = round(calc_decoupling_out(Vout_1) * 1e6, 2)
print(f"Vout 1 {Vout_1}: L1 {L_Vout1} uH, R upper {R_Vout1_upper}, R lower {R_Vout1_lower}, Cout {C_Vout1}")

L_Vout2 = round(calc_regulator_L(Vout_2) * 1e6, 2)
R_Vout2_upper, R_Vout2_lower = calc_feedback_resistor(Vout_2)
C_Vout2 = round(calc_decoupling_out(Vout_2) * 1e6, 2)
print(f"Vout 2 {Vout_2}: L1 {L_Vout2} uH, R upper {R_Vout2_upper}, R lower {R_Vout2_lower}, Cout {C_Vout2}")

L_Vout3 = round(calc_regulator_L(Vout_3) * 1e6, 2)
R_Vout3_upper, R_Vout3_lower = calc_feedback_resistor(Vout_3)
C_Vout3 = round(calc_decoupling_out(Vout_3) * 1e6, 2)
print(f"Vout 3 {Vout_3}: L1 {L_Vout3} uH, R upper {R_Vout3_upper}, R lower {R_Vout3_lower}, Cout {C_Vout3}")

L_Vout4 = round(calc_regulator_L(Vout_4) * 1e6, 2)
R_Vout4_upper, R_Vout4_lower = calc_feedback_resistor(Vout_4)
C_Vout4 = round(calc_decoupling_out(Vout_4) * 1e6, 2)
print(f"Vout 4 {Vout_4}: L1 {L_Vout4} uH, R upper {R_Vout4_upper}, R lower {R_Vout4_lower}, Cout {C_Vout4}")
