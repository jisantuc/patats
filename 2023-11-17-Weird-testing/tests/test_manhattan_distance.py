from example_lib.manhattan_distance import manhattan_distance
from hypothesis import given
from hypothesis.strategies import booleans, composite, integers


@composite
def square_points(draw, coord_strat=integers(), flip_y=booleans()):
    coord_int = draw(coord_strat)
    flip = draw(flip_y)
    return (coord_int, coord_int if not flip else coord_int * -1)


@given(square_points())
def test_manhattan(square_point):
    assert manhattan_distance(square_point, (0, 0)) == abs(2 * square_point[0])
