from typing import Any, Dict
import toml
import source.config as cfg


def read_params() -> Dict[str, Any]:
    with open(cfg.PARAMS_PATH, "r") as file:
        return toml.load(file)
