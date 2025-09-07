from typing import Any, Type, TypeVar

T = TypeVar("T")


def try_parse(value: Any, type_: Type[T], default: T) -> T:
    try:
        out = type_(value)  # type:ignore
    except Exception:
        print(f"Couldnt parse value {value} into {type_}. Defaulting to {default}.")
        out = default
    return out
