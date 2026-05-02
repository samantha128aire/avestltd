# N204MM Mooney Avionics Wiring Harness Instructions

## Project Overview

**Aircraft:** Mooney N204MM  
**Project:** Avionics upgrade and wiring harness fabrication  
**Complexity:** Intermediate to Advanced  
**Estimated Time:** 40-60 hours for complete installation

---

## System Architecture Overview

### Equipment Being Removed:
- King KT76A Transponder
- KNS80 RNAV
- Vacuum Attitude Indicator
- Vacuum Directional Gyro

### Equipment Being Added:
- **Aspen EFD1000 E5** - Primary Flight Display (replaces vacuum instruments)
- **Garmin GNX 375** - GPS/Transponder combo (replaces KNS80 and KT76A)
- **Garmin GI 275 MFD** - Multi-Function Display (interfaces with GNX 375)

### Equipment Remaining:
- Garmin GMA 340 Audio Panel
- Garmin GNS 430 GPS/Com/Nav
- King KY197 Comm
- Garmin Localizer/Glideslope
- King KI206 Localizer/Glideslope  
- S-Tec GPSS/HDG switch (P/N 03975)
- S-Tec 30 Autopilot

---

## Critical Integration Points

### 1. Aspen EFD1000 E5 Primary Flight Display

**Functions:**
- Attitude indicator
- Directional gyro/HSI
- Airspeed
- Altitude
- Vertical speed
- Turn coordinator
- AHRS (Attitude Heading Reference System)
- Autopilot interface
- GPS navigation display

**Key Interfaces:**
- Power (28V DC aircraft bus)
- ARINC 429 to GNS 430
- RS-232 to autopilot
- Analog inputs (pitot/static, OAT)
- Discrete autopilot control

---

### 2. Garmin GNX 375 GPS/Transponder

**Functions:**
- WAAS GPS navigator
- ADS-B Out/In transponder
- Weather display (FIS-B)
- Traffic display (TIS-B)
- WAAS LPV approaches

**Key Interfaces:**
- Power (28V DC aircraft bus)
- RS-232 to GI 275 MFD
- ARINC 429 outputs
- Antenna connections (GPS, transponder, diversity)
- Audio panel interface

---

### 3. Garmin GI 275 MFD

**Functions:**
- Multi-function display for GNX 375
- Traffic display
- Weather display
- GPS navigation backup
- Engine monitoring (if configured)

**Key Interfaces:**
- Power (28V DC aircraft bus)
- RS-232 to GNX 375
- CAN bus (optional for engine monitoring)

---

## WIRING HARNESS CONSTRUCTION

### Tools and Materials Required:

**Tools:**
- Wire strippers (20-26 AWG)
- Crimping tool for D-sub pins
- Crimping tool for Molex pins
- Soldering iron and solder
- Heat shrink tubing assortment
- Heat gun
- Digital multimeter
- Pin removal tools
- Cable ties and lacing cord
- Wire labels/tags

**Materials:**
- MIL-spec aircraft wire (various gauges, see below)
- D-sub connectors (match equipment requirements)
- Molex connectors (match equipment requirements)
- Shielded cable for serial communications
- Coaxial cable for antennas (RG-400 or RG-142)
- Heat shrink tubing
- Wire identification sleeves
- Connector backshells
- Grounding hardware

---

## POWER DISTRIBUTION

### Circuit Breaker Requirements:

**Aspen EFD1000 E5:**
- Primary power: 5A breaker
- Backup power: 5A breaker (separate bus)
- Wire: 20 AWG

**Garmin GNX 375:**
- Primary power: 5A breaker
- Wire: 20 AWG

**Garmin GI 275:**
- Primary power: 3A breaker
- Wire: 22 AWG

### Power Wiring:

**Color Code (Standard):**
- RED: +28V DC (hot)
- BLACK: Ground (return)
- WHITE: Lighting dimming (if applicable)

