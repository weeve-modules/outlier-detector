# Cleaner

|                |                                                                                   |
| -------------- | --------------------------------------------------------------------------------- |
| Name           | Cleaner                                                                           |
| Version        | v0.0.2                                                                            |
| Dockerhub Link | [weevenetwork/weeve-sweeper](https://hub.docker.com/r/weevenetwork/weeve-sweeper)                                                        |
| authors        | Jakub Grzelak                                                                     |

- [Cleaner](#cleaner)
  - [Description](#description)
  - [Features](#features)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output](#output)
  - [Docker Compose Example](#docker-compose-example)

## Description

Cleaner is a processing module responsible for data sanitization and anomaly detection of data passing through weeve data services.
Cleaner checks if received data are within constraints associated with some maximum and minimum acceptance value or change rate.
This module is containerized using Docker.

## Features

- Detects anomaly by comparing to a rate of change in data values
- Uses value thresholds to keep, flatten or remove data
- Flask ReST client
- Request - sends HTTP Request to the next module

## Environment Variables

### Module Specific

The following module configurations can be provided in a data service designer section on weeve platform:

| Name                              | Environment Variables           | type   | Description                                              |
| --------------------------------- | ------------------------------- | ------ | -------------------------------------------------------- |
| Upper Threshold                   | UPPER_THRESHOLD                 | float  | Value above which data would be considered as anomaly    |
| Lower Threshold                   | LOWER_THRESHOLD                 | float  | Value below which data would be considered as anomaly    |
| Anomaly Positive Rate of Change   | ANOMALY_POSITIVE_RATE_OF_CHANGE | float  | Anomaly positive rate of change per second               |
| Anomaly Negative Rate of Change   | ANOMALY_NEGATIVE_RATE_OF_CHANGE | float  | Anomaly negative rate of change per second               |
| Out of Bound Data                 | OUT-OF-BOUND_DATA               | string | What to do with out of bound data: keep, remove, smooth  |
| Input Label                       | INPUT_LABEL                     | string | The input label on which anomaly is detected             |
| Input Unit                        | INPUT_UNIT                      | string | The input unit on which anomaly is detected              |
| Output Label                      | OUTPUT_LABEL                    | string | The output label as which data is dispatched             |
| Output Unit                       | OUTPUT_UNIT                     | string | The output unit in which data is dispatched              |

Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

### Set by the weeve Agent on the edge-node

| Environment Variables | type   | Description                                    |
| --------------------- | ------ | ---------------------------------------------- |
| MODULE_NAME           | string | Name of the module                             |
| MODULE_TYPE           | string | Type of the module (INGRESS, PROCESS, EGRESS)  |
| EGRESS_SCHEME         | string | URL Scheme                                     |
| EGRESS_HOST           | string | URL target host                                |
| EGRESS_PORT           | string | URL target port                                |
| EGRESS_PATH           | string | URL target path                                |
| EGRESS_URL            | string | HTTP ReST endpoint for the next module         |
| INGRESS_HOST          | string | Host to which data will be received            |
| INGRESS_PORT          | string | Port to which data will be received            |
| INGRESS_PATH          | string | Path to which data will be received            |

## Dependencies

```txt
Flask==1.1.1
requests
python-decouple==3.4
```

## Input

Input to this module is JSON body single object:

Example:

```node
{
  temperature: 15,
  input_unit: Celsius
}
```

## Output

Output of this module is JSON body array of objects.

Output of this module is JSON body:

```node
{
    "<OUTPUT_LABEL>": <Processed data>,
    "unit": <OUTPUT_UNIT>,
}
```
 
* Here `OUTPUT_LABEL` and `OUTPUT_UNIT` are specified at the module creation and `Processed data` is data processed by Module Main function.

Example:

```node
{
  temperature: 54,
  unit: Celsius,
}
```

## Docker Compose Example

```yml
version: "3"
services:
  sweeper:
    image: weevenetwork/weeve-sweeper
    environment:
      MODULE_NAME: sweeper
      EGRESS_API_HOST: https://hookb.in/pzaBWG9rKoSXNNqwBo3o
      EGRESS_API_METHOD: "POST"
      HANDLER_HOST: "0.0.0.0"
      HANDLER_PORT: "5000"
      UPPER_THRESHOLD: 100
      LOWER_THRESHOLD: -10
      ANOMALY_POSITIVE_RATE_OF_CHANGE: 20
      ANOMALY_NEGATIVE_RATE_OF_CHANGE: -20
      OUT-OF-BOUND_DATA: "remove"
      INPUT_LABEL: "temperature"
      INPUT_UNIT: "Celsius"
      OUTPUT_LABEL: "temperature"
      OUTPUT_UNIT: "Celsius"
    ports:
      - 5000:80
```
