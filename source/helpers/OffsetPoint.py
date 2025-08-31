from typing import Any, Dict, Tuple
from source.helpers.Params import read_params


def offset_point(
    pos: Tuple[int, int], offset: Tuple[int, int], reverse=False
) -> Tuple[int, int]:
    """
    Offsets the `pos` tuple by `offset` tuple.

    Both `pos` and `offset` represent coordinates on 2d plane.
    1st index represents X value.
    2nd index represents Y value.

    If `reverse` is False (default), then `offset` is added to `pos`.
    Otherwise offset is substracted from pos.
    """
    off_x = offset[0]
    off_y = offset[1]
    if reverse:
        return pos[0] - off_x, pos[1] - off_y
    return pos[0] + off_x, pos[1] + off_y


def offset_point_provided_config(
    pos: Tuple[int, int], config: Dict[str, Any], reverse=False
) -> Tuple[int, int]:
    """
    Offsets the `pos` tuple by offset_x and offset_y from "MovementController" key from parameters.

    `pos` represents coordinates on 2d plane.
    1st index represents X value.
    2nd index represents Y value.

    If `reverse` is False (default), then offsets are added to `pos`.
    Otherwise offsets is substracted from `pos`.
    """
    off_x = config.get("MovementController", {}).get("offset_x", 0)
    off_y = config.get("MovementController", {}).get("offset_y", 0)
    return offset_point(pos=pos, offset=(off_x, off_y), reverse=reverse)


def offset_point_read_config(pos: Tuple[int, int], reverse=False) -> Tuple[int, int]:
    """
    Offsets the `pos` tuple by offset_x and offset_y from "MovementController" key from parameters.

    `pos` represents coordinates on 2d plane.
    1st index represents X value.
    2nd index represents Y value.

    If `reverse` is False (default), then offsets are added to `pos`.
    Otherwise offsets is substracted from `pos`.
    """
    config = read_params()
    off_x = config.get("MovementController", {}).get("offset_x", 0)
    off_y = config.get("MovementController", {}).get("offset_y", 0)
    return offset_point(pos=pos, offset=(off_x, off_y), reverse=reverse)
