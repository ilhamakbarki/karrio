from karrio.core.metadata import Metadata

from karrio.mappers.aymakan.mapper import Mapper
from karrio.mappers.aymakan.proxy import Proxy
from karrio.mappers.aymakan.settings import Settings
import karrio.providers.aymakan.units as units
import karrio.providers.aymakan.utils as utils


METADATA = Metadata(
    id="aymakan",
    label="Aymakan",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    # options=units.ShippingOption,
    # services=units.ShippingService,
    # connection_configs=utils.ConnectionConfig,
)