**Critical Notes:**
- All power connections must go through individual circuit breakers
- Use separate breakers for each unit
- Ensure clean power - consider adding noise filters if electrical noise is present
- Aspen EFD1000 E5 requires dual power inputs (primary and backup)
- All grounds must be connected to primary aircraft ground bus

---

## ASPEN EFD1000 E5 CONNECTIONS

### Connector: P1 (37-pin D-sub Male on aircraft harness side)

**POWER (Pins 1-6):**
```
Pin 1:  +28V Primary Power (RED, 20 AWG) → Aircraft Bus via 5A breaker
Pin 2:  Ground (BLACK, 20 AWG) → Primary ground bus
Pin 3:  +28V Backup Power (RED, 20 AWG) → Backup Bus via 5A breaker  
Pin 4:  Ground (BLACK, 20 AWG) → Primary ground bus
Pin 5:  Lighting Dimming (WHITE, 22 AWG) → Panel lights dimmer bus (optional)
Pin 6:  Shield Ground → Chassis ground
```

**AUTOPILOT INTERFACE (Pins 7-14):**
```
Pin 7:  AP Disconnect (YELLOW, 22 AWG) → S-TEC disconnect switch
Pin 8:  AP Engage (GREEN, 22 AWG) → S-TEC engage button
Pin 9:  AP Roll Servo (BLUE/WHITE, 22 AWG shielded) → S-TEC roll servo input
Pin 10: AP Roll Servo Ground (BLACK, 22 AWG) → Shield drain
Pin 11: AP Pitch Servo (GREEN/WHITE, 22 AWG shielded) → S-TEC pitch servo input
Pin 12: AP Pitch Servo Ground (BLACK, 22 AWG) → Shield drain
Pin 13: GPSS Output (ORANGE, 22 AWG) → S-TEC GPSS input
Pin 14: GPSS Ground (BLACK, 22 AWG) → Ground
```

**SERIAL DATA - GPS INPUT FROM GNS 430 (Pins 15-17):**
```
Pin 15: ARINC 429 HI from GNS 430 (BLUE, 22 AWG twisted shielded pair)
Pin 16: ARINC 429 LO from GNS 430 (BLUE/WHITE, 22 AWG twisted shielded pair)
Pin 17: Shield drain (connected to pin 6)
```

**AIR DATA (Pins 18-24):**
```
Pin 18: Pitot Pressure (YELLOW, pressure line, not electrical)
Pin 19: Static Pressure (GREEN, pressure line, not electrical)
Pin 20: OAT Sensor + (RED, 24 AWG) → OAT probe
Pin 21: OAT Sensor - (BLACK, 24 AWG) → OAT probe
Pin 22: Not used
Pin 23: Not used
Pin 24: Not used
```

**ADDITIONAL I/O (Pins 25-37):**
```
Pin 25: External annunciator + (ORANGE, 22 AWG) → Warning light (optional)
Pin 26: External annunciator - (BLACK, 22 AWG) → Ground
Pin 27-35: Reserved/Not used
Pin 36: RS-232 TX to GNS 430 (GREEN, 22 AWG shielded)
Pin 37: RS-232 RX from GNS 430 (BLUE, 22 AWG shielded)
```

---

## GARMIN GNX 375 CONNECTIONS

### Connector: P1 (25-pin D-sub Male on aircraft harness side)

**POWER (Pins 1-3):**
```
Pin 1:  +28V Primary Power (RED, 20 AWG) → Aircraft Bus via 5A breaker
Pin 2:  Ground (BLACK, 20 AWG) → Primary ground bus
Pin 3:  Shield Ground → Chassis ground
```

**SERIAL DATA TO GI 275 (Pins 4-6):**
```
Pin 4:  RS-232 TX to GI 275 (GREEN, 22 AWG shielded)
Pin 5:  RS-232 RX from GI 275 (BLUE, 22 AWG shielded)
Pin 6:  Shield drain (connect to pin 3)
```

