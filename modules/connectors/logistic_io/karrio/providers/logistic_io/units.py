
import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """ Carrier specific packaging type """
    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingService(lib.StrEnum):
    """ Carrier specific services """
    logistic_io_standard_service = "Logistic IO Standard Service"


class ShippingOption(lib.Enum):
    """ Carrier specific options """
    # logistic_io_option = lib.OptionEnum("code")

    """ Unified Option type mapping """
    # insurance = logistic_io_coverage  #  maps unified karrio option to carrier specific

    pass


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = ["on_hold", "115", "134"]
    delivered = ["delivered", "132", "112", "149"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed", "104", "122", "123", "167", "170"]
    delivery_delayed = ["delivery_delayed", "116", "117", "118", "119", "121", "137", "138", "169"]
    out_for_delivery = ["out_for_delivery", "111", "140", "148"]
    ready_for_pickup = ["ready_for_pickup", "101"]
