"""
Sensitivity Analysis for SCS-CN Runoff Calculation

Analyzes how runoff changes with different Curve Number (CN) values.
Generates visualization plots as specified in the experiment guide.
"""

import numpy as np
import matplotlib.pyplot as plt
from scscn_runoff import calculate_runoff


def sensitivity_analysis_cn(P: float = 50.0, cn_values: list = None) -> dict:
    """
    Analyze runoff sensitivity to CN for fixed rainfall.

    Args:
        P: Fixed rainfall depth in mm
        cn_values: List of CN values to test

    Returns:
        Dictionary with CN values and corresponding Q values
    """
    if cn_values is None:
        cn_values = [60, 70, 80, 90, 95, 100]

    Q_values = [calculate_runoff(P, cn) for cn in cn_values]

    return {"P": P, "CN": cn_values, "Q": Q_values}


def plot_cn_vs_runoff(cn_values: list, q_values: list, P: float):
    """
    Create line plot: CN vs Q.

    Args:
        cn_values: List of CN values
        q_values: List of corresponding Q values
        P: Fixed rainfall depth
    """
    plt.figure(figsize=(10, 6))
    plt.plot(cn_values, q_values, 'b-o', linewidth=2, markersize=8)
    plt.xlabel('Curve Number (CN)', fontsize=12)
    plt.ylabel('Runoff Q (mm)', fontsize=12)
    plt.title(f'SCS-CN Sensitivity Analysis\n(Rainfall P = {P} mm)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(cn_values)
    plt.tight_layout()
    plt.savefig('cn_vs_runoff.png', dpi=150)
    plt.show()
    print("Saved: cn_vs_runoff.png")


def plot_rainfall_vs_runoff(P_range: list, cn_values: list):
    """
    Create comparison plot: Rainfall vs Runoff for different CN values.

    Args:
        P_range: Range of rainfall values to plot
        cn_values: List of CN values to compare
    """
    plt.figure(figsize=(12, 7))

    colors = plt.cm.viridis(np.linspace(0, 1, len(cn_values)))

    for cn, color in zip(cn_values, colors):
        Q_values = [calculate_runoff(p, cn) for p in P_range]
        plt.plot(P_range, Q_values, '-', color=color, linewidth=2,
                 label=f'CN = {cn}')

    plt.xlabel('Rainfall P (mm)', fontsize=12)
    plt.ylabel('Runoff Q (mm)', fontsize=12)
    plt.title('Rainfall-Runoff Relationship for Different CN Values', fontsize=14)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('rainfall_vs_runoff.png', dpi=150)
    plt.show()
    print("Saved: rainfall_vs_runoff.png")


def print_sensitivity_summary(P: float = 50.0):
    """Print sensitivity analysis summary."""
    cn_values = [60, 70, 80, 90, 95, 100]
    results = sensitivity_analysis_cn(P, cn_values)

    print("\n" + "=" * 50)
    print(f"Sensitivity Analysis Summary (P = {P} mm)")
    print("=" * 50)
    print(f"{'CN':<10} {'S (mm)':<12} {'Ia (mm)':<12} {'Q (mm)':<12}")
    print("-" * 50)

    for cn in cn_values:
        S = (25400 / cn) - 254
        Ia = 0.2 * S
        Q = calculate_runoff(P, cn)
        print(f"{cn:<10} {S:<12.2f} {Ia:<12.2f} {Q:<12.2f}")

    print("-" * 50)
    print("\nKey Observations:")
    print("1. Runoff increases non-linearly with CN")
    print("2. At CN=100, all rainfall becomes runoff (Q=P)")
    print("3. For low CN (permeable surfaces), most rainfall is absorbed")
    print("=" * 50)


if __name__ == "__main__":
    P_fixed = 50.0
    cn_values = [60, 70, 80, 90, 95, 100]

    results = sensitivity_analysis_cn(P_fixed, cn_values)
    print_sensitivity_summary(P_fixed)

    P_range = np.linspace(0, 100, 101)

    plot_cn_vs_runoff(results["CN"], results["Q"], P_fixed)

    plot_rainfall_vs_runoff(P_range, cn_values)
