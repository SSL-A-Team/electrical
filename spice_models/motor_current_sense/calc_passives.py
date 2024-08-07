# Calculates passive values for the motor current sensing network
# these can be loaded into the adjacent spice models to
# see the network response
#
# The dev board amplifier network equations are specified in
# ST Microelectronics Application Note AN5397. Variable names in this
# script will use identical names and equation references. We use the
# variant of the network in Figure 8, but with a non-symmetrical DC
# offset.
# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjd26rjm8P6AhWyj4kEHeTmAPgQFnoECBIQAQ&url=https%3A%2F%2Fwww.st.com%2Fresource%2Fen%2Fapplication_note%2Fan5397-current-sensing-in-motion-control-applications-stmicroelectronics.pdf&usg=AOvVaw2--yddSoA57WRf8KFsh-lz
#
# It's also noted the STSPIN (stspin32f0(?a|b)) internal amplifier
# doesn't have a spice model or internal chart, just characteristic
# parameters. Ryo identified LTC6241 a similar part, so it's parameters
# are used here as needed.
#
# Generally, one should set I_max and V_motor

import eseries
import math
from UliEngineering.Electronics import VoltageDivider

############################
#  user adjustable params  #
############################

# maximum current we want to accurately sense
# df45 50W and 65W are rated for 2.36A, and 3.26A respectively
# ecu22048h24 is rated for 2.94A, h18 (not using) is rated for 4.04A
# we pick 4.0A to give us some margin for noise/error
# NOTE: stalled motor will greatly exceed this, but that's ok
I_max = 4.0

# 6C LiPo battery, full charged is 4.2V/cell
V_motor_max = 4.2 * 6.0

# max resistor wattage
P_max_W = 1.0

num_adc_bits = 10

###########################
#  non-adjustable params  #
###########################

operating_boundary_margin_v = 0.25
Vgnd = 0.0
Vdda = 3.3

V_amp_output_min = Vgnd + operating_boundary_margin_v
V_amp_output_max = Vdda - operating_boundary_margin_v

# @48KHz PWM frequency
ltc6241_gain_db = 32.0
# dB = 20 * log_10(V1/V2) ~ 10^(db / 20) = V
ltc6241_gain_lin = 10 ** (ltc6241_gain_db / 20)
# print(f"Amplifier maximum linear V/V gain: {str(round(ltc6241_gain_lin, 3))}")
an5397_recommended_R1_E96 = 2.37e3 # 2k37

# P = I^2 * R
R_sense = P_max_W / (I_max ** 2)
print(f"maximum sense resistance: {R_sense}")

# round down to preserve safe thermal/power budget
R_sense_E24 = eseries.find_less_than_or_equal(eseries.E24, R_sense)

R_sense_05 = R_sense / 2.0
R_sense_05_E24 = eseries.find_less_than_or_equal(eseries.E24, R_sense_05)

# print("")
V_output_range = V_amp_output_max - V_amp_output_min
# print(f"Desired amplifier output range {V_output_range}")

# V = IR
V_input_range = I_max * R_sense_E24
V_gain_needed = round(V_output_range / V_input_range, 3)

print(f"desired amplifier gain: {V_gain_needed}")
if V_gain_needed > ltc6241_gain_lin:
    print("WARNING: needed gain exceeds stable gain limit of the amplifier")

# AN5397 eq. 13
# G = (R2 / R1)
r2 = V_gain_needed * an5397_recommended_R1_E96
# it's prudent to round away (down) from the max gain to stay away from the OpAmp rails in-case
# a very small or 0 margin is picked, otherwise we might chop off the performant range
# R2 proportional to Gain, so also round R2 down
r2_E96 = eseries.find_less_than_or_equal(eseries.E96, r2)

actual_gain = round(r2_E96 / an5397_recommended_R1_E96, 3)
print(f"actual amplifier gain: {actual_gain}")
V_actual_output_range = V_input_range * actual_gain

# round in the direction of higher DC offset to keep away from edges of amplifier operating region
R_dc_offset_bottom_E96 = eseries.find_greater_than_or_equal(eseries.E96, 2 * r2_E96)
R_dc_offset_ratio = V_amp_output_min / Vdda
R_dc_offset_top = VoltageDivider.top_resistor_by_ratio(R_dc_offset_bottom_E96, R_dc_offset_ratio)
# round in the direction of higher DC offset to keep away from edges of amplifier operating region
R_dc_offset_top_E96 = eseries.find_less_than_or_equal(eseries.E96, R_dc_offset_top)
V_dc_offset = VoltageDivider.voltage_divider_voltage(R_dc_offset_top_E96, R_dc_offset_bottom_E96, Vdda)

V_actual_min_output = round(V_dc_offset, 3)
if V_actual_min_output < V_amp_output_min:
    print("WARNING: minimum amplifier output fell below desired minimum")

V_actual_max_output = round(V_dc_offset + V_actual_output_range, 3)
if V_actual_max_output > V_amp_output_max:
    print("WARNING: maximum amplifier output is above desired maximim")

num_adc_values = 2 ** num_adc_bits
pct_range_used = V_actual_output_range / (Vdda - Vgnd)

print("")
print("")
print(f"Nominal voltage range at ADC: [{V_actual_min_output}, {V_actual_max_output}]")
print(f"Num ADC quant. steps used {math.floor(pct_range_used * num_adc_values)} ({round(pct_range_used * 100.0, 1)}%)")
print("")
print(f"BUY: R_sense (AN5397 Rs) resistor value {str(round(R_sense_E24, 3))} (5%, {P_max_W}W)")
# print(f"\tALT: Buy resistor value {str(round(R_sense_05_E24, 3))} (5%) and place in parallel")
print(f"BUY: R1 (AN5397 R1) value {str(round(an5397_recommended_R1_E96, 3))}")
print(f"BUY: R2 (AN5397 R2) value {str(round(r2_E96, 3))} (1%)")
print(f"BUY: R_dc_offset_lower (AN5397 2*R2 lower) value {str(round(R_dc_offset_bottom_E96, 3))} (1%)")
print(f"BUY: R_dc_offset_upper (AN5397 2*R2 upper) value {str(round(R_dc_offset_top_E96, 3))} (1%)")
