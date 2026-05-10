import io
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def load_dem(filepath=None, seed=42):
    if filepath:
        return np.load(filepath)
    rng = np.random.default_rng(seed)
    rows, cols = 100, 100
    x = np.linspace(0, 1, cols)
    slope = 25 + 50 * x
    terrain = rng.random((rows, cols)) * 8
    dem = slope[np.newaxis, :] + terrain
    return dem


def calculate_flood(dem, water_level):
    flooded_mask = dem < water_level
    depth = np.maximum(water_level - dem, 0)
    percentage = np.sum(flooded_mask) / dem.size * 100
    return flooded_mask, depth, percentage


def visualize_flood(dem, flooded_mask, depth, water_level, save_path=None):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    im0 = axes[0].imshow(dem, cmap='terrain', aspect='auto')
    axes[0].set_title('Original DEM')
    axes[0].set_xlabel('Column')
    axes[0].set_ylabel('Row')
    plt.colorbar(im0, ax=axes[0], label='Elevation (m)')

    dem_display = np.ma.masked_where(~flooded_mask, dem)
    im1 = axes[1].imshow(dem, cmap='gray', aspect='auto')
    im1b = axes[1].imshow(dem_display, cmap='Blues', aspect='auto', alpha=0.8)
    axes[1].set_title(f'Flood Extent at {water_level}m')
    axes[1].set_xlabel('Column')
    axes[1].set_ylabel('Row')
    plt.colorbar(im1b, ax=axes[1], label='Elevation (m)')

    im2 = axes[2].imshow(depth, cmap='Blues', aspect='auto')
    axes[2].set_title(f'Inundation Depth at {water_level}m')
    axes[2].set_xlabel('Column')
    axes[2].set_ylabel('Row')
    plt.colorbar(im2, ax=axes[2], label='Depth (m)')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f'Saved: {save_path}')
    plt.close(fig)


def simulate_rising_water(dem, levels):
    percentages = []
    for wl in levels:
        _, _, pct = calculate_flood(dem, wl)
        percentages.append(pct)
    return np.array(percentages)


def validate(dem, levels, percentages, depths):
    checks = []
    checks.append(('Flooded area increases monotonically',
                   np.all(np.diff(percentages) >= -1e-9)))

    max_depths = [np.max(d) for d in depths]
    expected_max = [max(0, wl - np.min(dem)) for wl in levels]
    checks.append(('Max depth equals (water_level - min_elevation)',
                   np.allclose(max_depths, expected_max, atol=1e-9)))

    checks.append(('Flooded percentage between 0-100%',
                   np.all((percentages >= 0) & (percentages <= 100))))

    below_min = calculate_flood(dem, np.min(dem) - 1)[2]
    checks.append(('Water below min elevation -> 0% flooded',
                   below_min == 0.0))

    above_max = calculate_flood(dem, np.max(dem) + 1)[2]
    checks.append(('Water above max elevation -> 100% flooded',
                   above_max == 100.0))

    print('\n=== Validation Results ===')
    all_pass = True
    for name, result in checks:
        status = 'PASS' if result else 'FAIL'
        if not result:
            all_pass = False
        print(f'  [{status}] {name}')
    print(f'\n  Overall: {"ALL CHECKS PASSED" if all_pass else "SOME CHECKS FAILED"}')
    return all_pass


def create_flood_gif(dem, levels, save_path, fps=5):
    frames = []
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    for i, wl in enumerate(levels):
        mask, depth, pct = calculate_flood(dem, wl)

        ax = axes[0]
        ax.clear()
        dem_display = np.ma.masked_where(~mask, dem)
        ax.imshow(dem, cmap='gray', aspect='auto')
        ax.imshow(dem_display, cmap='Blues', aspect='auto', alpha=0.8)
        ax.set_title(f'Flood Extent at {wl:.0f}m ({pct:.1f}%)')
        ax.set_xlabel('Column')
        ax.set_ylabel('Row')

        ax = axes[1]
        ax.clear()
        ax.imshow(depth, cmap='Blues', aspect='auto', vmin=0, vmax=np.max(dem) - np.min(dem))
        ax.set_title('Inundation Depth')
        ax.set_xlabel('Column')
        ax.set_ylabel('Row')

        plt.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        frames.append(Image.open(buf))

    plt.close(fig)

    frames[0].save(
        save_path,
        save_all=True,
        append_images=frames[1:],
        duration=1000 // fps,
        loop=0,
    )
    print(f'Saved: {save_path}')


if __name__ == '__main__':
    print('=== Flood Inundation Analysis ===\n')

    dem = load_dem()
    np.save('dem_data.npy', dem)
    print(f'DEM shape: {dem.shape}, range: {dem.min():.2f}–{dem.max():.2f} m')

    levels_compare = [40, 50]
    depths_list = []
    for wl in levels_compare:
        mask, depth, pct = calculate_flood(dem, wl)
        depths_list.append(depth)
        print(f'Water level {wl}m: {pct:.2f}% flooded')
        visualize_flood(dem, mask, depth, wl,
                        save_path=f'flood_extent_{wl}m.png')

    levels_range = np.arange(40, 51)
    percentages = simulate_rising_water(dem, levels_range)
    depths_range = [calculate_flood(dem, wl)[1] for wl in levels_range]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(levels_range, percentages, 'b-o', linewidth=2, markersize=6)
    ax.set_xlabel('Water Level (m)')
    ax.set_ylabel('Flooded Area (%)')
    ax.set_title('Water Level vs. Flooded Percentage')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('flood_curve.png', dpi=150, bbox_inches='tight')
    print('\nSaved: flood_curve.png')
    plt.close(fig)

    validate(dem, levels_range, percentages, depths_range)

    print('\nGenerating flood animation GIF...')
    create_flood_gif(dem, np.arange(30, 81, 2), 'flood_animation.gif')
