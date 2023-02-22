"""
This file implements module's main logic.
Data processing should happen here.

Edit this file to implement your module.
"""

from logging import getLogger
from .params import PARAMS

import time

log = getLogger("module")

prev_data = None
prev_time = None


def module_main(received_data: any) -> [any, str]:
    """
    Process received data by implementing module's main logic.
    Function description should not be modified.

    Args:
        received_data (any): Data received by module and validated.

    Returns:
        any: Processed data that are ready to be sent to the next module or None if error occurs.
        str: Error message if error occurred, otherwise None.

    """

    log.debug("Processing ...")

    try:
        global prev_data
        global prev_time

        data = received_data[PARAMS["INPUT_DATA_LABEL"]]
        timestamp = int(received_data[PARAMS["INPUT_TIME_LABEL"]])

        if is_outlier(data, timestamp):
            if PARAMS["OUTLIER_POLICY"] == "keep":
                prev_data = data
                prev_time = timestamp
                return received_data, None
            elif PARAMS["OUTLIER_POLICY"] == "smooth":
                prev_time = timestamp
                received_data[PARAMS["INPUT_DATA_LABEL"]] = prev_data
                return received_data, None
            elif PARAMS["OUTLIER_POLICY"] == "remove":
                return None, None
        else:
            prev_data = data
            prev_time = timestamp
            return received_data, None

    except Exception as e:
        return None, f"Exception in the module business logic: {e}"


def is_outlier(data, timestamp):
    if (
        prev_data is None or prev_time is None
    ):  # first data or all previous data were outliers
        if PARAMS["LOWER_THRESHOLD"] is not None:
            if data < PARAMS["LOWER_THRESHOLD"]:
                return True
        if PARAMS["UPPER_THRESHOLD"] is not None:
            if data > PARAMS["UPPER_THRESHOLD"]:
                return True

        return False

    rate_change = (data - prev_data) / (timestamp - prev_time + 10e-8)

    if PARAMS["LOWER_THRESHOLD"] is not None:
        if data < PARAMS["LOWER_THRESHOLD"]:
            return True
    if PARAMS["UPPER_THRESHOLD"] is not None:
        if data > PARAMS["UPPER_THRESHOLD"]:
            return True
    if PARAMS["RATE_OF_CHANGE_LOWER_THRESHOLD"] is not None:
        if rate_change < PARAMS["RATE_OF_CHANGE_LOWER_THRESHOLD"]:
            return True
    if PARAMS["RATE_OF_CHANGE_UPPER_THRESHOLD"] is not None:
        if rate_change > PARAMS["RATE_OF_CHANGE_UPPER_THRESHOLD"]:
            return True
