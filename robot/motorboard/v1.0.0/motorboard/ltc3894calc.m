pkg load dataframe

%{
Global robot properties
%}

% battery calculations
batt_num_cells = 6;

cell_min_safe_voltage = 3.0;
cell_nom_voltage = 3.7;
cell_max_safe_voltage = 4.2;

Vbatt_lo = batt_num_cells * cell_min_safe_voltage;
Vbatt_nom = batt_num_cells * cell_nom_voltage;
Vbatt_hi = batt_num_cells * cell_max_safe_voltage;

dataframe({"Vbatt Minimum", "Vbatt Nominal", "Vbatt Maximum"; Vbatt_lo, Vbatt_nom, Vbatt_hi})

%{
12V, 72W regulator derivation
%}

%% Config Values
Vout = 12;
Vin_max = Vbatt_hi;

freq = 350e3; % selected from lowest default option in datasheet
Iout_max = 6; % based on estimated 72W power consumption for worst case entire robot

%% Calculated Values
deltaIL_max = 0.4 * Iout_max;

L = ( Vout/(freq*deltaIL_max) ) * ( 1-(Vout/Vin_max) );

duty = Vout / Vin_max;
Ifwd_avg = Iout_max * (1 - duty);


deltaIL = ( Vout/(freq*0.8*L) ) * ( 1-(Vout/Vin_max) );
Vsense_max = 88e-3;
Rsense = Vsense_max / (Iout_max + (deltaIL / 2));
Rsense_power = (Iout_max .^ 2) .* Rsense;

display_data = {"Select Inductor L >=", 
  "Select Inductor I >=", 
  "Select Diode Power >= listed_val * Vf_diode", 
  "Select Rsense R as close to but lower than", 
  "Select Rsense P >=";
L, 
  Iout_max, 
  Iout_max, 
  Rsense, 
  Rsense_power}
  