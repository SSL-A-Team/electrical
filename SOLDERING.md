# A-Team Soldering Guide

During fleet board production, the team soldered many components JLC did not have in stock. These also tended to be the more complex components.

The team noticed that minor soldering technique choices had a substantial impact on reliability and yield rate. Specific materials and techniques that made differences in our success are documented below.

## Solder Choice

Leaded solder should be used (60/40 or 63/37) to reduce the hot air reflow temperature. Especially on larger boards (like control), lower and slower temperature bring ups reduce warping from localized heating. This impacts yeild rate of components like the stm32h7 in the large lqfp-144 package that need a highly planer board to adhere all pins.

Keeping the reflow temperature low was also important for our Odin-W262 radio, which is a SoM board made with lead-free solder. Keeping the temperature low means we do not reflow the SoM components when attaching the SoM to our board.

If the team has a bottom heating apparatus, this is much less of a factor.  

## Choice in Flux and Cleaning Agent

The high efficiency switching power supplies were highly sensitive to cleaning method and flux choice, as small leakage currents on voltage and current sense area could produce DC error or instability in the rail.

It is absolutely required that 90-99% IPA be used as the cleaning agent. DO NOT USE 70% IPA. It does not dry sufficiently for a reliable product.

We recommend the use of ChipQuik WS991. We also recommend against using other water soluable variants as we noticed it seemed to bubble up when very low currents passed though it over time. The exact mechnism was unclear. This caused yield rate problems in stspins and U2. 

## Parts with EPAD

For parts with a ground pad underneath, take care not to overfill the pad. When the part is pushed down this can cause shoting to pins underneath. This is easy to do because a larger pad size (EPAD) compared with the other package pins produces a larger meniscus, which is non-linear.

Espcially on switching power supplies with very low resistance current detection, the potential difference created between CSN and EPAD due to a large solder blob on EPAD may be non-trivial. This was the case with the 12V regulator (U2), and the lt3751 and lt3757 on the kicker versions.

## IMUs

The small LGA IMUs are quite difficult to solder. We found yeild rates increased by fluxing then tinning both the board *AND* the part, then reflowing the part onto the board.