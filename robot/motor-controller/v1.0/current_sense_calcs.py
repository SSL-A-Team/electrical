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

Irated = nanotec_df45_65W_Irated
Ipeak = nanotec_df45_65W_Ipeak
Istall = nanotec_df45_65W_Istall