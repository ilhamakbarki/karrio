"""Karrio J&T Express shipment API implementation."""

# import karrio.schemas.jtexpress.shipping_request as jtexpress
# import karrio.schemas.jtexpress.shipping_response as shipping

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.jtexpress.error as error
import karrio.providers.jtexpress.utils as provider_utils
import karrio.providers.jtexpress.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings)
        if "tracking_number" in response
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    details = None  # parse carrier shipment type from "data"
    label = ""  # extract and process the shipment label to a valid base64 text
    # invoice = ""  # extract and process the shipment invoice to a valid base64 text if applies

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="",  # extract tracking number from shipment
        shipment_identifier="",  # extract shipment identifier from shipment
        label_type="PDF",  # extract shipment label file format
        docs=models.Documents(
            label=label,  # pass label base64 text
            # invoice=invoice,  # pass invoice base64 text if applies
        ),
        meta=dict(
            # any relevent meta
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # map data to convert karrio model to jtexpress specific type
    request = None

    return lib.Serializable(request, lib.to_dict)
