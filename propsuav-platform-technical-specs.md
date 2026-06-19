# PropsUAV Drone Launch Platform - Technical Specifications & Build Manual

## PROJECT OVERVIEW
Mobile drone spraying platform mounted on enclosed trailer with integrated liquid storage, generator power, and elevated pilot control station.

---

## TRAILER SPECIFICATIONS

### Exterior Dimensions
```
Total Length:    186" (163" + 23" V-nose)
Exterior Width:  84"
Interior Height: 83"
Payload:         4,700 lbs available
```

### Structural Components
- **Frame Material:** Steel tube frame (welded construction)
- **Interior Framing:** 1" × 1.5" steel beams, spaced 24" on-center
- **Roof:** Composite structure (existing)
- **Fenders:** Steel, 58-62" between fenders, 9" protrusion
- **Tires:** 205/75R15 (dual rear axle configuration)

### Door Openings
| Location | Width | Height | Position |
|----------|-------|--------|----------|
| Rear | 76" | 80" | Center rear |
| Right Side | 32" | 68" | 15" from front |

---

## INTERIOR LAYOUT

### Liquid Storage System

#### Primary Storage (Two IBC Tanks)
```
Position:         Over rear and mid axles (side-by-side)
Capacity Each:    275 gallons
Dimensions Each:  ~48"L × 40"W × 46"H
Material:         Plastic IBC containers with steel frames
Weight Each:      ~300 lbs (empty), ~2,300 lbs (full)
Total Weight:     ~4,600 lbs (full)
```

**IBC Tank Placement Layout (Top View):**
```
REAR (163" mark)
+────────────────────────────────────────+
│ IBC Tank #1      │      IBC Tank #2    │
│  (Left/Rear)     │    (Right/Rear)     │
│  275 gal         │     275 gal         │
│  48×40×46"       │     48×40×46"       │
│                  │                      │
│  Over left axle  │   Over right axle   │
+────────────────────────────────────────+
│                                         │
│      V-Nose Section (23")               │
│      Generator location (front-left)    │
│                                         │
+────────────────────────────────────────+
FRONT (V-nose)
```

#### Mixing/Application Tank
- **Capacity:** 60-75 gallons
- **Type:** Cone-bottom tank with drain valve
- **Position:** Front area (left side, forward of V-nose generator)
- **Dimensions:** ~36"H × 24" diameter
- **Material:** Polyethylene or similar
- **Purpose:** Secondary mixing and metering

### Power System

#### Generator
- **Location:** V-nose compartment (front-left)
- **Type:** Gasoline/propane portable generator
- **Power Output:** 5-7 kW recommended (for pump + accessories)
- **Fuel Tank:** Integrated or separate (check fuel space)
- **Exhaust Routing:** Through right-side wall (away from operator)
- **Battery Charging:** Integrated charger, 120V outlet access

#### Electrical System
- **Primary Outlets:** Two 120V duplex outlets on platform
- **Pump Power:** Dedicated 240V or 120V circuit (verify pump specs)
- **Lighting:** LED work lights on platform (optional)
- **Cable Routing:** Through conduit along interior beams

### Pumping & Distribution System

#### Main Supply Pump
- **Type:** Electric diaphragm or centrifugal pump
- **Flow Rate:** 10-15 GPM (verify with spraying equipment)
- **Power:** 120V or 240V (match generator capacity)
- **Suction:** From lower port of primary IBC tanks (via check valve)
- **Discharge:** To mixing tank or directly to spray nozzle

#### Plumbing Overview
```
IBC Tank #1 (Left)  ─┐
                      ├─→ [Check Valve] ──→ [Pump] ──→ Mixing Tank
IBC Tank #2 (Right) ─┘                                    │
                                                           ↓
                                                    [Filter] ──→ [Fill Nozzle on Platform]
                                                           ↓
                                          [Spray System/Equipment]
```

#### Hose Specifications
- **Fill Nozzle Location:** Center-front of launch platform (accessible to pilot)
- **Hose Size:** 1-1.5" diameter for supply line
- **Material:** Food-grade, UV-resistant polyurethane or similar
- **Routing:** Through sealed conduit along right interior wall to platform
- **Connections:** Quick-disconnect couplers at tank and nozzle for easy detachment

---

## LAUNCH PLATFORM ASSEMBLY

### Platform Structure

