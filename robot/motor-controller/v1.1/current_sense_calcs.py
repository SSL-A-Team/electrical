# Important Documents
#   - Datasheet: STSPIN32F0
#   - Current Sensing: AN5397
#
#
# we should deploy a layered protection strategy covering the following cases
# dead shorts
# motor stall
# overstress (too much time spent above continuous rated current)
#    this could be intentional (aggressive play)
#    OR accidential (bad controls)
#
# We rely on a slow blow high current fuse to address dead shorts
# The fuse and OCP will address motor stalls, OCP will probably kick in first
#   Slow blow fuses tend to be *very* slow unless the current is quite a bit higher than rated
#   Fast blow is probably wrong choice here, collisions/etc might cause short momentary current spikes
#   and we don't want the motor controller to just break safe in these cases
#
# The upstream board can always fuse *lower* for a specific deployed motor
#
# Datasheet says OCth has a 8% error tolerance at all programmable voltages
# Need to set OCP at 10% over the peak current or more, but beneath the stall current
#
# OpAmp Params
#   GBP: 18Mhz
#
#

nanotec_df45_50W_Irated = 2.4
nanotec_df45_50W_Ipeak = 7.0
nanotec_df45_50W_Istall = 13.9
nanotec_df45_65W_Irated = 3.3
nanotec_df45_65W_Ipeak = 9.5
nanotec_df45_65W_Istall = 14.8

# analog supply parameters
Vdda = 3.0

# motor parameters
Irated = nanotec_df45_65W_Irated
Ipeak = nanotec_df45_65W_Ipeak
Istall = nanotec_df45_65W_Istall
Imax = 10.0

# OpAmp user parameters
Vdynrng_guard = 0.25

# user component selections
Rsense = 0.050
Rb = 2.37e3

Ra = 140e3
R2 = 40e3
R1 = 10e3

Vdynrng_opamp = Vdda - (0.2 * 2)
Vdynrng_opamp_selected = Vdda - (Vdynrng_guard * 2)
Vdynrng_opamp_lo = Vdynrng_guard
Vdynrng_opamp_hi = Vdda - Vdynrng_guard

print("OpAmp Contraints")

Gmax = Vdynrng_opamp / (Imax * Rsense)

print(f"\tMax Gain: {Gmax}")

Gmax_guard = Vdynrng_opamp_selected / (Imax * Rsense)

print(f"\tMax Gain: {Gmax_guard}")

G = 1 + (R2 / R1)

print(f"\tSelected Gain: {G}")

Vibias_desired = Vdynrng_guard / G

print(f"\tDesired Raw Input Bias: {Vibias_desired}")

Vibias_selected_raw = (Vdda * Rb) / (Ra + Rb)

print(f"\tSelected Raw Bias: {Vibias_selected_raw}")

Vibias_selected_op = Vibias_selected_raw * G

print(f"\tSelected Bias: {Vibias_selected_op}")

Vdynrng_guard_error = abs(Vibias_selected_op - Vdynrng_guard)

print(f"\tDyn Rng Guard Error: {Vdynrng_guard_error}")

GReal = Ra / (Ra + Rb) * G

print(f"\tReal Gain: {GReal}")

I_input_bias = 100e-12

Voutput_bias_pos = I_input_bias * ((1)/((1/Ra)+(1/Rb)) * (1 + R2/R1))
Voutput_bias_neg = -I_input_bias * ((R1*R2)/(R1+R2))
Voutput_bias_total = Voutput_bias_pos + Voutput_bias_neg
print(f"\tVob_pos: {Voutput_bias_pos}")
print(f"\tVob_neg: {Voutput_bias_neg}")
print(f"\tVob_total: {Voutput_bias_total}")