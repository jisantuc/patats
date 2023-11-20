from pydantic import BaseModel


class ImportantData(BaseModel):
    x: int
    y: int
    msg: str


def to_json(data: ImportantData) -> dict:
    return {"the_x_value": data.x, "the_y_value": data.y, "the_msg": data.msg}
