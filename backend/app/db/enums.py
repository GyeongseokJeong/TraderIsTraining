from enum import Enum
from typing import TypeVar

EnumType = TypeVar("EnumType", bound=Enum)


def enum_values(enum_class: type[EnumType]) -> list[str]:
    return [member.value for member in enum_class]
