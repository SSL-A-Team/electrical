# Motor Controller v1.1 Changelog
 - adds independent fusing for stspin Vmotor, provides better isolation if Vmotor bridges to other rails
 - adds TVS diode after 3v3 fuse, provides better isolation in the event Vmotor bridges to 3v3
 - adds low-half resistors to current sense and OCP DC offset circuity, decouples from amp leakage calibration
 - adds current limiting resistor to RST transistor gate