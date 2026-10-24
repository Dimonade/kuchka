"""`is_close` on angles, across the wrap."""

from __future__ import annotations

import math

import pytest

from kuchka.units import angular


@pytest.mark.parametrize(
    ("degrees", "radians"),
    [
        (90, math.pi / 2),
        (45, math.pi / 4),
        (60, math.pi / 3),
        (30, math.pi / 6),
        (180, math.pi),
        (360, 2 * math.pi),
    ],
    ids=["90", "45", "60", "30", "180", "360"],
)
def test_float_radians_are_close_to_the_matching_degrees(
    degrees: int, radians: float
) -> None:
    assert angular.Degree(degrees).is_close(
        angular.Radian(radians), tolerance=angular.Radian(1e-15)
    )


def test_the_angle_tolerance_may_be_written_in_any_angular_unit() -> None:
    reading = angular.Radian(math.pi / 2)
    assert angular.Degree(90).is_close(reading, tolerance=angular.ArcSecond(1e-9))
    assert angular.Degree(90).is_close(reading, tolerance=angular.Turn(1e-12))


def test_angles_either_side_of_the_wrap_point_are_close() -> None:
    assert angular.Degree(359.9999).is_close(
        angular.Degree(0.0001), tolerance=angular.Degree(0.001)
    )
    assert angular.Degree(0.0001).is_close(
        angular.Degree(359.9999), tolerance=angular.Degree(0.001)
    )


def test_unnormalised_angles_are_compared_by_position() -> None:
    assert angular.Degree(370).is_close(angular.Degree(10), tolerance=angular.Degree(0))


def test_an_angle_tolerance_of_half_a_turn_accepts_everything() -> None:
    assert angular.Degree(0).is_close(
        angular.Degree(180), tolerance=angular.Degree(180)
    )
    assert angular.Degree(0).is_close(angular.Degree(123), tolerance=angular.Turn(1))


def test_angle_closeness_is_symmetric() -> None:
    a, b, tolerance = angular.Degree(10), angular.Degree(350), angular.Degree(20)
    assert a.is_close(b, tolerance=tolerance) is b.is_close(a, tolerance=tolerance)
