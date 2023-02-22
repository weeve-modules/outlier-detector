"""
All parameters specific to the application
"""

from os import getenv

PARAMS = {
    "UPPER_THRESHOLD": None if getenv("UPPER_THRESHOLD") is None else float(getenv("UPPER_THRESHOLD")),
    "LOWER_THRESHOLD": None if getenv("LOWER_THRESHOLD") is None else float(getenv("LOWER_THRESHOLD")),
    "RATE_OF_CHANGE_UPPER_THRESHOLD": None if getenv("RATE_OF_CHANGE_UPPER_THRESHOLD") is None else float(getenv("RATE_OF_CHANGE_UPPER_THRESHOLD")),
    "RATE_OF_CHANGE_LOWER_THRESHOLD": None if getenv("RATE_OF_CHANGE_LOWER_THRESHOLD") is None else float(getenv("RATE_OF_CHANGE_LOWER_THRESHOLD")),
    "OUTLIER_POLICY": getenv("OUTLIER_POLICY", "remove"),
    "INPUT_DATA_LABEL": getenv("INPUT_DATA_LABEL", "temperature"),
    "INPUT_TIME_LABEL": getenv("INPUT_TIME_LABEL", "timestamp"),
}
