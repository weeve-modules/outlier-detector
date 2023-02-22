"""
All parameters specific to the application
"""

from os import getenv

PARAMS = {
    "UPPER_THRESHOLD": float(getenv("UPPER_THRESHOLD")),
    "LOWER_THRESHOLD": float(getenv("LOWER_THRESHOLD")),
    "RATE_OF_CHANGE_UPPER_THRESHOLD": float(
        getenv("RATE_OF_CHANGE_UPPER_THRESHOLD")
    ),
    "RATE_OF_CHANGE_LOWER_THRESHOLD": float(
        getenv("RATE_OF_CHANGE_LOWER_THRESHOLD")
    ),
    "OUTLIER_POLICY": getenv("OUTLIER_POLICY", "remove"),
    "INPUT_LABEL": getenv("INPUT_LABEL", "temperature"),
}
