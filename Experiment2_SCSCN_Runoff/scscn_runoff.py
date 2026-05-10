"""
SCS-CN Runoff Calculation Module

Implements the Soil Conservation Service Curve Number (SCS-CN) method
for estimating direct runoff from rainfall.

Formulas:
    S = (25400 / CN) - 254
    Ia = 0.2 * S
    Q = (P - Ia)² / (P - Ia + S) if P > Ia, else Q = 0

Where:
    Q  = Runoff depth (mm)
    P  = Rainfall depth (mm)
    S  = Potential maximum retention (mm)
    Ia = Initial abstraction (mm)
    CN = Curve Number (0-100)
"""


def calculate_runoff(P: float, CN: float) -> float:
    """
    Calculate runoff depth using the SCS-CN method.

    Args:
        P:  Rainfall depth in mm
        CN: Curve Number (0-100)

    Returns:
        Runoff depth in mm

    Raises:
        ValueError: If CN <= 0 or CN > 100 or P < 0
    """
    if CN <= 0 or CN > 100:
        raise ValueError(f"CN must be in range (0, 100], got {CN}")
    if P < 0:
        raise ValueError(f"P must be non-negative, got {P}")

    if P == 0:
        return 0.0

    S = (25400.0 / CN) - 254.0
    Ia = 0.2 * S

    if P <= Ia:
        return 0.0

    Q = (P - Ia) ** 2 / (P - Ia + S)

    return min(Q, P)


def calculate_S(Cn: float) -> float:
    """
    Calculate potential maximum retention (S) from Curve Number.

    Args:
        Cn: Curve Number (0-100)

    Returns:
        S in mm
    """
    return (25400.0 / Cn) - 254.0


def calculate_Ia(Cn: float) -> float:
    """
    Calculate initial abstraction (Ia) from Curve Number.

    Args:
        Cn: Curve Number (0-100)

    Returns:
        Ia in mm (typically 0.2 * S)
    """
    S = calculate_S(Cn)
    return 0.2 * S
