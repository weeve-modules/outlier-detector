from flask import Flask, request
import requests
import logging
import time
from decouple import config

log = logging.getLogger(__name__)
app = Flask(__name__)
__EGRESS_API_HOST__ = config('EGRESS_API_HOST')
__EGRESS_API_METHOD__ = config('EGRESS_API_METHOD')
__HANDLER_HOST__ = config('HANDLER_HOST')
__HANDLER_PORT__ = config('HANDLER_PORT')

# Set module settings
__UPPER_THRESHOLD__ = float(config('UPPER_THRESHOLD'))
__LOWER_THRESHOLD__ = float(config('LOWER_THRESHOLD'))
__ANOMALY_POSITIVE_RATE_OF_CHANGE__ = float(
    config('ANOMALY_POSITIVE_RATE_OF_CHANGE'))
__ANOMALY_NEGATIVE_RATE_OF_CHANGE__ = float(
    config('ANOMALY_NEGATIVE_RATE_OF_CHANGE'))
__OUT_OF_BOUND_DATA__ = config('OUT-OF-BOUND_DATA')
__INPUT_LABEL__ = config('INPUT_LABEL')
__INPUT_UNIT__ = config('INPUT_UNIT')
__OUTPUT_LABEL__ = config('OUTPUT_LABEL')
__OUTPUT_UNIT__ = config('OUTPUT_UNIT')

# Previously received data value (for smoothing)
prev_data = 0
prev_time = time.time()
first_data = True


@app.route('/handle', methods=['POST'])
def handle():
    '''
    Receive ReST API POST request with data.
    '''
    global prev_time

    # receive data
    received_data = request.get_json(force=True)
    data_time = time.time()

    # parse target data from the structure
    try:
        parsed_data = received_data[__INPUT_LABEL__]
        #print("RECEIVED DATA: ", received_data)
    except:
        log.exception(f"Wrong data structure.")

    try:
        analytics(parsed_data, data_time)
    except:
        log.exception(f"Data analysis failed.")

    # 204 - return success, no content status
    return '', 204


def analytics(data, data_time):
    global prev_data
    global prev_time
    global first_data

    rate_change = (data - prev_data) / (data_time - prev_time)

    # if the first data received
    if first_data and __LOWER_THRESHOLD__ <= data <= __UPPER_THRESHOLD__:
        first_data = False
        prev_data = data
        prev_time = data_time
        output(data)
    elif __LOWER_THRESHOLD__ <= data <= __UPPER_THRESHOLD__ and __ANOMALY_NEGATIVE_RATE_OF_CHANGE__ <= rate_change <= __ANOMALY_POSITIVE_RATE_OF_CHANGE__:
        # not anomalous
        prev_data = data
        prev_time = data_time
        output(data)
    else:
        # anomalous
        if __OUT_OF_BOUND_DATA__ == 'keep':
            prev_data = data
            prev_time = data_time
            output(data)
        elif __OUT_OF_BOUND_DATA__ == 'smooth':
            prev_time = data_time
            output(prev_data)

        # elif __OUT_OF_BOUND_DATA__ == 'remove': DO NOTHING


def output(data):
    # prepare output HTTP ReST API request, build JSON body
    return_body = {
        __OUTPUT_LABEL__: data,
        "input_unit": __OUTPUT_UNIT__
    }

    # post request
    if __EGRESS_API_METHOD__ == "POST":
        resp = requests.post(
            url=f"{__EGRESS_API_HOST__}", data=return_body)
        #print(f"RETURN_BODY: {return_body}")
        #print(f"THE RESPONSE:{resp} {resp.text}")
    else:
        log.exception(f"The HTTP Method not supportive.")


if __name__ == "__main__":
    app.run(host=__HANDLER_HOST__, port=__HANDLER_PORT__)
