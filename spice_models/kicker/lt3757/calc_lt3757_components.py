# Calculates passives for the lt3757 flyback mode regulator
# circuit in the datasheet (pg. 32) The datasheet is available
# here: https://www.analog.com/media/en/technical-documentation/data-sheets/lt3757-3757a.pdf
#
# A spice model is included by default with LT Spice.
import math

import eseries
from UliEngineering.Electronics import VoltageDivider

############################
#  User Adjustable Params  #
############################

### Capacitor Bank Parameters
# desired charge time of the primary bank (s)
T_charge_bank_s = 0.75
# capacitance of the primary bank (F)
C_out = 3000e-6
# voltage of the primary bank (V)
V_out = 200.0
# selected primary side charging current (A)
# I_pk = 42.0
I_pk = 42.0
# charge voltage safety buffer
V_out_buf = 5.0

### Inductor Parameters
# GA3460-BL
# transformer ratio of the selected transformer
N = 10
# inductance of the primary side of the selected transformer
L_pri = 2.5e-6
# L_pri = 10e-6

# leakage inductance max
L_pri_leak = 0.060e-6
# L_pri_leak = 0.25e-6

### Switching FET Properties
# BSC0402NSATMA1
V_ds_on = 10.0
V_ds_max = 150.0
I_d_max = 80.0

### Rectifier Diode Properties
# MURS/460 (360 backup, I=3.0, V_f 1.25, trr=50ns)
# forward votlage drop of the selected rectifier diode
V_f_diode = 1.28  # forward voltage drop
V_rrm_diode = 600.0  # rated repetitive reverse voltage
I_diode = 4.0  # rated current
T_rr_diode = 50e-9  # reverse recovery time

### Battery Parameters (or source voltage variability)
lipo_num_cells = 6
LIPO_NOM_CELL_VOLTAGE = 3.7
LIPO_CELL_VOLTAGE_SWING = 0.5
V_trans_min = lipo_num_cells * (LIPO_NOM_CELL_VOLTAGE - LIPO_CELL_VOLTAGE_SWING)
V_trans_nominal = lipo_num_cells * (LIPO_NOM_CELL_VOLTAGE)
V_trans_max = lipo_num_cells * (LIPO_NOM_CELL_VOLTAGE + LIPO_CELL_VOLTAGE_SWING)
V_trans_lockout_buffer = 2.0

# IC power voltage
V_cc = 12.0
V_cc_lockout_buffer = 0.5

t_d = 0.0  # switching time delay losses (ignore or reproduce from selected switching FET as described)
estimate_efficiency = 0.80

#
#
#

V_diode = V_f_diode  # datasheet refers to the forward voltage drop as V_diode, but this is a little ambiguous

print("")
print(f"-------------------===-------------------")
print("select feedback resistor values")
print("")

V_fb_tgt = V_out - V_out_buf
V_fb_ref = 1.6  # pg 12 of datasheet
R_fb_lower = eseries.find_less_than_or_equal(eseries.E96, 2940)  # 3k as a starting point seems to make reasonable upper values
R_tot_desired_upper = VoltageDivider.feedback_top_resistor(V_fb_tgt, R_fb_lower, V_fb_ref)
# the voltage here can be really high for a single 0402/0603 so we'll half it and stack the values
# to manage the potential across teh footprint
R_half_desired = R_tot_desired_upper / 2.0
R_half_desired_E96 = eseries.find_less_than_or_equal(eseries.E96, R_half_desired)

print(f"selected R_fb_upper  {R_half_desired_E96} x2 (use two 0402 or 0603 resistors of this value for a total of {2.0 * R_half_desired_E96}")
print(f"selected R_fb_lower {R_fb_lower}")