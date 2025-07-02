"""Karrio Logistic IO tracking API implementation."""

# import karrio.schemas.logistic_io.tracking_request as logistic_io
import karrio.schemas.logistic_io.tracking_response as tracking

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.logistic_io.error as error
import karrio.providers.logistic_io.utils as provider_utils
import karrio.providers.logistic_io.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(responses, settings)
        ],
        start=[],
    )

    shipments = lib.to_object(tracking.TrackingResponseType).data if responses.get("status") is True else None
    tracking_details = [
        _extract_details(details, settings)
        for details in shipments
    ]

    return tracking_details, messages


def _extract_details(
    data: tracking.DatumType,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if data.order_details.current_stage.alpha_status_code in status.value
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=data.cp_awb,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.date, "%Y-%m-%dT%H:%M:%S.%fZ"),
                description=event.status_remark,
                code=event.status,
                time=lib.flocaltime(event.created_date, "%Y-%m-%dT%H:%M:%S.%fZ"),
                location=event.scanned_location,
            )
            for event in data.tracking_history.updates
        ],
        estimated_delivery=lib.fdate(data.order_details.delivery_date, "%Y-%m-%dT%H:%M:%S.%fZ"),
        delivered=status == "delivered",
        status=status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    track_ids = ",".join(payload.tracking_numbers)
    request = dict(cp_awb=track_ids)
    return lib.Serializable(request, lib.to_dict)
