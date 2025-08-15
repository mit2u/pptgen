from enum import StrEnum

from pydantic import BaseModel

PPTX_MAPPING = {
    '1' : 0 , '2' : 1 , '3' : 5 , '4' :6
}


class SlideEnum(StrEnum):
    title = "1"
    bullet = "2"
    column = "3"
    image = "4"


class Slide(BaseModel):
    title: str
    bullet_points: list[str]
    column_presentation: bool
    col1_bullet_points: list[str]
    col2_bullet_points: list[str]
    content: str
    image: str
    image_placeholder: str
    slide_type: SlideEnum
