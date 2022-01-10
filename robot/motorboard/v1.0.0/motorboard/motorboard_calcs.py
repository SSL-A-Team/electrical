#import pandas

## Global robot properties

# battery calculations
batt_num_cells = 6

cell_bare_minimum_under_load = 2.7
cell_min_safe_voltage = 3.0
cell_nom_voltage = 3.7
cell_max_safe_voltage = 4.2

Vbatt_bare_minimum_under_load = batt_num_cells * cell_bare_minimum_under_load
Vbatt_lo = batt_num_cells * cell_min_safe_voltage
Vbatt_nom = batt_num_cells * cell_nom_voltage
Vbatt_hi = batt_num_cells * cell_max_safe_voltage

# dataframe({"Vbatt Minimum", "Vbatt Nominal", "Vbatt Maximum" Vbatt_lo, Vbatt_nom, Vbatt_hi})

# motors
max_motor_current = 14.18 #df45 65W
nom_motor_current = 3.26

# relevant user guide https://www.st.com/resource/en/application_note/an5397-current-sensing-in-motion-control-applications-stmicroelectronics.pdf
# current sense
Rsense_chosen_R = 13e-3

R_inline = 1.78e3
R_fb = 13.7e3
R_bias = R_fb * 2.0

# overcurrent
Roc_inline = 3.3e3
Roc_bias = 59e3
Voc_tgt = 250e-3 # software config OC for 250mV (100, 250, 500)

# Inrush Current Calc
desired_Imax_inrush = 10
motor_decoupling_capactiance_F = 270e-6
cap_12v0_dc_F = 30e-6

total_motor_cap_F = 5 * motor_decoupling_capactiance_F
V_batt_downstream_capacitance_F = total_motor_cap_F + cap_12v0_dc_F

# battery OV/UV LO calcs
V_max_tolerable = Vbatt_hi * 1.25 # we can actually tolerate quite a bit more here, but this should be sane for a kicker
V_min_tolerable = Vbatt_bare_minimum_under_load
V_ovuv_lo_tol_err = 3e-3 # we don't really need 3mV, but increasing breaks datasheet math (e.g. 40M + resistor values)

chosen_r1_R = 154e3 # choose from E96
chosen_r2_R = 147e3 # choose from E96
chosen_r3_R = 5.1e6 + 4.3e6 # choose from E96

# 12V, 72W regulator derivation

## Config Values
Vout = 12
Vin_max = Vbatt_hi

freq = 350e3 # selected from lowest default option in datasheet
Iout_max = 6 # based on estimated 72W power consumption for worst case entire robot

## Calculated Values
deltaIL_max = 0.4 * Iout_max

L = ( Vout/(freq*deltaIL_max) ) * ( 1-(Vout/Vin_max) )

duty = Vout / Vin_max
Ifwd_avg = Iout_max * (1 - duty)


deltaIL = ( Vout/(freq*0.8*L) ) * ( 1-(Vout/Vin_max) )
Vsense_max = 88e-3
Rsense = Vsense_max / (Iout_max + (deltaIL / 2))
Rsense_power = (Iout_max ** 2) * Rsense

# display_data = {"Select Inductor L >=", 
#   "Select Inductor I >=", 
#   "Select Diode Power >= listed_val * Vf_diode", 
#   "Select Rsense R as close to but lower than", 
#   "Select Rsense P >="
# L, 
#   Iout_max, 
#   Iout_max, 
#   Rsense, 
#   Rsense_power}
  
## Current Sense and Gain Network Calc

V_pos = 3.3
V_neg = -3.3

V_o_pos = (R_fb / R_inline) * V_pos
V_o_neg = -(R_fb / R_inline) * V_neg
assert(V_o_pos == V_o_neg)
amp_gain = R_fb / R_inline
half_range = V_pos / 2.0
desired_Vdrop_Imax = half_range / amp_gain
max_Rsense_R = desired_Vdrop_Imax / max_motor_current
max_Rsense_W = (max_motor_current ** 2) * max_Rsense_R
nom_Rsense_w = (nom_motor_current ** 2) * max_Rsense_R

Vdrop_chosen = Rsense_chosen_R * max_motor_current
Rsense_loss_in_fidelity_pct = (1 - (Vdrop_chosen / desired_Vdrop_Imax)) * 100
Rsense_chosen_maxW = (max_motor_current ** 2) * Rsense_chosen_R
Rsense_chosen_nomW = (nom_motor_current ** 2) * Rsense_chosen_R

## Over Current Comparator Calc

Vdrop_sum = Vdrop_chosen
Voc_needed_bias = Voc_tgt - Vdrop_sum
Roc_needed_ratio = V_pos / Voc_needed_bias
Roc_lower = Roc_inline / 3
Roc_ratio = Roc_bias / Roc_lower
Voc_bias = V_pos / Roc_ratio
Voc_sense_trip = Voc_tgt - Voc_bias
Ioc_trip = Voc_sense_trip / Rsense_chosen_R
Ioc_trip_err_pct = (abs(Ioc_trip - max_motor_current) / max_motor_current) * 100

## Battery Voltage and Reverse Current Calcs

# inrush limit
C_out = V_batt_downstream_capacitance_F
gate_drv_source_current_A = 35e-6
C_gate = (gate_drv_source_current_A * C_out) / desired_Imax_inrush

# voltage lock out
# oooo kay looks like the selection value process for our 
I_leak_A = 10e-9
R1_plus_R2 = V_ovuv_lo_tol_err / I_leak_A
choose_R3_near = (V_ovuv_lo_tol_err / I_leak_A) * ((V_min_tolerable - 0.5) / 0.5)
choose_R1_near = (R1_plus_R2 + choose_R3_near) / (2.0 * V_max_tolerable)
choose_R2_near = R1_plus_R2 - choose_R1_near

actual_uvlo = ((0.5 * I_leak_A * chosen_r3_R) / V_ovuv_lo_tol_err) + 0.5
chosen_R1_plus_R2 = chosen_r1_R + chosen_r2_R
actual_ovlo = (chosen_R1_plus_R2 + chosen_r3_R) / (2.0 * chosen_r1_R)

# the laziest printing you ever did see
for name in sorted(dir()):
    if not name.startswith('__'): 
        print(name, ": ", eval(name))