**AUDIO PANEL INTERFACE (Pins 7-10):**
```
Pin 7:  Audio Out + (WHITE, 22 AWG shielded) → GMA 340 audio input
Pin 8:  Audio Out - (BLACK, 22 AWG) → Audio ground
Pin 9:  PTT Input (YELLOW, 22 AWG) → GMA 340 PTT relay for GNX COM
Pin 10: PTT Ground (BLACK, 22 AWG) → Ground
```

**ARINC 429 OUTPUT (Pins 11-13):**
```
Pin 11: ARINC 429 HI (ORANGE, 22 AWG twisted shielded pair) → Aspen or other avionics
Pin 12: ARINC 429 LO (ORANGE/WHITE, 22 AWG twisted shielded pair) → Aspen or other avionics
Pin 13: Shield drain
```

**LOCALIZER/GLIDESLOPE INPUT (Pins 14-17):**
```
Pin 14: LOC + (BLUE, 22 AWG shielded) → Garmin LOC/GS receiver output
Pin 15: LOC - (BLUE/WHITE, 22 AWG) → LOC ground
Pin 16: GS + (GREEN, 22 AWG shielded) → Garmin LOC/GS receiver output
Pin 17: GS - (GREEN/WHITE, 22 AWG) → GS ground
```

**ANTENNA CONNECTIONS (Coax, not on D-sub):**
```
GPS Antenna: TNC connector → RG-400 coax → GPS antenna (must be installed per STC)
Transponder Antenna 1: TNC connector → RG-400 coax → Bottom transponder antenna
Transponder Antenna 2 (Diversity): TNC connector → RG-400 coax → Top antenna (optional but recommended)
```

**REMAINING PINS (18-25):**
```
Pins 18-25: Reserved/configuration - refer to GNX 375 installation manual for specific aircraft features
```

---

## GARMIN GI 275 MFD CONNECTIONS

### Connector: P1 (15-pin D-sub Male on aircraft harness side)

**POWER (Pins 1-2):**
```
Pin 1:  +28V Primary Power (RED, 22 AWG) → Aircraft Bus via 3A breaker
Pin 2:  Ground (BLACK, 22 AWG) → Primary ground bus
```

**SERIAL DATA FROM GNX 375 (Pins 3-5):**
```
Pin 3:  RS-232 TX to GNX 375 (GREEN, 22 AWG shielded)
Pin 4:  RS-232 RX from GNX 375 (BLUE, 22 AWG shielded)
Pin 5:  Shield Ground → Chassis ground
```

**BACKLIGHT CONTROL (Pin 6):**
```
Pin 6:  Lighting Dimming (WHITE, 22 AWG) → Panel lights dimmer bus (optional)
```

**ADDITIONAL I/O (Pins 7-15):**
```
Pins 7-15: Reserved/CAN bus/configuration - refer to GI 275 manual for specific features
```

---

## INTEGRATION WITH EXISTING EQUIPMENT

### 1. Connection to Garmin GNS 430:

**ARINC 429 Output from GNS 430 to Aspen EFD1000:**
- Verify GNS 430 has ARINC 429 output capability (most do)
- Run twisted shielded pair from GNS 430 ARINC 429 output to Aspen P1 pins 15-16
- Configure GNS 430 to output GPS and navigation data on ARINC 429

**RS-232 between GNS 430 and Aspen (if required):**
- Some installations use RS-232 for additional data
- Connect GNS 430 RS-232 TX to Aspen P1 pin 37
- Connect GNS 430 RS-232 RX to Aspen P1 pin 36
- Use shielded cable

### 2. Connection to S-TEC 30 Autopilot:

**From Aspen EFD1000 to S-TEC 30:**
- Aspen provides autopilot drive signals
- Connect Aspen P1 pins 9-14 to S-TEC 30 corresponding inputs
- Refer to S-TEC 30 manual for exact pinout on autopilot computer
- GPSS signal from Aspen allows GPS steering from either GNS 430 or GNX 375

