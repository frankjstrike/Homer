# update_tagstyles.py

This script is designed to check the status of services defined in the homer configuration file, and update their 'tagstyle' accordingly. This is useful for monitoring service uptime and ensuring that all services are running as expected.

## How to Run

To run this script, use the following command:

```bash
python3 script.py --config /path/to/your/config.yml
```

## Parameters

-c or --config: This is a required parameter. It specifies the path to the YAML configuration file that contains definitions of the services that should be monitored by the script.


## Functionality

The script retrieves all services from the provided configuration file. It then checks the status of each service by sending a GET request to the service's URL.
If the status code of the response is 200 or 403, it's considered that the service is 'up', and the tagstyle of the service in the configuration file is updated to 'is-success'.
If the status code of the response is not 200 or 403, the service is considered 'down', and the tagstyle of the service in the configuration file is updated to 'is-danger'.
The script also creates a backup of the configuration file before updating it. If there are more than 20 backup files in the backup directory, it deletes the oldest one.

## Dependencies
This script requires the following Python libraries:

* logging
* time
* argparse
* sys
* requests
* yaml
* glob
* os

You can install these libraries using pip:

```bash
pip install pyyaml requests
```

Note: logging, time, argparse, sys, glob, and os are part of the Python Standard Library, so you don't need to install them.
