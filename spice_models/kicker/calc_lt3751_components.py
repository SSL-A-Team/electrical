# Calculates passives for the lt3751 capacitor charging reference
# circuit in the datasheet (pg. 25). The datasheet is available
# here: https://www.analog.com/media/en/technical-documentation/data-sheets/LT3751.pdf
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
I_pk = 42.0
# charge voltage safety buffer
V_out_buf = 5.0

### Inductor Parameters
# GA3460-BL
# transformer ratio of the selected transformer
N = 10
# inductance of the primary side of the selected transformer
L_pri = 2.5e-6
# leakage inductance max
L_pri_leak = 0.060e-6

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
print("-------------------===-------------------")
print("calculate ideal transformer values")
print("")

N_suggested = V_out / V_trans_nominal
N_suggested = round(N_suggested)
print(f"Suggested N: {N_suggested}")

I_pk_calculated = (((2.0 * N * V_trans_nominal) + V_out) * C_out * V_out) \
                  / (estimate_efficiency * V_trans_nominal * (T_charge_bank_s - t_d))
I_pk_calculated = round(I_pk_calculated, 2)
print(f"Desired charge time(s): {T_charge_bank_s}")
print(f"Calculated peak current to meet desired charge time: {I_pk_calculated}A")

L_pri_calc = (3e-6 * V_out) / (I_pk_calculated * N)
L_pri_calc = round(L_pri_calc, 9)
print(f"Suggested primary inductance: {L_pri_calc}H")

print("")
print("Future calculations will use the user selected values as it's impossible to find exact transformers. Suggested "
      "models are available in the datasheet (Table 1).")

print(f"-------------------===-------------------")

# bailout conditions established by the datasheet
if V_trans_max > 80.0:
    print("consult applications engineering.")
    print("this appear frequently in the datasheet, critical value seems to be 80 on pg. 18")
    exit(1)

print(f"calculate passives and resultant behavior")
print("")

# primary side inductance must be less than the following values
L_pri_max_stable_at_V_trans_min = (38e-6) / (I_pk * ((1.0 / V_trans_min) + (N / V_out)))
L_pri_max_stable_at_V_trans_max = (38e-6) / (I_pk * ((1.0 / V_trans_max) + (N / V_out)))
L_pri_max_stable = min(L_pri_max_stable_at_V_trans_min, L_pri_max_stable_at_V_trans_max)
if L_pri > L_pri_max_stable:
    print(f"ERROR: selected primary inductance of {L_pri} is greater than hard constraint of {L_pri_max_stable}")
    print(f"NOTE: the I_pk will not be reached within a refresh clock period")
    print(f"NOTE: this is a fatal configuration error. Remedies are suggested on pg. 16")
    exit(1)

print("inductor selection passed sanity checks")

V_drain_max = V_trans_max + ((V_out + V_diode) / N)
DEL_V_drain_max = V_drain_max - V_trans_min  # select antagonistically for greatest range
V_drain_min = V_trans_min + ((V_out + V_diode) / N)
DEL_V_drain_min = V_drain_min - V_trans_max  # select antagonistically for smallest range

print(f"Delta v drain max: {DEL_V_drain_max}, Delta v drain min: {DEL_V_drain_min}")

# assemble a table of R values for RVtrans, RVout, Rdcm
# datasheet gives the impression the designer should select the
# first compatible values going top down
# there are additional options, but require much more investigation
# and suggest speaking with applications engineering
R_value_table = [
    [(4.75, 55.0), (0.0, 5.0), 5.11e3, 5.11e3, 2.32e3],
    [(4.75, 60.0), (2.5, 50.0), 25.5e3, 25.5e3, 11.5e3],
    [(4.75, 60.0), (5.0, 80.0), 40.2e3, 40.2e3, 18.2e3],
    [(8.00, 80.0), (8.0, 160.0), 80.6e3, 80.6e3, 36.5e3]
]

R_value_table.reverse()

