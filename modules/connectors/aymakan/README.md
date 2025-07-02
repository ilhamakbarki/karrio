
# karrio.aymakan

This package is a Aymakan extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.aymakan
```

## Usage

```python
import karrio
from karrio.mappers.aymakan.settings import Settings


# Initialize a carrier gateway
aymakan = karrio.gateway["aymakan"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
