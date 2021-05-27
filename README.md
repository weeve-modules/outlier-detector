# Sweeper

| | |
| --- | ---|
| version | `v0.0.1` |
| authors | `Jakub Grzelak`, `Sanyam Arya` |
| docker image | `weevenetwork/weeve-sweeper` |
| tech tags | `Python`, `Flask`, `Docker` |

_Sweeper is a processing module responsible for data sanitization and anomaly detection of data passing through weeve data services._
_Sweeper checks if received data are within constraints associated with some maximum and minimum acceptance value or change rate._
_This module is containerized using Docker._

The following module features must be provided by a developer in a data service designer section on weeve platform:
* **Upper Threshold** - the value above which data would be considered as anomaly,
  * type: integer
* **Lower Threshold** - the value below which data would be considered as anomaly,
  * type: integer
* **Anomaly Positive Rate of Change** - anomaly positive rate of change per second,
  * type: float
* **Anomaly Negative Rate of Change** - anomaly negative rate of change per second,
  * type: float
* **Out of Bound Data** - what to do with out of bound data,
  * keep - keeps data
  * remove - removes data
  * smooth - sets data to the most recent value that satisfied the constraints
* **Input Label** - the input label on which anomaly is detected,
  * type: string
* **Input Unit** - the input unit on which anomaly is detected,
  * type: string
* **Output Label** - the output label as which data is dispatched,
  * type: string
* **Output Unit** - the output unit in which data is dispatched,
  * type: string

Other features required for establishing the inter-container communication between modules in a data service are set by weeve server.
These include: egress api host, egress api method, handler host and port.

### Requirements
Sweeper requires the following Python packages that will be installed on a container built:
* Flask v1.1.1
* requests
* python-decouple v3.4

### Output
Output of this module is JSON body:
{
    "_OUTPUT_LABEL_": _PROCESSED_DATA_,
    "input_unit": _OUTPUT_UNIT_,
}

where _OUTPUT_LABEL_ and _OUTPUT_UNIT_ are specified at the module creation and _PROCESSED_DATA_ is data processed by Sweeper
