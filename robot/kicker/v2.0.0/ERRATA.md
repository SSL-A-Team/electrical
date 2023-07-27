# Errata for Kicker v2.0.0

 - High Voltage rail sometimes charges uncommanded on startup when battery power is supplied
   - Root Cause: 12v power can leak through the body diode of the internal LDO FET in the lt3757, allowing ~10.5V on to Vbatt. The leakage path also enables charging.
   - Solution: Fix power sequencing, patch a diode with Vf <= 1.0V from 12v to Vbatt. This stop the leakage path through the lt3757, resolving the issue.
   - Patch Notes:
 - Unconfirmed: High Voltage rail charge uncommanded on startup
   - Root Cause: unknown and non-reproducible. Possible issue with old deployed firmware revisions. Possible EOS due to long power pigtail
   - Solution: unknown, unable to reproduce after initial issue
   - Patch Notes: