from enum import Enum


class MovementActions(Enum):
    WalkUp = "WALK_UP"
    WalkRight = "WALK_RIGHT"
    WalkLeft = "WALK_LEFT"
    WalkDown = "WALK_DOWN"
    RotateLeft = "ROTATE_LEFT"
    RotateRight = "ROTATE_RIGHT"
    ClickLeft = "CLICK_LEFT"
    ClickRight = "CLICK_RIGHT"
    ClickMiddle = "CLICK_MIDDLE"
    ButtonPress = "BUTTON_PRESS"
