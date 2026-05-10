# Experiment 4: Flood Inundation

DEM-based flood inundation simulation with flood extent visualization and animation.

## Overview

- **Synthetic DEM generation** (`flood_inundation.py`): 100×100 grid, elevation 30–80 m, slope + noise
- **Flood calculation**:
  - `calculate_flood(dem, water_level)` — flooded mask, depth array, flooded percentage
- **Visualization** (3-panel plot): original DEM, flood overlay, depth heatmap
  - `flood_extent_40m.png`, `flood_extent_50m.png`
- **Flood curve**: water level vs flooded percentage (`flood_curve.png`)
- **Physical validation** (5 checks):
  1. Flooded area increases monotonically with water level
  2. Max depth = water level − min(DEM)
  3. Percentage within 0–100%
  4. Water below min(DEM) → 0% flooded
  5. Water above max(DEM) → 100% flooded
- **GIF animation** (`flood_animation.gif`): rising water from 30 to 80 m (step 2 m)

## Files

| File | Purpose |
|------|---------|
| `flood_inundation.py` | Main simulation script |
| `dem_data.npy` | Synthetic DEM (100×100) |
| `flood_extent_40m.png` | Flood extent at WL=40 m |
| `flood_extent_50m.png` | Flood extent at WL=50 m |
| `flood_curve.png` | Water level vs flooded % curve |
| `flood_animation.gif` | Rising water animation |
| `Experiment4_Flood_Inundation.docx` | Experiment description |
| `prompt_log.md` | AI interaction log |
