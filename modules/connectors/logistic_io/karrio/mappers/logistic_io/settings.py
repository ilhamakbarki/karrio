"""Karrio Logistic IO client settings."""

import attr
import karrio.providers.logistic_io.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Logistic IO connection settings."""

    # Add carrier specific API connection properties here
    username: str
    password: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "logistic_io"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
