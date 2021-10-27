"""
All constants specific to the application
"""
from app.utils.env import env
from app.utils.floatenv import floatenv

APPLICATION = {
    "UPPER_THRESHOLD": floatenv("UPPER_THRESHOLD", 20.0),
    "LOWER_THRESHOLD": floatenv("LOWER_THRESHOLD", -10.0),
    "ANOMALY_POSITIVE_RATE_OF_CHANGE": floatenv("ANOMALY_POSITIVE_RATE_OF_CHANGE", 20.0),
    "ANOMALY_NEGATIVE_RATE_OF_CHANGE": floatenv("ANOMALY_NEGATIVE_RATE_OF_CHANGE", -10.0),
    "OUT-OF-BOUND_DATA": env("OUT-OF-BOUND_DATA", "keep"),
    "INPUT_LABEL": env("INPUT_LABEL", "temperature"),
    "INPUT_UNIT": env("INPUT_UNIT", "Celsius"),
    "OUTPUT_LABEL": env("OUTPUT_LABEL", "temperature"),
    "OUTPUT_UNIT": env("OUTPUT_UNIT", "Celsius")
}
