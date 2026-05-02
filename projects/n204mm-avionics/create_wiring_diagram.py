#!/usr/bin/env python3
"""
N204MM Avionics Wiring Diagram Generator
Creates visual wiring diagram for Mooney avionics upgrade
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')

# Title
ax.text(10, 13.5, 'N204MM Mooney M20J Avionics Wiring Diagram', 
        fontsize=20, fontweight='bold', ha='center')
ax.text(10, 13, 'Aspen EFD1000 E5 + Garmin GNX 375 + GI 275 MFD Integration',
        fontsize=14, ha='center', style='italic')

# Color scheme
color_new = '#90EE90'      # Light green for new equipment
color_existing = '#87CEEB'  # Light blue for existing equipment
color_power = '#FFB6C1'     # Light pink for power
color_removed = '#FFE4E1'   # Misty rose for removed equipment

# === NEW EQUIPMENT (Left side) ===

# Aspen EFD1000 E5
aspen_box = FancyBboxPatch((0.5, 9), 3.5, 2.5, boxstyle="round,pad=0.1",
                           facecolor=color_new, edgecolor='black', linewidth=2)
ax.add_patch(aspen_box)
ax.text(2.25, 10.8, 'ASPEN EFD1000 E5', fontsize=11, fontweight='bold', ha='center')
ax.text(2.25, 10.4, 'Primary Flight Display', fontsize=9, ha='center')
ax.text(2.25, 10, '37-pin D-sub', fontsize=8, ha='center', style='italic')
ax.text(2.25, 9.6, '• Attitude Indicator', fontsize=7, ha='center')
ax.text(2.25, 9.3, '• Directional Gyro/HSI', fontsize=7, ha='center')

# GNX 375
gnx_box = FancyBboxPatch((0.5, 6), 3.5, 2.5, boxstyle="round,pad=0.1",
                         facecolor=color_new, edgecolor='black', linewidth=2)
ax.add_patch(gnx_box)
ax.text(2.25, 7.8, 'GARMIN GNX 375', fontsize=11, fontweight='bold', ha='center')
ax.text(2.25, 7.4, 'GPS/Transponder Combo', fontsize=9, ha='center')
ax.text(2.25, 7, '25-pin D-sub', fontsize=8, ha='center', style='italic')
ax.text(2.25, 6.6, '• WAAS GPS Navigator', fontsize=7, ha='center')
ax.text(2.25, 6.3, '• ADS-B Out/In', fontsize=7, ha='center')

# GI 275 MFD
gi275_box = FancyBboxPatch((0.5, 3), 3.5, 2.5, boxstyle="round,pad=0.1",
                           facecolor=color_new, edgecolor='black', linewidth=2)
ax.add_patch(gi275_box)
ax.text(2.25, 4.8, 'GARMIN GI 275 MFD', fontsize=11, fontweight='bold', ha='center')
ax.text(2.25, 4.4, 'Multi-Function Display', fontsize=9, ha='center')
ax.text(2.25, 4, '15-pin D-sub', fontsize=8, ha='center', style='italic')
ax.text(2.25, 3.6, '• Traffic Display', fontsize=7, ha='center')
ax.text(2.25, 3.3, '• Weather Display', fontsize=7, ha='center')

# === EXISTING EQUIPMENT (Right side) ===

# GNS 430
gns430_box = FancyBboxPatch((16, 10), 3.5, 1.5, boxstyle="round,pad=0.1",
                            facecolor=color_existing, edgecolor='black', linewidth=2)
ax.add_patch(gns430_box)
ax.text(17.75, 11, 'GARMIN GNS 430', fontsize=11, fontweight='bold', ha='center')
ax.text(17.75, 10.5, 'GPS/COM/NAV', fontsize=9, ha='center')

# S-TEC 30 Autopilot
stec_box = FancyBboxPatch((16, 8), 3.5, 1.5, boxstyle="round,pad=0.1",
                          facecolor=color_existing, edgecolor='black', linewidth=2)
ax.add_patch(stec_box)
ax.text(17.75, 8.9, 'S-TEC 30', fontsize=11, fontweight='bold', ha='center')
ax.text(17.75, 8.4, 'Autopilot', fontsize=9, ha='center')

# GMA 340 Audio Panel
gma_box = FancyBboxPatch((16, 6), 3.5, 1.5, boxstyle="round,pad=0.1",
                         facecolor=color_existing, edgecolor='black', linewidth=2)
ax.add_patch(gma_box)
ax.text(17.75, 6.9, 'GARMIN GMA 340', fontsize=11, fontweight='bold', ha='center')
ax.text(17.75, 6.4, 'Audio Panel', fontsize=9, ha='center')

# LOC/GS Receiver
locgs_box = FancyBboxPatch((16, 4), 3.5, 1.5, boxstyle="round,pad=0.1",
                           facecolor=color_existing, edgecolor='black', linewidth=2)
ax.add_patch(locgs_box)
ax.text(17.75, 4.9, 'GARMIN LOC/GS', fontsize=11, fontweight='bold', ha='center')
ax.text(17.75, 4.4, 'Receiver', fontsize=9, ha='center')

# KY197 Comm
ky197_box = FancyBboxPatch((16, 2), 3.5, 1.5, boxstyle="round,pad=0.1",
                           facecolor=color_existing, edgecolor='black', linewidth=2)
ax.add_patch(ky197_box)
ax.text(17.75, 2.9, 'KING KY197', fontsize=11, fontweight='bold', ha='center')
ax.text(17.75, 2.4, 'Comm Radio', fontsize=9, ha='center')

# === POWER DISTRIBUTION (Center Top) ===

power_box = FancyBboxPatch((8, 11.5), 4, 1.2, boxstyle="round,pad=0.1",
                           facecolor=color_power, edgecolor='red', linewidth=2)
ax.add_patch(power_box)
ax.text(10, 12.5, 'POWER DISTRIBUTION', fontsize=11, fontweight='bold', ha='center')
ax.text(10, 12.1, 'Circuit Breakers: CB1(5A) CB2(5A) CB3(5A) CB4(3A)', fontsize=8, ha='center')

ground_box = FancyBboxPatch((8, 10), 4, 1, boxstyle="round,pad=0.1",
                            facecolor='lightgray', edgecolor='black', linewidth=2)
ax.add_patch(ground_box)
ax.text(10, 10.5, 'GROUND BUS', fontsize=11, fontweight='bold', ha='center')

# === ANTENNAS (Bottom Center) ===

gps_ant = FancyBboxPatch((7, 0.3), 1.8, 0.8, boxstyle="round,pad=0.05",
                         facecolor='lightyellow', edgecolor='black', linewidth=1)
ax.add_patch(gps_ant)
ax.text(7.9, 0.7, 'GPS ANT', fontsize=8, fontweight='bold', ha='center')

xpdr_ant1 = FancyBboxPatch((9.2, 0.3), 1.8, 0.8, boxstyle="round,pad=0.05",
                           facecolor='lightyellow', edgecolor='black', linewidth=1)
ax.add_patch(xpdr_ant1)
ax.text(10.1, 0.7, 'XPDR ANT1', fontsize=8, fontweight='bold', ha='center')

xpdr_ant2 = FancyBboxPatch((11.4, 0.3), 1.8, 0.8, boxstyle="round,pad=0.05",
                           facecolor='lightyellow', edgecolor='black', linewidth=1)
ax.add_patch(xpdr_ant2)
ax.text(12.3, 0.7, 'XPDR ANT2', fontsize=8, fontweight='bold', ha='center')

# === REMOVED EQUIPMENT (Bottom Left) ===

removed_label = ax.text(2.25, 1.8, 'REMOVED EQUIPMENT', fontsize=10, 
                        fontweight='bold', ha='center', style='italic', color='red')

removed_box1 = FancyBboxPatch((0.5, 0.8), 1.5, 0.6, boxstyle="round,pad=0.05",
                              facecolor=color_removed, edgecolor='red', linewidth=1, linestyle='--')
ax.add_patch(removed_box1)
ax.text(1.25, 1.1, 'KNS80', fontsize=8, ha='center', style='italic')

removed_box2 = FancyBboxPatch((2.2, 0.8), 1.5, 0.6, boxstyle="round,pad=0.05",
                              facecolor=color_removed, edgecolor='red', linewidth=1, linestyle='--')
ax.add_patch(removed_box2)
ax.text(2.95, 1.1, 'KT76A', fontsize=8, ha='center', style='italic')

removed_box3 = FancyBboxPatch((0.5, 0.1), 1.5, 0.6, boxstyle="round,pad=0.05",
                              facecolor=color_removed, edgecolor='red', linewidth=1, linestyle='--')
ax.add_patch(removed_box3)
ax.text(1.25, 0.4, 'Vacuum AI', fontsize=8, ha='center', style='italic')

removed_box4 = FancyBboxPatch((2.2, 0.1), 1.5, 0.6, boxstyle="round,pad=0.05",
                              facecolor=color_removed, edgecolor='red', linewidth=1, linestyle='--')
ax.add_patch(removed_box4)
ax.text(2.95, 0.4, 'Vacuum DG', fontsize=8, ha='center', style='italic')

# === CONNECTION ARROWS ===

# Define arrow style
arrow_style = dict(arrowstyle='->', lw=1.5)
arrow_style_power = dict(arrowstyle='->', lw=2, color='red')
arrow_style_ground = dict(arrowstyle='->', lw=1.5, color='black', linestyle='--')
arrow_style_data = dict(arrowstyle='->', lw=1.2, color='blue')
arrow_style_coax = dict(arrowstyle='->', lw=1.5, color='orange')

# Power connections (red arrows)
ax.annotate('', xy=(2.25, 11.5), xytext=(10, 11.5), arrowprops=arrow_style_power)
ax.text(6, 11.7, '+28V', fontsize=7, ha='center', color='red', fontweight='bold')

ax.annotate('', xy=(2.25, 8.5), xytext=(10, 11.5), arrowprops=arrow_style_power)
ax.annotate('', xy=(2.25, 5.5), xytext=(10, 11.5), arrowprops=arrow_style_power)

# Ground connections (black dashed)
ax.annotate('', xy=(2.25, 9), xytext=(10, 10.2), arrowprops=arrow_style_ground)
ax.annotate('', xy=(2.25, 6), xytext=(10, 10.2), arrowprops=arrow_style_ground)
ax.annotate('', xy=(2.25, 3), xytext=(10, 10.2), arrowprops=arrow_style_ground)

# ARINC 429: GNS 430 -> Aspen (blue)
arrow1 = FancyArrowPatch((16, 10.75), (4, 10.5), 
                         arrowstyle='->', mutation_scale=15, lw=1.5, color='blue')
ax.add_patch(arrow1)
ax.text(10, 10.8, 'ARINC 429', fontsize=7, ha='center', color='blue', fontweight='bold')

# RS-232: GNX 375 <-> GI 275 (blue)
arrow2 = FancyArrowPatch((2.25, 6), (2.25, 5.5),
                         arrowstyle='<->', mutation_scale=15, lw=1.5, color='blue')
ax.add_patch(arrow2)
ax.text(3.2, 5.75, 'RS-232', fontsize=7, ha='left', color='blue', fontweight='bold')

# Autopilot: Aspen -> S-TEC 30 (green)
arrow3 = FancyArrowPatch((4, 9.75), (16, 8.75),
                         arrowstyle='->', mutation_scale=15, lw=1.5, color='green')
ax.add_patch(arrow3)
ax.text(10, 9.5, 'AP Control', fontsize=7, ha='center', color='green', fontweight='bold')

# Audio: GNX 375 -> GMA 340 (purple)
arrow4 = FancyArrowPatch((4, 7.25), (16, 6.75),
                         arrowstyle='->', mutation_scale=15, lw=1.5, color='purple')
ax.add_patch(arrow4)
ax.text(10, 7.3, 'Audio', fontsize=7, ha='center', color='purple', fontweight='bold')

# LOC/GS: Receiver -> GNX 375 (brown)
arrow5 = FancyArrowPatch((16, 4.75), (4, 7),
                         arrowstyle='->', mutation_scale=15, lw=1.5, color='brown')
ax.add_patch(arrow5)
ax.text(10, 5.5, 'LOC/GS', fontsize=7, ha='center', color='brown', fontweight='bold')

# Antenna connections (orange, coax)
# GPS Antenna -> GNX 375
arrow6 = FancyArrowPatch((7.9, 1.1), (2.25, 6),
                         arrowstyle='->', mutation_scale=15, lw=1.5, color='orange', linestyle=':')
ax.add_patch(arrow6)
ax.text(5, 3.5, 'RG-400', fontsize=7, ha='center', color='orange', style='italic')

# Transponder Antennas -> GNX 375
arrow7 = FancyArrowPatch((10.1, 1.1), (2.25, 6),
                         arrowstyle='->', mutation_scale=15, lw=1.5, color='orange', linestyle=':')
ax.add_patch(arrow7)

arrow8 = FancyArrowPatch((12.3, 1.1), (2.25, 6),
                         arrowstyle='->', mutation_scale=15, lw=1.5, color='orange', linestyle=':')
ax.add_patch(arrow8)

# === LEGEND ===

legend_x = 14.5
legend_y = 1.5

ax.text(legend_x, legend_y + 0.4, 'LEGEND:', fontsize=10, fontweight='bold')

# New equipment
rect1 = patches.Rectangle((legend_x, legend_y), 0.3, 0.2, facecolor=color_new, edgecolor='black')
ax.add_patch(rect1)
ax.text(legend_x + 0.4, legend_y + 0.1, 'New Equipment', fontsize=8, va='center')

# Existing equipment
rect2 = patches.Rectangle((legend_x, legend_y - 0.3), 0.3, 0.2, facecolor=color_existing, edgecolor='black')
ax.add_patch(rect2)
ax.text(legend_x + 0.4, legend_y - 0.2, 'Existing Equipment', fontsize=8, va='center')

# Removed equipment
rect3 = patches.Rectangle((legend_x, legend_y - 0.6), 0.3, 0.2, facecolor=color_removed, 
                          edgecolor='red', linestyle='--')
ax.add_patch(rect3)
ax.text(legend_x + 0.4, legend_y - 0.5, 'Removed Equipment', fontsize=8, va='center')

# Connection types
ax.plot([legend_x, legend_x + 0.3], [legend_y - 0.9, legend_y - 0.9], 'r-', lw=2)
ax.text(legend_x + 0.4, legend_y - 0.9, 'Power (+28V)', fontsize=8, va='center')

ax.plot([legend_x, legend_x + 0.3], [legend_y - 1.1, legend_y - 1.1], 'k--', lw=1.5)
ax.text(legend_x + 0.4, legend_y - 1.1, 'Ground', fontsize=8, va='center')

ax.plot([legend_x, legend_x + 0.3], [legend_y - 1.3, legend_y - 1.3], 'b-', lw=1.5)
ax.text(legend_x + 0.4, legend_y - 1.3, 'Digital Data', fontsize=8, va='center')

ax.plot([legend_x, legend_x + 0.3], [legend_y - 1.5, legend_y - 1.5], color='orange', 
        linestyle=':', lw=1.5)
ax.text(legend_x + 0.4, legend_y - 1.5, 'Coaxial (Antennas)', fontsize=8, va='center')

# === NOTES ===

notes_text = """INSTALLATION NOTES:
• All power through individual circuit breakers
• Aspen requires dual power (primary + backup)
• All serial connections use shielded cable
• Shields grounded at ONE end only
• Antennas require RG-400 coaxial cable
• GPS antenna must be STC-compliant
• Professional installation recommended
• IFR certification required after install"""

ax.text(5.5, 2.2, notes_text, fontsize=7, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Footer
ax.text(10, 0.1, 'Created: February 6, 2026 | Aircraft: N204MM Mooney M20J | By: Samantha (OpenClaw AI)', 
        fontsize=7, ha='center', style='italic', color='gray')

# Save the figure
plt.tight_layout()
plt.savefig('/Users/sam/.openclaw/workspace/projects/n204mm-avionics/wiring-diagram.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Wiring diagram saved: wiring-diagram.png")
plt.close()

# Create a second diagram - Simplified Connection Overview
fig2, ax2 = plt.subplots(1, 1, figsize=(16, 10))
ax2.set_xlim(0, 16)
ax2.set_ylim(0, 10)
ax2.axis('off')

ax2.text(8, 9.5, 'N204MM Simplified Connection Overview', 
         fontsize=18, fontweight='bold', ha='center')

# Simplified boxes in a clearer layout
boxes_simple = [
    # (x, y, width, height, label, color)
    (1, 6, 2.5, 1.5, 'ASPEN\nEFD1000 E5\nP1: 37-pin', color_new),
    (1, 4, 2.5, 1.5, 'GNX 375\nGPS/XPDR\nP1: 25-pin', color_new),
    (1, 2, 2.5, 1.5, 'GI 275\nMFD\nP1: 15-pin', color_new),
    
    (6, 7, 2, 1.2, 'Power Bus\n4x Breakers', color_power),
    (6, 5.5, 2, 1, 'Ground Bus', 'lightgray'),
    
    (12, 7, 2.5, 1.2, 'GNS 430\nGPS/COM', color_existing),
    (12, 5.5, 2.5, 1, 'S-TEC 30\nAutopilot', color_existing),
    (12, 4.2, 2.5, 1, 'GMA 340\nAudio', color_existing),
    (12, 2.9, 2.5, 1, 'LOC/GS\nReceiver', color_existing),
]

for x, y, w, h, label, color in boxes_simple:
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                         facecolor=color, edgecolor='black', linewidth=2)
    ax2.add_patch(box)
    ax2.text(x + w/2, y + h/2, label, fontsize=10, fontweight='bold', 
             ha='center', va='center')

# Connection labels with arrows (simplified)
connections = [
    # (x1, y1, x2, y2, label, color)
    (3.5, 6.75, 12, 7.6, 'ARINC 429\nGPS Data', 'blue'),
    (2.25, 6, 2.25, 5.5, 'RS-232', 'blue'),
    (3.5, 6.5, 12, 6, 'Autopilot\nControl', 'green'),
    (3.5, 4.75, 12, 4.7, 'Audio +\nPTT', 'purple'),
    (12, 3.4, 3.5, 4.5, 'LOC/GS\nSignals', 'brown'),
]

for x1, y1, x2, y2, label, color in connections:
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->', mutation_scale=20, lw=2, color=color)
    ax2.add_patch(arrow)
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    ax2.text(mid_x, mid_y + 0.2, label, fontsize=8, ha='center', 
            color=color, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Antenna connections at bottom
ant_y = 0.8
ax2.text(2.25, ant_y + 0.6, 'ANTENNAS (Coaxial RG-400)', fontsize=10, 
        fontweight='bold', ha='center')

antennas_simple = [
    (1, ant_y, 'GPS\nAntenna'),
    (2.5, ant_y, 'XPDR\nAnt 1'),
    (4, ant_y, 'XPDR\nAnt 2'),
]

for x, y, label in antennas_simple:
    ant_box = FancyBboxPatch((x, y), 1.2, 0.5, boxstyle="round,pad=0.05",
                            facecolor='lightyellow', edgecolor='orange', linewidth=2)
    ax2.add_patch(ant_box)
    ax2.text(x + 0.6, y + 0.25, label, fontsize=7, ha='center', va='center')
    
    # Arrow from antenna to GNX 375
    ax2.annotate('', xy=(2.25, 4), xytext=(x + 0.6, y + 0.5),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='orange', linestyle=':'))

# Power distribution arrows
for unit_y in [6.75, 4.75, 2.75]:
    ax2.annotate('', xy=(2.25, unit_y), xytext=(6, 7.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    ax2.annotate('', xy=(2.25, unit_y - 0.3), xytext=(7, 6),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='black', linestyle='--'))

ax2.text(4.5, 7.3, 'Power', fontsize=7, color='red', fontweight='bold')
ax2.text(4.5, 5.8, 'Ground', fontsize=7, color='black')

# Summary box
summary = """KEY CONNECTIONS:
✓ Aspen ← GNS 430 (ARINC 429)
✓ Aspen → S-TEC 30 (AP Control)
✓ GNX 375 ↔ GI 275 (RS-232)
✓ GNX 375 → GMA 340 (Audio)
✓ GNX 375 ← LOC/GS (ILS Signals)
✓ GNX 375 ← 3x Antennas (Coax)"""

ax2.text(11, 1.2, summary, fontsize=8, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

ax2.text(8, 0.1, 'Simplified Overview | N204MM Mooney M20J | February 6, 2026', 
        fontsize=7, ha='center', style='italic', color='gray')

plt.tight_layout()
plt.savefig('/Users/sam/.openclaw/workspace/projects/n204mm-avionics/wiring-diagram-simple.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Simplified diagram saved: wiring-diagram-simple.png")
plt.close()

print("\n✅ Both wiring diagrams created successfully!")
print("📁 Location: /Users/sam/.openclaw/workspace/projects/n204mm-avionics/")
print("   • wiring-diagram.png (detailed)")
print("   • wiring-diagram-simple.png (overview)")
