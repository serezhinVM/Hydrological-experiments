"""
Comprehensive Tests for SCS-CN Runoff Calculation

Tests cover:
    1. P = 0: Expected Q = 0
    2. P < Ia: Expected Q = 0
    3. P = Ia: Expected Q = 0
    4. Normal case: P = 50mm, CN = 80 (expected Q ≈ 13.8mm)
    5. Maximum CN: CN = 100
    6. Verify Q ≤ P for all cases
"""

import pytest
from scscn_runoff import calculate_runoff, calculate_S, calculate_Ia


class TestBoundaryConditions:
    """Test boundary conditions for SCS-CN method."""

    def test_p_zero_returns_zero(self):
        """Test that P = 0 returns Q = 0."""
        assert calculate_runoff(0, 80) == 0.0

    def test_p_less_than_ia_returns_zero(self):
        """Test that P < Ia returns Q = 0."""
        Q = calculate_runoff(5, 80)
        assert Q == 0.0

    def test_p_equals_ia_returns_zero(self):
        """Test that P = Ia returns Q = 0."""
        CN = 80
        S = calculate_S(CN)
        Ia = 0.2 * S
        Q = calculate_runoff(Ia, CN)
        assert Q == 0.0

    def test_normal_case_p50_cn80(self):
        """Test normal case: P = 50mm, CN = 80 should give Q ≈ 13.8mm."""
        Q = calculate_runoff(50, 80)
        assert 13.5 <= Q <= 14.0

    def test_cn_100_no_abstraction(self):
        """Test CN = 100 (impervious): Q ≈ P."""
        Q = calculate_runoff(50, 100)
        assert Q == 50.0

    def test_q_never_exceeds_p(self):
        """Verify Q ≤ P for all valid inputs."""
        test_cases = [
            (10, 60), (10, 80), (10, 100),
            (25, 60), (25, 80), (25, 100),
            (50, 60), (50, 80), (50, 100),
            (100, 60), (100, 80), (100, 100),
        ]
        for P, CN in test_cases:
            Q = calculate_runoff(P, CN)
            assert Q <= P, f"Q ({Q}) > P ({P}) for CN={CN}"

    def test_higher_cn_produces_more_runoff(self):
        """Verify higher CN produces more runoff for same P."""
        P = 50
        Q_60 = calculate_runoff(P, 60)
        Q_80 = calculate_runoff(P, 80)
        Q_95 = calculate_runoff(P, 95)
        assert Q_60 < Q_80 < Q_95

    def test_cn_boundary_conditions(self):
        """Test edge cases for CN values."""
        with pytest.raises(ValueError):
            calculate_runoff(50, 0)
        with pytest.raises(ValueError):
            calculate_runoff(50, -10)
        with pytest.raises(ValueError):
            calculate_runoff(50, 100.1)

    def test_negative_rainfall_raises_error(self):
        """Test that negative P raises ValueError."""
        with pytest.raises(ValueError):
            calculate_runoff(-10, 80)


class TestHelperFunctions:
    """Test helper functions."""

    def test_calculate_s(self):
        """Test S calculation for CN = 80."""
        S = calculate_S(80)
        assert 63.0 <= S <= 64.0

    def test_calculate_ia(self):
        """Test Ia calculation for CN = 80."""
        Ia = calculate_Ia(80)
        S = calculate_S(80)
        assert abs(Ia - 0.2 * S) < 0.001


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
