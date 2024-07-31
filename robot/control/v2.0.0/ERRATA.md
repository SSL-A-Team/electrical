# Control v2.0 Errata

 - KICKER_DET line is not actually routed to the MCU. Detection implemented using other means in firmware
 - LT4367 protection chip still does not full survive repeated battery hot plug events. Can be bypassed by depopulating R7, R8, R9, and R10 and then solder bridging U2.1 with U2.2 and U2.3 with U3.4, disabling UV and OV protections. 
 - stspin motor controller watchdog protections do not work because nrst is driven high with a Lo-Z source by the MCU. Depopulate R91, R121, R151, R181, R211 and load the latest comp firmware. 
 - depopulate R14, pull up technically overvolts downstream regulator enable pin but current is VERY low 