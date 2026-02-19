from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel
import csv

class Gender(StrEnum):
    MALE = "M"
    FEMALE = "Ж"

    @staticmethod
    def from_int(gender: int) -> Gender:
        if gender==1:
            return Gender.MALE
        if gender==2:
            return Gender.FEMALE

        raise ValueError(f"Invalid gender: {gender}")


class People(BaseModel):
    people_name: str
    people_family: str
    people_patronymic: str
    people_gender: Gender
    people_came_from: str
    people_birthday: int
    people_comment: str


People.model_rebuild()