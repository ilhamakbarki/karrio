"""Karrio Aymakan client settings."""

import attr
import karrio.providers.aymakan.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Aymakan connection settings."""

    # Add carrier specific API connection properties here
    api_key: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "aymakan"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
