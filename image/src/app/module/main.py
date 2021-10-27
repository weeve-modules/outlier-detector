"""
All logic related to the module's main application
Mostly only this file requires changes
"""

from app.config import APPLICATION
import time

prev_data = 0
prev_time = time.time()
first_data = True

def module_main(data):
    """implement module logic here

    Args:
        parsed_data ([JSON Object]): [Data received by the module and validated by data_validation function]

    Returns:
        [string, string]: [data, error]
    """
    try:
        global prev_time

        # receive data timestamp
        data_time = time.time()
        
        if type(data) == dict:
            parsed_data = data[APPLICATION['INPUT_LABEL']]
            processed_data = analytics(parsed_data, data_time)

        return processed_data, None
    except Exception:
        return None, "Unable to perform the module logic"

def analytics(data, data_time):
    global prev_data
    global prev_time
    global first_data

    rate_change = (data - prev_data) / (data_time - prev_time)

    # if the first data received
    if first_data and APPLICATION['LOWER_THRESHOLD'] <= data <= APPLICATION['UPPER_THRESHOLD']:
        first_data = False
        prev_data = data
        prev_time = data_time
        return data
    elif APPLICATION['LOWER_THRESHOLD'] <= data <= APPLICATION['UPPER_THRESHOLD'] and APPLICATION['ANOMALY_NEGATIVE_RATE_OF_CHANGE'] <= rate_change <= APPLICATION['ANOMALY_POSITIVE_RATE_OF_CHANGE']:
        # not anomalous
        prev_data = data
        prev_time = data_time
        return data
    else:
        # anomalous
        if APPLICATION['OUT-OF-BOUND_DATA'] == 'keep':
            prev_data = data
            prev_time = data_time
            return data
        elif APPLICATION['OUT-OF-BOUND_DATA'] == 'smooth':
            prev_time = data_time
            return prev_data
        elif APPLICATION['OUT-OF-BOUND_DATA'] == 'remove':
            return None