selected_R_value_entry = None
for entry in R_value_table:
    V_trans_range = entry[0]
    DEL_V_drain_range = entry[1]
    if V_trans_range[0] < V_trans_min and V_trans_max < V_trans_range[1] and \
            DEL_V_drain_range[0] < DEL_V_drain_min and DEL_V_drain_max < DEL_V_drain_range[1]:
        selected_R_value_entry = entry
        break

if selected_R_value_entry is None:
    print("ERROR: R value table lookup failed")
    print("INFO: manual re-optimization of selections necessary or consult applications engineering")
    print(f"NOTE: this is a fatal configuration error. Remedies are suggested on pg. 17")
    exit(1)

R_V_trans = selected_R_value_entry[2]
R_V_out = selected_R_value_entry[3]
R_dcm = selected_R_value_entry[4]

print(f"selected RVtrans: {R_V_trans}")
print(f"selected RVout: {R_V_out}")
print(f"selected Rdcm: {R_dcm}")

# as V_out is larger, R_bg becomes smaller, so round R_bg UP so V_out doesn't overshoot
R_bg = 0.98 * N * (R_V_out / ((V_out - V_out_buf) + V_diode))
R_bg_e96 = eseries.find_greater_than_or_equal(eseries.E96, R_bg)
print(f"selected Rbg: {R_bg_e96}")

if V_ds_on > V_cc - 2.0:
    print(f"ERROR: V_ds_on is too high")
    print(f"INFO: the regulator will not be able to full switch the FET on")
    print(f"NOTE: this is a fatal configuration error. Remedies are suggested on pg. 18")
    exit(1)

max_v_drain_spike = V_trans_max + (V_out / N)
if V_ds_max < max_v_drain_spike:
    print(f"ERROR: V_ds_max is too low")
    print(f"INFO: V_ds ({V_ds_max}) must be greater than {max_v_drain_spike}")
    print(f"INFO: the FET cannot survive the maximum reflected energy")
    print(f"NOTE: this is a fatal configuration error. Remedies are suggested on pg. 18")
    exit(1)

I_avg_m = (I_pk * V_out) / (2.0 * (V_out + (N * V_trans_min)))
if I_d_max < I_avg_m:
    print(f"ERROR: V_d_max is too low")
    print(f"INFO: the FET cannot survive the maximum peak current")
    print(f"NOTE: this is a fatal configuration error. Remedies are suggested on pg. 18")
    exit(1)

print("selected switching FET passed sanity checks.")

suggested_min_V_rrm = V_out + (N * V_trans_max)
if V_rrm_diode < suggested_min_V_rrm:
    print(f"ERROR: V_rrm_diode is too low")
    print(f"INFO: V_rrm_diode ({V_rrm_diode}) must be greater than {suggested_min_V_rrm}")
    print(f"INFO: the diode cannot survive the maximum transient reverse voltage")
    print(f"NOTE: this is a fatal configuration error. Remedies are suggested on pg. 19")
    exit(1)

suggested_min_I_f_av = I_pk / (2 * N)
if I_diode < suggested_min_I_f_av:
    print(f"ERROR: I_diode is too low")
    print(f"INFO: I_diode ({I_diode}) must be greater than {suggested_min_I_f_av}")
    print(f"INFO: the diode cannot survive thermal impact of the average forward current")
    print(f"NOTE: this is a fatal configuration error. Remedies are suggested on pg. 19")
    exit(1)

suggested_max_trr = 100e-9
if T_rr_diode > suggested_max_trr:
    print(f"ERROR: T_rr_diode is too high")
    print(f"INFO: T_rr_diode ({T_rr_diode}) must be less than {suggested_max_trr}")
    print(f"INFO: leakage current will cause charging and thermal mitigation issues")
    print(f"NOTE: this is a fatal configuration error. Remedies are suggested on pg. 19")
    exit(1)

print("diode selection passed sanity checks")

# I_pk = I_max = 106e-3 / R_sense
# when R_sense is larger, I_pk is lower, round R_sense up to avoid over current
R_sense = 106e-3 / I_pk
R_sense_E96 = eseries.find_greater_than_or_equal(eseries.E96, R_sense)

