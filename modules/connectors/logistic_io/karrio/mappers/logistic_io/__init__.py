from karrio.core.metadata import Metadata

from karrio.mappers.logistic_io.mapper import Mapper
from karrio.mappers.logistic_io.proxy import Proxy
from karrio.mappers.logistic_io.settings import Settings
import karrio.providers.logistic_io.units as units
import karrio.providers.logistic_io.utils as utils


METADATA = Metadata(
    id="logistic_io",
    label="Logistic IO",
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