**GPSS Switch Integration:**
- Existing S-TEC GPSS/HDG switch (P/N 03975) remains
- Switch selects between GPSS (GPS steering) and HDG (heading) mode
- Aspen provides GPSS signal on P1 pin 13

### 3. Connection to Garmin GMA 340 Audio Panel:

**GNX 375 Audio:**
- GNX 375 has integrated COM transceiver capability
- Connect GNX 375 audio outputs (P1 pins 7-8) to GMA 340 audio input
- Connect PTT relay from GMA 340 to GNX 375 (P1 pin 9)
- Verify GMA 340 has available audio input channel

### 4. Localizer/Glideslope Integration:

**Existing Garmin LOC/GS Receiver:**
- Currently connected to KNS80 (being removed)
- Reconnect LOC/GS outputs to GNX 375 (P1 pins 14-17)
- This allows ILS approaches using GNX 375

**King KI206 LOC/GS:**
- Remains connected to GNS 430
- Provides backup ILS capability

---

## WIRING HARNESS CONSTRUCTION STEPS

### Step 1: Planning and Measurement

1. **Measure cable runs:**
   - From each new unit location to power bus
   - From each new unit to connection points on existing equipment
   - Add 20% extra length for routing and service loops

2. **Create wiring diagram:**
   - Draw out all connections on paper first
   - Label each wire with source, destination, and pin numbers
   - Use the pinout tables above

3. **Order materials:**
   - Calculate wire lengths needed for each gauge
   - Order appropriate connectors (D-subs with correct pin counts)
   - Order pins, backshells, heat shrink

### Step 2: Connector Assembly

**For D-sub Connectors:**

1. **Strip and tin wires:**
   - Strip 1/8" of insulation from wire end
   - Tin lightly with solder (do not over-solder)

2. **Crimp or solder pins:**
   - Use proper crimping tool for pin type
   - Alternatively, solder wires into pins (some prefer this for aircraft applications)
   - Ensure good mechanical connection

3. **Insert pins into connector:**
   - Follow pin-out diagram carefully
   - Pins typically lock into place with a click
   - Verify each pin is fully seated

4. **Install backshell:**
   - Route wire bundle through backshell before pinning
   - Secure cable with strain relief
   - Install backshell over connector

5. **Label connector:**
   - Label with unit name and connector number
   - Example: "ASPEN-P1" or "GNX375-P1"

### Step 3: Cable Routing

1. **Plan routing path:**
   - Avoid high-EMI areas (alternators, inverters, strobes)
   - Keep away from hot areas (exhaust, heating)
   - Use existing wire bundles where possible

2. **Secure cables:**
   - Use cable ties every 6-8 inches
   - Use cushioned clamps where cables pass through bulkheads
   - Provide service loops at each end (6-12 inches)

3. **Maintain separation:**
   - Keep power wires separate from signal wires
   - Keep shielded cables away from high-current wires
   - Cross power and signal cables at 90° if they must cross

### Step 4: Antenna Installation

**GPS Antenna (for GNX 375):**
- Install on top of fuselage per GNX 375 STC
- Use RG-400 coaxial cable
- Keep cable length as short as practical
- Install per Garmin instructions

**Transponder Antennas:**
- Bottom antenna (primary): Typically already installed
- Top antenna (diversity): Highly recommended for ADS-B
- Use RG-400 coaxial cable
- Maintain proper spacing between antennas (consult GNX 375 manual)

### Step 5: Grounding

**Critical Grounding Points:**
1. Primary ground bus connection for all equipment grounds
2. Shield drains at ONE end only (typically at equipment end)
3. Chassis grounds to aircraft structure
4. Verify continuity and low resistance (<0.1 ohm) to aircraft ground

**Grounding Best Practices:**
- Use star grounding topology where possible
- Never create ground loops
- Use separate ground wires for each unit
- Keep ground wires as short as practical

### Step 6: Power Connections

1. **Install circuit breakers:**
   - Aspen EFD1000: Two 5A breakers (primary and backup)
   - GNX 375: One 5A breaker
   - GI 275: One 3A breaker

2. **Connect power wires:**
   - Route power wires in separate conduit or bundle
   - Use proper crimps or solder joints at bus connections
   - Install inline fuses if breakers are not easily accessible

3. **Verify voltage:**
   - Check voltage at each unit location before connection
   - Should be 28V ± 2V DC
   - Check for voltage drop under load

### Step 7: Testing and Verification

**Pre-Power-Up Checks:**
1. Continuity test all connections with multimeter
2. Verify no shorts to ground (except ground pins)
3. Check all pin assignments against pinout diagrams
4. Verify all shields connected at ONE end only
5. Verify polarity of all power connections

**Power-Up Sequence:**
1. Power up Aspen EFD1000 first (verify display functions)
2. Power up GNX 375 (verify GPS lock and transponder)
3. Power up GI 275 (verify communication with GNX 375)
4. Verify all interfaces working:
   - GPS data to Aspen from GNS 430
   - Autopilot control from Aspen
   - Audio from GNX 375 to GMA 340
   - Traffic and weather on GI 275

**System Integration Testing:**
1. Verify GPS navigation on all displays
2. Test autopilot engagement and control
3. Test transponder operation (ground test only)
4. Verify ILS approaches work on GNX 375
5. Test all annunciators and warnings
6. Verify dimming functions

---

## CONFIGURATION SETTINGS

### Aspen EFD1000 E5:

**Menu → Setup → Installation:**
- Aircraft type: Mooney M20J
- Autopilot: S-TEC 30
- GPS source: GNS 430 via ARINC 429
- Backup GPS: GNX 375 (if configured)
- HSI source: Internal AHRS
- Air data: Internal ADC

### Garmin GNX 375:

**Menu → Setup → Installation:**
- Aircraft type: Mooney M20J
- Installation type: IFR GPS/Transponder
- Interface to GI 275: RS-232
- Audio panel: Garmin GMA 340
- Transponder code: Set during flight

### Garmin GI 275:

**Menu → Setup → Installation:**
- Display type: MFD
- Data source: GNX 375 via RS-232
- Traffic display: Enabled
- Weather display: Enabled

---

## TROUBLESHOOTING

### No Power to Unit:
- Check circuit breaker
- Verify voltage at connector pins
- Check ground connection continuity

### No GPS Data Display:
- Verify ARINC 429 or RS-232 connections
- Check shield grounds
- Verify baud rate and data format settings

### Autopilot Not Engaging:
- Check discrete connections (engage, disconnect)
- Verify servo connections
- Check Aspen autopilot configuration

### No Audio from GNX 375:
- Check audio connections to GMA 340
- Verify GMA 340 audio panel configuration
- Check PTT relay operation

### Transponder Not Responding:
- Verify antenna connections
- Check transponder code setting
- Verify altitude encoding

---

## FINAL NOTES

1. **All work must be performed by A&P mechanic or under A&P supervision**
2. **Log book entries required for all installations**
3. **STC or Form 337 required for major alterations**
4. **IFR certification required after avionics changes**
5. **Transponder/encoder certification required within 24 months**
6. **Follow all manufacturer installation instructions**
7. **Maintain documentation of all wire connections**

**This document provides general guidance. Always refer to the specific equipment installation manuals for detailed instructions and FAA-approved data.**

---

## RECOMMENDED NEXT STEPS

1. Review all manuals thoroughly
2. Create detailed wiring diagram specific to N204MM
3. Order all materials and connectors
4. Schedule installation with A&P if not performing yourself
5. Plan for avionics shop ground testing after installation
6. Schedule IFR certification flight

**Estimated Professional Installation Cost: $8,000-$15,000**  
**Estimated DIY Cost (materials only): $1,500-$2,500**  
**Estimated Time: 40-60 hours**

---

**Document Created: February 6, 2026**  
**For: N204MM Mooney M20J Avionics Upgrade**  
**By: Samantha (OpenClaw AI Assistant)**