P_R_sense = (((I_pk ** 2.0) * R_sense_E96) / 3.0) * (V_out / (V_out + (N * V_trans_min)))
P_R_sense = round(P_R_sense, 3)
print(f"selected R_sense {R_sense_E96} 1%, P>={P_R_sense}W, L<=2nH")

print("")
print(f"-------------------===-------------------")
print("select feedback resistor values")
print("")

V_fb_tgt = V_out - V_out_buf
V_fb_ref = 1.22  # pg 8 of datasheet
R_fb_lower = eseries.find_less_than_or_equal(eseries.E96, 2940)  # 3k as a starting point seems to make reasonable upper values
R_tot_desired_upper = VoltageDivider.feedback_top_resistor(V_fb_tgt, R_fb_lower, V_fb_ref)
# the voltage here can be really high for a single 0402/0603 so we'll half it and stack the values
# to manage the potential across teh footprint
R_half_desired = R_tot_desired_upper / 2.0
R_half_desired_E96 = eseries.find_greater_than_or_equal(eseries.E96, R_half_desired)

print(f"selected R_fb_upper  {R_half_desired_E96} x2 (use two 0402 or 0603 resistors of this value for a total of {2.0 * R_half_desired_E96}")
print(f"selected R_fb_lower {R_fb_lower}")

print("")
print(f"-------------------===-------------------")
print("select under and over voltage lock out resistor values")
print("")

V_trans_uvlo = V_trans_min - V_trans_lockout_buffer
V_trans_ovlo = V_trans_max + V_trans_lockout_buffer
V_cc_uvlo = V_cc - V_cc_lockout_buffer
V_cc_ovlo = V_cc + V_cc_lockout_buffer

R_vtrans_uvlo1 = (V_trans_uvlo - 1.225) / 50e-6
R_vtrans_ovlo1 = (V_trans_ovlo - 1.225) / 50e-6
R_cc_uvlo2 = (V_cc_uvlo - 1.225) / 50e-6
R_cc_ovlo2 = (V_cc_ovlo - 1.225) / 50e-6

R_vtrans_uvlo1_E96 = eseries.find_less_than_or_equal(eseries.E96, R_vtrans_uvlo1)
R_vtrans_ovlo1_E96 = eseries.find_greater_than_or_equal(eseries.E96, R_vtrans_ovlo1)
R_cc_uvlo2_E96 = eseries.find_less_than_or_equal(eseries.E96, R_cc_uvlo2)
R_cc_ovlo2_E96 = eseries.find_greater_than_or_equal(eseries.E96, R_cc_ovlo2)

print(f"selected R_Vtrans UVLO1 {R_vtrans_uvlo1_E96}")
print(f"selected R_Vtrans OVLO1 {R_vtrans_ovlo1_E96}")
print(f"selected R_Vcc UVLO2 {R_cc_uvlo2_E96}")
print(f"selected R_Vcc OVLO2 {R_cc_ovlo2_E96}")

print("")
print(f"-------------------===-------------------")
print("determine SPICE leakage values")
print("")

L_sec = L_pri * (N ** 2)
K = math.sqrt(1.0 - (L_pri_leak / L_pri))
L_pri_series_leakage = (1.0 - K) * L_pri
L_pri_coupled = K * L_pri
L_sec_series_leakage = (1.0 - K) * L_sec
L_sec_coupled = K * L_sec

L_pri_series_leakage = round(L_pri_series_leakage, 9)
L_pri_coupled = round(L_pri_coupled, 9)
L_sec_series_leakage = round(L_sec_series_leakage, 8)
L_sec_coupled = round(L_sec_coupled, 6)

print(f"primary series inductance (leakage) uH: {L_pri_series_leakage * 1e6}")
print(f"primary coupled inductance uH: {L_pri_coupled * 1e6}")
print(f"secondary series inductance (leakage) uH: {L_sec_series_leakage * 1e6}")
print(f"secondary coupled inductance uH: {L_sec_coupled * 1e6}")