#### Overall Dimensions
- **Length:** 84" (exterior trailer width)
- **Width:** 60-72" (usable platform depth)
- **Height Above Roof:** 30-36" (pilot standing height reference)
- **Material:** Aluminum extrusion frame (lightweight structural)
- **Decking:** Aluminum or composite grating (non-slip)

#### Frame Construction
```
SIDE VIEW (Left/Driver Side):

          PILOT AREA (Center-Front)
         ╔════════════════════════════╗
         ║  Safety Railing            ║  ← 36" above existing roof
         ║  Mesh Drone Protection     ║
         ║                            ║
    ┌────╫─┐ ┌──────────────────────┐ │
    │    ║  │  Platform Deck        │ │  ← 30-36" above existing roof
    │    ║  │  (Aluminum extrusion) │ │
    │    ║  │                       │ │
    │    ║  └──────────────────────┘ │
    │    ║         STAIRS            ↓
    │    ║    (9" wide, welded steel)
    │    ║    (10 steps, 7" rise)
    │    ║
    │ COMPOSITE ROOF (83" interior height)
    │ ╔═══════════════════════════════════╗
    │ ║  1"×1.5" Steel Beams (24" spacing)║
    │ ╚═══════════════════════════════════╝
    └────────────────────────────────────┘
         FENDERS (58-62" between, 9" protrusion)
```

### Stair Assembly (Welded Steel)

#### Specifications
- **Width:** 9" (between inner stringers)
- **Height per Step:** 7" rise
- **Depth per Step:** 10" run (minimum)
- **Number of Steps:** 8-10 steps (depending on final platform height)
- **Material:** ASTM A36 structural steel, fully welded
- **Handrail:** 1.5" diameter steel tube, 36" above treads
- **Attachment:** Welded brackets to trailer fender and frame base

#### Step Details
```
           [Step Tread 10" deep]
        ┌──────────────────┐
        │ Steel flat plate │  ← 3/8" thick
        │  (or diamond plate)
        └──────────────────┘
              ↑
           7" RISE
              ↓
        ┌──────────────────┐
        │ Previous step    │
        └──────────────────┘

Stringer Profile (Side View):
        ╱╲╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱  ← Handrail attachment
       ╱  ╲════════════════
      ╱    ╲════════════════
     ╱      ╲════════════════  ← Welded tread
    ╱        ╲════════════════
   ╱          ╲════════════════
  ╱            ╲════════════════
 ╱              ╲
╱────────────────┘  ← Welded base bracket (to fender/frame)
```

#### Structural Tubes
- **Stringers (both sides):** 2"×4" rectangular tube, 3/16" wall
- **Treads:** 3/8" thick steel plate or expanded metal
- **Handrail:** 1.5" diameter steel pipe, Schedule 40
- **Welds:** Full penetration, FCAW or SMAW process
- **Paint/Finish:** Powder coat or epoxy enamel (rust protection)

---

## PLATFORM SUPERSTRUCTURE

### Pilot Standing Area (Front-Center)

#### Dimensions
- **Length:** 48" (front to back, or approximately 4 steps)
- **Width:** 36" (center of 84" platform)
- **Height Above Deck:** 36" (to top of safety railing)
- **Surface:** Non-slip aluminum grating or composite decking

#### Safety Railing
```
                    Safety Railing Assembly

                    ┌───────────────────┐
                    │  Upper Rail       │  ← 36" above deck
                    │  (1.5" diameter)  │
                    ├─────────────┬─────┤
                    │  Mesh       │ Mesh │  ← Drone protection screen
                    │  Screen     │     │     (1/2" or 3/8" holes)
                    │  (48"W×24"H)│     │
                    ├─────────────┴─────┤
                    │  Lower Rail       │  ← ~12" above deck
                    │  (1.5" diameter)  │
                    └───────────────────┘
```

**Railing Components:**
- **Upper Horizontal Rail:** 1.5" diameter steel tube
- **Lower Horizontal Rail:** 1.5" diameter steel tube (kick rail)
- **Vertical Supports:** 1" diameter steel pipe, 12" spacing
- **Mesh Infill:** 1/2" or 3/8" galvanized steel wire mesh (or polycarbonate)
- **Welds:** All connections fully welded

### Drone Positioning & Security

