"""
All parameters specific to the application
"""

from os import getenv

PARAMS = {
    "UPPER_THRESHOLD": float(getenv("UPPER_THRESHOLD", 10)),
    "LOWER_THRESHOLD": float(getenv("LOWER_THRESHOLD", -10)),
    "ANOMALY_POSITIVE_RATE_OF_CHANGE": float(getenv("ANOMALY_POSITIVE_RATE_OF_CHANGE", 20)),
    "ANOMALY_NEGATIVE_RATE_OF_CHANGE": float(getenv("ANOMALY_NEGATIVE_RATE_OF_CHANGE", -20)),
    "OUT-OF-BOUND_DATA": getenv("OUT-OF-BOUND_DATA", "remove"),
    "INPUT_LABEL": getenv("INPUT_LABEL", "temperature")
}
