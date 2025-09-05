from typing import Any, Type, TypeVar

T = TypeVar("T")


def try_parse(value: Any, type: Type[T], default: T) -> T:
    try:
        out = T(value)
    except Exception:
        print(f"Couldnt parse value into {type(T)}. Defaulting to {default}.")
        out = default
    return out
