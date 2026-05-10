# Prompt Log - Flood Inundation Analysis

## Experiment 4: Flood Inundation Analysis (DEM-based)

### AI Interaction Documentation

---

**Prompt 1: Generate DEM data**
- **Task:** Create a 100x100 grid with elevation values between 30-80m
- **Model Response:** Used `numpy.random.default_rng(seed=42)` to generate reproducible synthetic terrain, scaled to 30-80m range (`30 + 50 * random`)

---

**Prompt 2: Implement flood inundation calculation**
- **Task:** Write flood simulation logic for a given water level
- **Model Response:** Implemented `calculate_flood()` which returns:
  - `flooded_mask`: boolean array where `dem < water_level`
  - `depth_array`: inundation depth = `max(0, water_level - dem)`
  - `percentage`: `(flooded_cells / total_cells) * 100`

---

**Prompt 3: Create flood extent visualizations**
- **Task:** Generate 3-panel visualization (DEM, flood extent overlay, inundation depth)
- **Model Response:** Used `matplotlib` with `imshow()`: terrain colormap for DEM, gray + Blues overlay for flood extent, Blues for depth heatmap. Saved to `flood_extent_40m.png` and `flood_extent_50m.png`.

---

**Prompt 4: Dynamic rising water simulation**
- **Task:** Loop water levels 40-50m, calculate flooded %, plot curve
- **Model Response:** Implemented `simulate_rising_water()` looping over levels; plotted Water Level vs. Flooded Percentage as blue line with markers. Saved to `flood_curve.png`.

---

**Prompt 5: Physical validation**
- **Task:** Verify physical correctness of flood simulation
- **Model Response:** Implemented `validate()` with 5 checks:
  1. Flooded area increases monotonically with water level
  2. Max depth equals `(water_level - min_elevation)`
  3. Flooded percentage is 0-100%
  4. Water below min elevation -> 0% flooded
  5. Water above max elevation -> 100% flooded

**All 5 checks passed.**

---

**Prompt 6: Save DEM data**
- **Task:** Persist generated DEM to file
- **Model Response:** Used `np.save('dem_data.npy', dem)` to save the 100x100 array.

---

### Files Generated
| File | Description |
|------|-------------|
| `flood_inundation.py` | Main implementation script |
| `dem_data.npy` | Synthetic DEM data (100x100, 30-80m) |
| `flood_extent_40m.png` | Flood visualization at 40m water level |
| `flood_extent_50m.png` | Flood visualization at 50m water level |
| `flood_curve.png` | Water level vs. flooded percentage plot |
| `prompt_log.md` | This documentation |
