import json

import pytest

from example_lib.important_data_model import ImportantData, to_json


@pytest.mark.golden_test("golden_important_data.yml")
def test_important_data_serialization(golden):

    obj = ImportantData.parse_obj(json.loads(golden["input"]))
    assert to_json(obj) == golden.out["output"]
