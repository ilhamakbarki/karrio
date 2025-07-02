
# karrio.logistic_io

This package is a Logistic IO extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.logistic_io
```

## Usage

```python
import karrio
from karrio.mappers.logistic_io.settings import Settings


# Initialize a carrier gateway
logistic_io = karrio.gateway["logistic_io"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
