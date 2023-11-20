from example_lib.validators import validate_gt_0, validate_list_not_empty


def test_validate_gte_0():
    assert validate_gt_0(3)
    assert validate_gt_0(4)


def test_validate_list_not_empty():
    assert validate_list_not_empty([1, 2, 3])
    assert not validate_list_not_empty([])
