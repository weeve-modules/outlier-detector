"""
This file implements module's main logic.
Data processing should happen here.

Edit this file to implement your module.
"""

from logging import getLogger
from .params import PARAMS

import time

log = getLogger("module")

prev_data = 0
prev_time = time.time()
first_data = True


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
        global prev_time

        # receive data timestamp
        data_time = time.time()

        if type(received_data) == dict:
            processed_data = analytics(received_data, data_time)
        elif type(received_data) == list:
            processed_data = []
            for item in received_data:
                processed_data.append(analytics(item, data_time))

        return processed_data, None

    except Exception as e:
        return None, f"Exception in the module business logic: {e}"


def analytics(data, data_time):
    global prev_data
    global prev_time
    global first_data

    if type(prev_data) == dict:
        rate_change = (
            data[PARAMS["INPUT_LABEL"]] - prev_data[PARAMS["INPUT_LABEL"]]
        ) / (data_time - prev_time + 10e-8)
    else:
        rate_change = (data[PARAMS["INPUT_LABEL"]] - prev_data) / (
            data_time - prev_time + 10e-8
        )

    # if the first data received
    if (
        first_data
        and PARAMS["LOWER_THRESHOLD"]
        <= data[PARAMS["INPUT_LABEL"]]
        <= PARAMS["UPPER_THRESHOLD"]
    ):
        first_data = False
        prev_data = data
        prev_time = data_time
        return data
    elif (
        PARAMS["LOWER_THRESHOLD"]
        <= data[PARAMS["INPUT_LABEL"]]
        <= PARAMS["UPPER_THRESHOLD"]
        and PARAMS["RATE_OF_CHANGE_LOWER_THRESHOLD"]
        <= rate_change
        <= PARAMS["RATE_OF_CHANGE_UPPER_THRESHOLD"]
    ):
        # not anomalous
        prev_data = data
        prev_time = data_time
        return data
    else:
        # anomalous
        if PARAMS["OUTLIER_POLICY"] == "keep":
            prev_data = data
            prev_time = data_time
            return data
        elif PARAMS["OUTLIER_POLICY"] == "smooth":
            prev_time = data_time
            return prev_data
        elif PARAMS["OUTLIER_POLICY"] == "remove":
            return None