#### On-Platform Anchor Points
```
        PLATFORM TOP VIEW (Pilot Area)

    ┌──────────────────────────────┐
    │  ┌───────────────────────┐   │
    │  │  Mesh Drone Protection│   │  Anchor
    │  │  Box (removable)      │   │  Point
    │  └───┬──────────────────┬┘   │
    │      │                  │    │
    │   ● ANCHOR POINT #1     ●    │  ← Tie-down anchor
    │      (corner)           (corner)
    │                                │
    │      PILOT STANDING AREA      │
    │      (36" × 48")              │
    │                                │
    │   ● ANCHOR POINT #2     ●    │  ← Tie-down anchor
    │      (corner)           (corner)
    │      │                  │    │
    │  └───┴──────────────────┴┘   │
    │                                │
    └──────────────────────────────┘
```

**Anchor Point Specifications:**
- **Type:** Welded eye bolts or pad eyes (1/2" diameter minimum)
- **Locations:** Four corners of protective box (or platform perimeter)
- **Load Rating:** 500+ lbs each (verify with tie-down requirements)
- **Spacing:** 48" × 36" (matches platform dimensions)
- **Attachment:** Fully welded to platform frame, not bolted

#### Removable Protective Box
- **Purpose:** Drone security and weather protection during transport
- **Dimensions:** ~54"L × 42"W × 30"H (approximate, drone-dependent)
- **Material:** Aluminum frame + polycarbonate or composite panels
- **Mounting:** Quick-release pins or latches (removable in <5 minutes)
- **Ventilation:** Mesh vents for generator heat dissipation

---

## STRUCTURAL INTEGRATION & ATTACHMENTS

### Platform-to-Trailer Connection

#### Welded Base Connections
```
Cross-section: Platform attachment to trailer roof

Platform frame:    ══════════════╗
Gusseted plate:   ╱╱╱╱╱╱╱╱╱╱╱╱╱╱║
Roof beam:        ════════════════╪══════════════════
Welds:            ║ ║ ║ ║ ║ ║ ║ ║
                  FILLET WELDS (1/4" leg, continuous)
Interior frame:   ════════════════════════════════════
```

**Attachment Method:**
1. **Gusset Plates:** 1/2" thick steel, 12" × 12" (at each corner)
2. **Welds:** Full penetration fillet welds, 1/4" leg minimum
3. **Spacing:** Welded at four corners (front-left, front-right, rear-left, rear-right)
4. **Interior Support:** 1" × 1.5" beams run perpendicular to platform, creating triangulation

### Stair-to-Platform Connection

```
Top of stairs connects to platform front:

      ═════════════════════════
      │ Platform front beam    │
      ├────────────────────────┤
      │ Welded connection      │
      │ (½" gusset both sides) │
      ├────────────────────────┤
      │  Top step of stair     │
      │  (9" wide opening)     │
      └────────────────────────┘
         (allows foot transition)
```

---

## GENERATOR EXHAUST ROUTING

### Exhaust Path
```
TOP VIEW (Interior Layout):

    FRONT (V-Nose)
    ┌────────────────────────────┐
    │ Generator                  │
    │ [in V-nose, front-left]    │
    │                             │
    └─────────┬──────────────────┘
              │
              │ Exhaust Pipe (2" diameter)
              │ Stainless steel or aluminized
              │
    ┌─────────┴──────────────────────┐
    │         Routes through interior │
    │         along right-side wall   │
    │         (sealed conduit)        │
    └──────────────────────────┬──────┘
                               │
                       ╔═══════╩════════╗
                       ║ RIGHT-SIDE WALL║
                       ║  Opening: 3"   ║
                       ║  (12" from rear)
                       ╚════════════════╝
                               │
                               ↓
                    Exits 12" above roof level
                    (away from operator area)
```

**Specifications:**
- **Pipe Diameter:** 2-2.5" (match generator outlet)
- **Material:** Stainless steel or aluminized steel
- **Wall Penetration:** 3" diameter hole (sealed with heat-resistant gasket)
- **Termination:** 90° elbow pointing downward/rearward
- **Insulation:** High-temp wrap (if interior temperature < 6" clearance)
- **Support:** Clamps every 18" along routing path

---

## WEIGHT & CAPACITY ANALYSIS

### Component Weights (Approximate)

| Component | Empty | Full | Notes |
|-----------|-------|------|-------|
| IBC Tank #1 (275 gal) | 300 lbs | 2,300 lbs | @ 7.5 lbs/gal for water |
| IBC Tank #2 (275 gal) | 300 lbs | 2,300 lbs | @ 7.5 lbs/gal for water |
| Cone-bottom Tank (75 gal) | 100 lbs | 625 lbs | Additional mixing capacity |
| Platform Frame | 800 lbs | — | Aluminum structure |
| Stairs | 400 lbs | — | Welded steel |
| Generator (6 kW) | 300 lbs | — | Gasoline-powered |
| Protective Box | 200 lbs | — | Aluminum + panels |
| Drone (typical) | 50-100 lbs | — | DJI Agras or similar |
| **TOTALS** | **2,450 lbs** | **5,225+ lbs** | **Exceeds 4,700 lbs at full capacity** |

### Weight Distribution Recommendations
1. **Primary tanks (IBC) over rear axles:** Distributes 4,600 lbs evenly
2. **Generator in V-nose:** ~300 lbs forward (load balancing)
3. **Mixing tank off-center slightly** to maintain tongue weight (10-15% of total)
4. **Platform ballast:** Minimize load when liquid is at maximum

**⚠️ CRITICAL NOTE:** Full liquid capacity (550 gallons) exceeds payload. Recommend operating at 400-450 gallons maximum, or upgrade trailer if full capacity required.

---

## MATERIALS SUMMARY

### Structural Steel
- **Trailer Frame Beams:** 1" × 1.5" ASTM A36
- **Stair Stringers:** 2" × 4" rectangular tube, 3/16" wall
- **Handrails:** 1.5" diameter Schedule 40 pipe
- **Gusset Plates:** 1/2" thick ASTM A36 plate
- **All Welds:** E7018 (SMAW) or ER70S-6 (FCAW)

### Platform Frame
- **Extrusions:** 2" × 4" aluminum (6061-T6 alloy)
- **Fasteners:** Stainless steel bolts/rivets (corrosion resistance)
- **Decking:** Aluminum safety grating or composite deck plate
- **Finish:** Powder coat (satin or textured, UV-resistant)

### Protective & Finishing
- **Rope Sealing:** Spray foam or silicone caulk (exhaust penetration)
- **Mesh Screen:** Galvanized steel wire (1/2" or 3/8" holes)
- **Protective Coatings:** Epoxy primer + polyurethane topcoat (steel)

---

## ASSEMBLY SEQUENCE & NOTES

### Phase 1: Trailer Preparation
1. Clean and prepare roof surface (remove any debris)
2. Mark attachment points (four corners)
3. Install backing plates or reinforcement if needed (inspect existing beams)

### Phase 2: Platform Frame Fabrication (Off-Site)
1. Cut and fit aluminum extrusion
2. Assemble main frame (rectangular base)
3. Weld gusset plates at attachment points
4. Install decking and safety railing subassembly
5. Powder coat all components
6. Perform hydrostatic testing (if platform used as water containment)

### Phase 3: Stair Fabrication (Off-Site)
1. Cut and bend steel tube for stringers
2. Fit and tack all step treads
3. Full penetration welds on all connections
4. Verify step rise/run tolerance (±1/4")
5. Fabricate and weld mounting brackets
6. Powder coat or apply epoxy finish

### Phase 4: Platform Installation
1. Lift platform frame onto trailer roof (crane/equipment needed)
2. Align four corner attachment points
3. Tack-weld gusset plates to roof beams
4. Perform final alignment (level check)
5. Full penetration welds on all four corners
6. Mount and weld stair assembly at rear-left corner
7. Install safety railing and mesh screens

### Phase 5: Utilities Integration
1. Install generator in V-nose compartment
2. Route and secure exhaust pipe through right-side wall
3. Install pump and plumbing connections to IBC tanks
4. Pressure test all hose connections (50 PSI minimum)
5. Install fill nozzle on platform (center-front)
6. Route electrical conduit for 120V/240V power

### Phase 6: Testing & Safety Verification
1. Static load test on platform (500 lbs minimum, unloaded)
2. Full system test with water at operating pressure
3. Generator operation and exhaust isolation check
4. Stair integrity and load rating verification (500+ lbs per step)
5. Tie-down anchor strength verification
6. Mobility and braking function check (if trailer equipped)

---

## DIMENSIONAL CALLOUTS & REFERENCE

### Critical Measurement Points

**Stair Rise/Run:**
- Rise per step: 7.0"
- Run per step: 10.0"
- Total rise (10 steps): 70"
- Total run (9 treads): 90"

**Platform Heights (from ground):**
- Existing roof: ~58-60"
- Platform deck: ~90-96" (30-36" above roof)
- Railing top: ~126-132" (36" above deck)
- Pilot eye level (standing): ~120-126"

**Tank Clearances:**
- IBC tank clearance to roof: 12-18" (for access)
- Mixing tank access: 24" clearance on all sides
- Generator service access: 30" clearance (front)

**Door & Opening Alignments:**
- Right-side door (32"W × 68"H): Does NOT interfere with IBC tanks
- Rear door (76"W × 80"H): Full access for drone storage
- Platform stairs: Located at rear-left corner (does not block right-side door)

---

## OPERATIONAL SAFETY NOTES

⚠️ **Confined Space Risk:** Interior may accumulate toxic fumes if not properly ventilated. Generator exhaust MUST exit through right wall. Operator must use in open air only.

⚠️ **Load Capacity:** Platform is rated for pilot + drone (~150-200 lbs maximum). Do NOT exceed designed weight without structural analysis.

⚠️ **Electrical Hazard:** All 120V/240V circuits must have proper GFCI protection. Generator bonding required if operating near conductive surfaces.

⚠️ **Tire & Braking:** Verify trailer brakes are functional. 4,600+ lbs liquid load requires adequate braking distance.

⚠️ **Wind Loading:** Platform acts as a sail. DO NOT operate in sustained winds >20 mph. When parked, deploy wind brakes or lower protective box.

⚠️ **Tie-Down Requirements:** Platform and drone MUST be secured during transport. Verify all anchor points before towing.

---

## MAINTENANCE & INSPECTION SCHEDULE

| Component | Interval | Task |
|-----------|----------|------|
| Welds (stairs, platform) | Annual | Visual inspection, dye penetrant testing if cracks suspected |
| Fasteners (bolts, rivets) | Annual | Torque verification, replacement if loose |
| Mesh screen | 6 months | Check for corrosion, replace if rust present |
| Generator | Per manufacturer | Oil changes, filter replacement, fuel stabilization |
| Hose/Fittings | Annual | Pressure test (50 PSI), replace if leaks found |
| Trailer tires | Annual | Pressure check, tread depth, alignment |
| Protective box seals | 6 months | Check for weather degradation, reseal if necessary |

---

## REFERENCE DRAWINGS

**Included Visuals:**
1. Isometric 3D view (complete assembly)
2. Top-down plan view (interior layout)
3. Side elevation view (left/driver side)
4. Front elevation view
5. Detailed stair section
6. Interior layout detail (tanks, plumbing, electrical)

---

## BUILD TIMELINE ESTIMATE

- **Design & Drawings:** 1-2 weeks (complete)
- **Fabrication (off-site):** 4-6 weeks (platform + stairs)
- **Material Procurement:** 2-3 weeks (parallel with design)
- **Installation & Assembly:** 1-2 weeks (on-site)
- **Testing & Certification:** 1 week
- **Total:** 9-14 weeks (assuming no major rework)

---

## COST ESTIMATE (Preliminary)

| Category | Estimate |
|----------|----------|
| Structural Steel & Tubing | $2,000–$3,000 |
| Aluminum Extrusion & Decking | $1,500–$2,000 |
| Fabrication Labor | $3,000–$5,000 |
| Welding, Grinding, Finishing | $1,000–$2,000 |
| Powder Coat/Paint | $500–$1,000 |
| Fasteners, Hardware, Seals | $300–$500 |
| Installation Labor | $1,000–$2,000 |
| Plumbing, Hoses, Fittings | $400–$800 |
| Electrical (conduit, outlets, wiring) | $300–$600 |
| Miscellaneous/Contingency | $500–$1,000 |
| **TOTAL ESTIMATE** | **$10,500–$17,900** |

*(Excludes generator, pump, tanks, and drone)*

---

## CONCLUSION

This launch platform design provides a safe, ergonomic workstation for piloting high-capacity agricultural spray drones. The integrated storage, elevated vantage point, and protective systems minimize operational risk while maximizing efficiency.

**Key Advantages:**
✓ Full 84" platform width for stable drone launch/landing
✓ Elevated pilot position (30-36" above standard roof)
✓ Integrated 550-gallon liquid storage (over axles for weight distribution)
✓ Quick-access fill nozzle and drain systems
✓ Protective box for secure transport
✓ Generator-powered autonomous operation
✓ Welded steel construction for durability

---

*Document prepared for PropsUAV LLC. Designs subject to local building codes, trailer manufacturer specifications, and NFPA standards for propane/hazardous materials storage. Consult a professional engineer before final construction.*
