from pathlib import Path

RUNTIME_PATH = "."
"""Points to root of the project.
Change this if you want to be able to execute this script from different location than root dir.
"""

PARAMS_FILENAME = "params.toml"
PARAMS_PATH = str(Path(RUNTIME_PATH, PARAMS_FILENAME))

LOCATIONS_FILENAME = "default.toml"
LOCATIONS_DIR = str(Path("source", "MC_locations"))
LOCATIONS_PATH = str(Path(RUNTIME_PATH, LOCATIONS_DIR, LOCATIONS_FILENAME))
