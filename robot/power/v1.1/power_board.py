from battery_model import BatteryCellConfig, LiPoBattery

import numpy as np
import eseries
from UliEngineering.Electronics import VoltageDivider

lipo_cell_model = BatteryCellConfig(3.0, 3.2, 3.7, 4.2)
lipo_battery_model = LiPoBattery(6, lipo_cell_model, 1300.0, 35.0)

Vdd_digital = 3.3

# we want a voltage divider per cell for monitoring purposes
# we want this to be very high resistance overall since it
# will be before the load switch, so anytime the battery is
# connected it will pull current
#
# let start with a base resistance around 250kOhm
R_cell_sense_bottom = 500e3
resistor_precision = eseries.E192

R_cell_sense_bottom_E192 = eseries.find_less_than_or_equal(resistor_precision, R_cell_sense_bottom)

adc_target_voltage = 2.0

# lets calculate and uppers for each cell
upper_resistors = []
upper_resistors_E192 = []
total_resistances = []
cell_critical_voltages = []
cell_empty_voltages = []
cell_nominal_voltages = []
cell_full_voltages = []

for cell in range(1, lipo_battery_model.get_num_cells() + 1):
    cell_max_voltage = lipo_battery_model.get_cell_full_voltage(cell)
    R_cell_sense_desired_upper = VoltageDivider.feedback_top_resistor(cell_max_voltage, R_cell_sense_bottom_E192, adc_target_voltage)
    R_cell_sense_upper_E192 = eseries.find_greater_than_or_equal(resistor_precision, R_cell_sense_desired_upper)
    upper_resistors.append(R_cell_sense_desired_upper)
    upper_resistors_E192.append(R_cell_sense_upper_E192)
    total_resistances.append(R_cell_sense_bottom_E192 + R_cell_sense_upper_E192)
    print(f"Cell{cell}: Selected {R_cell_sense_upper_E192} / {R_cell_sense_bottom_E192} resistors.")
    
    actual_ratio = VoltageDivider.voltage_divider_ratio(R_cell_sense_upper_E192, R_cell_sense_bottom_E192)
    print(f"Cell{cell}: actual ratio {actual_ratio} (after series quantization)")

    vref_at_critical = lipo_battery_model.get_cell_critical_voltage(cell) * actual_ratio
    vref_at_empty = lipo_battery_model.get_cell_empty_voltage(cell) * actual_ratio
    vref_at_nominal = lipo_battery_model.get_cell_nominal_voltage(cell) * actual_ratio
    vref_at_full = lipo_battery_model.get_cell_full_voltage(cell) * actual_ratio
    cell_critical_voltages.append(vref_at_critical)
    cell_empty_voltages.append(vref_at_empty)
    cell_nominal_voltages.append(vref_at_nominal)
    cell_full_voltages.append(vref_at_full)

    print(f"Cell{cell}: approx Vref at critical {vref_at_critical}V")
    print(f"Cell{cell}: approx Vref at empty {vref_at_empty}V")
    print(f"Cell{cell}: approx Vref at nominal {vref_at_nominal}V")
    print(f"Cell{cell}: approx Vref at full {vref_at_full}V")
    print(f"actual firmware should subtract previous cell measurement to get more precise value")
    print("")

# assume we have an independent measurement of vbatt which would match cell 6 params
total_resistances.append(total_resistances[lipo_battery_model.get_num_cells() - 1])
# update from OVLO/UVLO in schematic, and cross check with TI provided .xlsx files since current sources are involved
total_resistances.append(47.5e3 + 9.53e3)
total_resistances.append(95.3e3 + 8.66e3)

print(total_resistances)

def calc_parallel_resistance(res_arr):
    running_tot = 0
    for res in res_arr:
        running_tot = running_tot + (1.0 / res)

    return 1.0 / running_tot

res_of_meas_arr = calc_parallel_resistance(total_resistances)
current_of_meas_arr = lipo_battery_model.get_pack_max_voltage() / res_of_meas_arr
print(f"days of battery capacity {lipo_battery_model.battery_duration_at_current(current_of_meas_arr) / 24.0}")

# consult stmicroelectronics AN2834 for measuring high impedance sources with the ADC
# TLDR: we can avoid major pain beacuse we don't really care about signal bandwidth here
# which enabled the external capacitor option
# AN2834 computes a conservative value on pages 52-54, which results in C_ext of 220nF. We prioritize full
# accuracy over bandwidth, since cell voltages shouldn't swing rapidly (in ways that we care about)
C_sh = 16e-12
C_ext = 220e-9
R_in = max(total_resistances) # should probably be upper resistances only but this is more conservative
min_time_between_samples = -(R_in * C_ext) * np.log(1 - (C_sh / C_ext) * (4095 / 0.5))
print(f"max adc sample time {min_time_between_samples} ({(1.0 / min_time_between_samples)} Hz)")