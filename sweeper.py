from flask import Flask, request
import requests
import logging
import time
from decouple import config

log = logging.getLogger(__name__)
app = Flask(__name__)
__EGRESS_API_HOST__ = config('EGRESS_API_HOST')
__EGRESS_API_PORT__ = config('EGRESS_API_PORT')
__EGRESS_API_URI__ = config('EGRESS_API_URI')
__EGRESS_API_METHOD__ = config('EGRESS_API_METHOD')
__HANDLER_HOST__ = config('HANDLER_HOST')
__HANDLER_PORT__ = config('HANDLER_PORT')

# Set default settings
settings = {
    "upper_threshold": 1000,
    "lower_threshold": -10,
    "anomaly_positive_rate": 20,
    "anomaly_negative_rate": 20,
    "outliers": 'keep',  # keep, remove, smooth
    "input_label": 'temperature',
    "input_unit": 'Celsius',
    "output_label": 'differentialTemp',
    "output_unit": 'Celsius'
}

# Flag if settings are set
settingsSet = False

# Previously received data value (for smoothing)
prev_data = 0
prev_time = time.time()
first_data = True

@app.route('/handle', methods=['POST'])
def handle():
    '''
    Receive ReST API POST request. First request is Sweeper settings.
    The next requests are data.
    '''
    global settings
    global settingsSet
    global prev_time

    if not settingsSet:
        # set Sweeper settings
        settings = request.get_json(force=True)
        #print(f"Settings Request {settings}")
        settingsSet = True
        prev_time = time.time()

    else:
        # receive data
        received_data = request.get_json(force=True)
        data_time = time.time()

        # parse target data from the structure
        try:
            parsed_data = received_data[settings['input_label']]
            #print("RECEIVED DATA: ", received_data)

            analytics(parsed_data, data_time)
        except:
            log.exception(f"Wrong data structure.")


    # 204 - return success, no content status
    return '', 204


def analytics(data, data_time):
    global prev_data
    global prev_time
    global first_data

    rate_change = (data - prev_data) / (data_time - prev_time)

    # if the first data received
    if first_data and settings['lower_threshold'] <= data <= settings['upper_threshold']:
        first_data = False
        prev_data = data
        prev_time = data_time
        output(data)

    if settings['lower_threshold'] <= data <= settings['upper_threshold'] and settings['anomaly_negative_rate'] <= rate_change <= settings['anomaly_positive_rate']:
        # not anomalous
        prev_data = data
        prev_time = data_time
        output(data)
    else:
        # anomalous
        if settings['outliers'] == 'keep':
            prev_data = data
            prev_time = data_time
            output(data)
        elif settings['outliers'] == 'smooth':
            prev_time = data_time
            output(prev_data)
        
        # elif settins['outliers'] == 'remove': DO NOTHING


def output(data):
    # prepare output HTTP ReST API request, build JSON body
    return_body = {
        str(settings["output_label"]): data,
        "input_unit": settings["output_unit"]
    }

    # post request
    if __EGRESS_API_METHOD__ == "POST":
        resp = requests.post(url=f"http://{__EGRESS_API_HOST__}:{__EGRESS_API_PORT__}{__EGRESS_API_URI__}", json=return_body)
        #print(f"THE RESPONSE:{resp} {resp.text}")
    else:
        log.exception(f"The HTTP Method not supportive.")


if __name__ == "__main__":
    app.run(host=__HANDLER_HOST__, port=__HANDLER_PORT__)