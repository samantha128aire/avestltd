# N204MM Avionics Wiring Connection Matrix

**Complete Wire-by-Wire Connection Guide**

---

## POWER DISTRIBUTION CONNECTIONS

### Circuit Breakers Required:
- CB1: Aspen EFD1000 Primary - 5A
- CB2: Aspen EFD1000 Backup - 5A
- CB3: Garmin GNX 375 - 5A
- CB4: Garmin GI 275 - 3A

---

## ASPEN EFD1000 E5 CONNECTIONS (37-pin D-sub P1)

| Pin | Wire Color | Gauge | Destination | Destination Pin | Function | Notes |
|-----|------------|-------|-------------|-----------------|----------|-------|
| 1 | RED | 20 AWG | Circuit Breaker CB1 | Hot Side | +28V Primary Power | From aircraft main bus |
| 2 | BLACK | 20 AWG | Ground Bus | N/A | Ground Return | Primary ground |
| 3 | RED | 20 AWG | Circuit Breaker CB2 | Hot Side | +28V Backup Power | From aircraft backup bus |
| 4 | BLACK | 20 AWG | Ground Bus | N/A | Ground Return | Primary ground |
| 5 | WHITE | 22 AWG | Panel Dimmer | N/A | Lighting Dimming | Optional |
| 6 | BARE/SHIELD | N/A | Chassis Ground | N/A | Shield Ground | Connect to aircraft frame |
| 7 | YELLOW | 22 AWG | S-TEC 30 | Disconnect Input | AP Disconnect | From disconnect switch |
| 8 | GREEN | 22 AWG | S-TEC 30 | Engage Input | AP Engage | From engage button |
| 9 | BLUE/WHITE | 22 AWG | S-TEC 30 | Roll Servo Input | AP Roll Command | Shielded pair |
| 10 | BLACK | 22 AWG | S-TEC 30 | Roll Ground | Roll Return | Shield drain |
| 11 | GREEN/WHITE | 22 AWG | S-TEC 30 | Pitch Servo Input | AP Pitch Command | Shielded pair |
| 12 | BLACK | 22 AWG | S-TEC 30 | Pitch Ground | Pitch Return | Shield drain |
| 13 | ORANGE | 22 AWG | S-TEC 30 | GPSS Input | GPS Steering | To GPSS switch |
| 14 | BLACK | 22 AWG | Ground Bus | N/A | GPSS Ground | Ground return |
| 15 | BLUE | 22 AWG | GNS 430 | ARINC HI Out | ARINC 429 Data+ | Twisted shielded pair |
| 16 | BLUE/WHITE | 22 AWG | GNS 430 | ARINC LO Out | ARINC 429 Data- | Twisted shielded pair |
| 17 | BARE/SHIELD | N/A | Pin 6 | N/A | Shield Drain | One end only |
| 18 | N/A | N/A | Pitot Line | N/A | Pitot Pressure | Pneumatic tube |
| 19 | N/A | N/A | Static Line | N/A | Static Pressure | Pneumatic tube |
| 20 | RED | 24 AWG | OAT Probe | + Terminal | OAT Sensor + | Shielded pair |
| 21 | BLACK | 24 AWG | OAT Probe | - Terminal | OAT Sensor - | Shielded pair |
| 22-24 | N/A | N/A | Not Used | N/A | Reserved | Leave open |
| 25 | ORANGE | 22 AWG | Warning Light | + Terminal | Annunciator + | Optional |
| 26 | BLACK | 22 AWG | Ground Bus | N/A | Annunciator - | Optional |
| 27-35 | N/A | N/A | Not Used | N/A | Reserved | Leave open |
| 36 | GREEN | 22 AWG | GNS 430 | RS-232 TX | Serial Data Out | Shielded |
| 37 | BLUE | 22 AWG | GNS 430 | RS-232 RX | Serial Data In | Shielded |

---

## GARMIN GNX 375 CONNECTIONS (25-pin D-sub P1)

| Pin | Wire Color | Gauge | Destination | Destination Pin | Function | Notes |
|-----|------------|-------|-------------|-----------------|----------|-------|
| 1 | RED | 20 AWG | Circuit Breaker CB3 | Hot Side | +28V Primary Power | From aircraft main bus |
| 2 | BLACK | 20 AWG | Ground Bus | N/A | Ground Return | Primary ground |
| 3 | BARE/SHIELD | N/A | Chassis Ground | N/A | Shield Ground | Connect to aircraft frame |
| 4 | GREEN | 22 AWG | GI 275 | Pin 4 | RS-232 TX to GI 275 | Shielded |
| 5 | BLUE | 22 AWG | GI 275 | Pin 3 | RS-232 RX from GI 275 | Shielded |
| 6 | BARE/SHIELD | N/A | Pin 3 | N/A | Shield Drain | One end only |
| 7 | WHITE | 22 AWG | GMA 340 | Audio Input + | Audio Out + | Shielded pair |
| 8 | BLACK | 22 AWG | GMA 340 | Audio Ground | Audio Out - | Audio return |
| 9 | YELLOW | 22 AWG | GMA 340 | GNX COM PTT | PTT Input | From audio panel relay |
| 10 | BLACK | 22 AWG | Ground Bus | N/A | PTT Ground | Ground return |
| 11 | ORANGE | 22 AWG | Aspen/Other | ARINC Input | ARINC 429 HI | Twisted shielded pair |
| 12 | ORANGE/WHITE | 22 AWG | Aspen/Other | ARINC Input | ARINC 429 LO | Twisted shielded pair |
| 13 | BARE/SHIELD | N/A | Pin 3 | N/A | Shield Drain | One end only |
| 14 | BLUE | 22 AWG | LOC/GS Receiver | LOC + Out | Localizer + | Shielded pair |
| 15 | BLUE/WHITE | 22 AWG | LOC/GS Receiver | LOC Ground | Localizer - | Shielded pair |
| 16 | GREEN | 22 AWG | LOC/GS Receiver | GS + Out | Glideslope + | Shielded pair |
| 17 | GREEN/WHITE | 22 AWG | LOC/GS Receiver | GS Ground | Glideslope - | Shielded pair |
| 18-25 | N/A | N/A | Reserved | N/A | Configuration | See manual |

### GNX 375 Antenna Connections (Coaxial - Not on D-sub)

| Connector | Cable Type | Destination | Function | Notes |
|-----------|------------|-------------|----------|-------|
| GPS ANT | RG-400 50Ω | GPS Antenna | GPS Receive | TNC connector, roof mount |
| XPDR ANT1 | RG-400 50Ω | Bottom Antenna | Transponder Primary | TNC connector, existing |
| XPDR ANT2 | RG-400 50Ω | Top Antenna | Transponder Diversity | TNC connector, recommended |

---

## GARMIN GI 275 MFD CONNECTIONS (15-pin D-sub P1)

| Pin | Wire Color | Gauge | Destination | Destination Pin | Function | Notes |
|-----|------------|-------|-------------|-----------------|----------|-------|
| 1 | RED | 22 AWG | Circuit Breaker CB4 | Hot Side | +28V Primary Power | From aircraft main bus |
| 2 | BLACK | 22 AWG | Ground Bus | N/A | Ground Return | Primary ground |
| 3 | GREEN | 22 AWG | GNX 375 | Pin 5 | RS-232 TX to GNX 375 | Shielded |
| 4 | BLUE | 22 AWG | GNX 375 | Pin 4 | RS-232 RX from GNX 375 | Shielded |
| 5 | BARE/SHIELD | N/A | Chassis Ground | N/A | Shield Ground | Connect to aircraft frame |
| 6 | WHITE | 22 AWG | Panel Dimmer | N/A | Lighting Dimming | Optional |
| 7-15 | N/A | N/A | Reserved | N/A | CAN Bus/Config | See manual for options |

---

## INTEGRATION WITH EXISTING EQUIPMENT

### Garmin GNS 430 Connections (Existing Unit - New Connections)

| GNS 430 Pin | Function | Wire Color | Gauge | New Destination | Destination Pin | Notes |
|-------------|----------|------------|-------|-----------------|-----------------|-------|
| ARINC HI Out | ARINC 429 + | BLUE | 22 AWG | Aspen EFD1000 | P1-15 | Twisted shielded pair |
| ARINC LO Out | ARINC 429 - | BLUE/WHITE | 22 AWG | Aspen EFD1000 | P1-16 | Twisted shielded pair |
| RS-232 TX | Serial Out | GREEN | 22 AWG | Aspen EFD1000 | P1-37 | Optional - shielded |
| RS-232 RX | Serial In | BLUE | 22 AWG | Aspen EFD1000 | P1-36 | Optional - shielded |

### S-TEC 30 Autopilot Connections (Existing Unit - New Connections)

| S-TEC Pin/Function | Wire Color | Gauge | New Source | Source Pin | Notes |
|--------------------|------------|-------|------------|------------|-------|
| Disconnect Input | YELLOW | 22 AWG | Aspen EFD1000 | P1-7 | From Aspen |
| Engage Input | GREEN | 22 AWG | Aspen EFD1000 | P1-8 | From Aspen |
| Roll Servo Input | BLUE/WHITE | 22 AWG | Aspen EFD1000 | P1-9 | Shielded pair |
| Roll Ground | BLACK | 22 AWG | Aspen EFD1000 | P1-10 | Shield drain |
| Pitch Servo Input | GREEN/WHITE | 22 AWG | Aspen EFD1000 | P1-11 | Shielded pair |
| Pitch Ground | BLACK | 22 AWG | Aspen EFD1000 | P1-12 | Shield drain |
| GPSS Input | ORANGE | 22 AWG | Aspen EFD1000 | P1-13 | GPS steering |
| GPSS Ground | BLACK | 22 AWG | Aspen EFD1000 | P1-14 | Ground return |

### Garmin GMA 340 Audio Panel Connections (Existing Unit - New Connections)

| GMA 340 Function | Wire Color | Gauge | New Source | Source Pin | Notes |
|------------------|------------|-------|------------|------------|-------|
| GNX Audio Input + | WHITE | 22 AWG | GNX 375 | P1-7 | Shielded pair |
| GNX Audio Ground | BLACK | 22 AWG | GNX 375 | P1-8 | Audio return |
| GNX COM PTT Relay | YELLOW | 22 AWG | GNX 375 | P1-9 | PTT control |
| PTT Ground | BLACK | 22 AWG | GNX 375 | P1-10 | Ground return |

### Garmin LOC/GS Receiver (Existing Unit - Reconnect)

**Current Connection:** KNS80 (being removed)  
**New Connection:** GNX 375

| LOC/GS Function | Wire Color | Gauge | New Destination | Destination Pin | Notes |
|-----------------|------------|-------|-----------------|-----------------|-------|
| Localizer + | BLUE | 22 AWG | GNX 375 | P1-14 | Disconnect from KNS80 |
| Localizer - | BLUE/WHITE | 22 AWG | GNX 375 | P1-15 | Shielded pair |
| Glideslope + | GREEN | 22 AWG | GNX 375 | P1-16 | Disconnect from KNS80 |
| Glideslope - | GREEN/WHITE | 22 AWG | GNX 375 | P1-17 | Shielded pair |

**Note:** King KI206 LOC/GS remains connected to GNS 430 for backup ILS capability.

---

## WIRE SHOPPING LIST

### Power Wiring
- RED 20 AWG MIL-W-22759: 25 feet (power runs to breakers)
- BLACK 20 AWG MIL-W-22759: 15 feet (ground returns)
- WHITE 22 AWG MIL-W-22759: 10 feet (lighting dimming - optional)

### Shielded Signal Wiring
- BLUE 22 AWG Shielded Twisted Pair: 30 feet (ARINC 429, serial data)
- GREEN 22 AWG Shielded: 25 feet (serial TX, LOC/GS)
- ORANGE 22 AWG Shielded: 15 feet (ARINC 429)

### Discrete Signal Wiring
- YELLOW 22 AWG: 15 feet (AP disconnect, PTT)
- WHITE 22 AWG Shielded: 10 feet (audio)
- Various colors 22 AWG: 20 feet (autopilot servos)
- BLACK 22 AWG: 40 feet (grounds and returns)

### Antenna Coaxial Cable
- RG-400 50Ω: 30-50 feet (GPS antenna + transponder antennas)

### Connectors Required
- 37-pin D-sub male (for Aspen harness)
- 25-pin D-sub male (for GNX 375 harness)
- 15-pin D-sub male (for GI 275 harness)
- D-sub pins (crimp or solder type)
- D-sub backshells with strain relief
- TNC connectors for coax (3x)

---

## WIRE BUNDLING GUIDE

### Bundle 1: Power Distribution
- All RED power wires (CB1, CB2, CB3, CB4 to units)
- All BLACK ground wires (from units to ground bus)
- Route through dedicated power conduit

### Bundle 2: Aspen EFD1000 Signals
- ARINC 429 from GNS 430 (BLUE/BLUE-WHITE pair)
- RS-232 from GNS 430 (GREEN/BLUE pair)
- Autopilot discretes to S-TEC (YELLOW/GREEN)
- Autopilot servos to S-TEC (BLUE-WHITE/GREEN-WHITE pairs)
- GPSS to S-TEC (ORANGE)

### Bundle 3: GNX 375 Signals
- RS-232 to GI 275 (GREEN/BLUE pair)
- Audio to GMA 340 (WHITE/BLACK pair)
- PTT to GMA 340 (YELLOW)
- ARINC 429 out (ORANGE/ORANGE-WHITE pair)
- LOC/GS from receiver (BLUE/GREEN pairs)

### Bundle 4: Antennas (Separate Routing)
- GPS antenna coax (RG-400)
- Transponder antenna 1 coax (RG-400)
- Transponder antenna 2 coax (RG-400)
- Keep away from signal wires
- Keep away from power wires

---

## GROUNDING SUMMARY

| Equipment | Ground Type | Wire Gauge | Connection Point |
|-----------|-------------|------------|------------------|
| Aspen EFD1000 | Power Ground | 20 AWG | Pins 2 & 4 to ground bus |
| Aspen EFD1000 | Chassis Ground | N/A | Pin 6 to aircraft frame |
| GNX 375 | Power Ground | 20 AWG | Pin 2 to ground bus |
| GNX 375 | Chassis Ground | N/A | Pin 3 to aircraft frame |
| GI 275 | Power Ground | 22 AWG | Pin 2 to ground bus |
| GI 275 | Chassis Ground | N/A | Pin 5 to aircraft frame |
| Shield Drains | Signal Ground | N/A | One end only to chassis |

**Critical:** All equipment chassis grounds must connect to primary aircraft ground point. No ground loops!

---

## TESTING CHECKLIST

### Pre-Power Checks (Multimeter Required)

- [ ] Continuity: Pin 1 (power) on each unit to respective circuit breaker
- [ ] Continuity: Pin 2 (ground) on each unit to ground bus (<0.1Ω)
- [ ] No shorts: Power pins to ground (should be open/infinite resistance)
- [ ] No shorts: Signal pins to ground (except ground pins)
- [ ] Shield continuity: Verify shields connected at ONE end only
- [ ] Voltage check: 28V ±2V at each power pin before connecting units

### Power-On Sequence

1. [ ] Power Aspen EFD1000 - verify display boot
2. [ ] Power GNX 375 - verify GPS acquisition
3. [ ] Power GI 275 - verify communication with GNX 375
4. [ ] Test GNS 430 ARINC output to Aspen
5. [ ] Test autopilot engage/disconnect
6. [ ] Test audio from GNX 375 to GMA 340
7. [ ] Test transponder (ground test mode only)

---

**Document Created: February 6, 2026**  
**Aircraft: N204MM Mooney M20J**  
**By: Samantha (OpenClaw AI Assistant)**
