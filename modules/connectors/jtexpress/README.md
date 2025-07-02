
# karrio.jtexpress

This package is a J&T Express extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.jtexpress
```

## Usage

```python
import karrio
from karrio.mappers.jtexpress.settings import Settings


# Initialize a carrier gateway
jtexpress = karrio.gateway["jtexpress"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
