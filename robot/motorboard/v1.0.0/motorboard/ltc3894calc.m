%% Config Values
Vout = 12;
Vin_max = 25.2;

freq = 350e3;
Iout_max = 6;

%% Calculated Values
deltaIL_max = 0.4 * Iout_max;

L = ( Vout/(freq*deltaIL_max) ) * ( 1-(Vout/Vin_max) )

duty = Vout / Vin_max;
Ifwd_avg = Iout_max * (1 - duty)


deltaIL = ( Vout/(freq*0.8*L) ) * ( 1-(Vout/Vin_max) );
Vsense_max = 88e-3;
Rsense = Vsense_max / (Iout_max + (deltaIL / 2))
