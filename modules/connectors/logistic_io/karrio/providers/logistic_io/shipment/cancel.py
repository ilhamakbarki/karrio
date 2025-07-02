
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.logistic_io.error as error
import karrio.providers.logistic_io.utils as provider_utils
import karrio.providers.logistic_io.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = True  # compute shipment cancel success state

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        ) if success else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    # map data to convert karrio model to logistic_io specific type
    request = None

    return lib.Serializable(request, lib.to_dict)
