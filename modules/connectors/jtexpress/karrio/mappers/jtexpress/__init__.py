from karrio.core.metadata import Metadata

from karrio.mappers.jtexpress.mapper import Mapper
from karrio.mappers.jtexpress.proxy import Proxy
from karrio.mappers.jtexpress.settings import Settings
import karrio.providers.jtexpress.units as units
import karrio.providers.jtexpress.utils as utils


METADATA = Metadata(
    id="jtexpress",
    label="J&T Express",
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
