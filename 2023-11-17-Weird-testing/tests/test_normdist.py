from hypothesis import given
from hypothesis.strategies import floats
from pytest import approx

from example_lib.normdist import NormalDistribution, sample_mean


@given(
    floats(0, 1000, allow_nan=False, allow_infinity=False),
    floats(1, 1000, allow_nan=False, allow_infinity=False),
)
def test_distribution_center(expected_center: float, expected_variance: float):
    dist = NormalDistribution(expected_center, expected_variance)
    mean = sample_mean(dist, 10000)
    assert abs(mean - expected_center) / expected_variance == approx(0, abs=1e-2)


@given(
    floats(0, 1000, allow_nan=False, allow_infinity=False),
    floats(1, 1000, allow_nan=False, allow_infinity=False),
    floats(-10000, 10000, allow_nan=False, allow_infinity=False),
)
def test_distribution_recenter(
    expected_center: float, expected_variance: float, bump: float
):
    initial_dist = NormalDistribution(expected_center, expected_variance)
    recentered = initial_dist.recenter(bump)

    recentered_sample_mean = sample_mean(recentered, 2000)

    assert recentered_sample_mean == approx(
        expected_center + bump, abs=expected_variance / 50
    )
