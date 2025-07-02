"""Karrio Logistic IO error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.logistic_io.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    messages = []
    if response.get("status") is False:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                message=response.get("message"),
                details={
                    "detail": response.get("detail"),
                    "status_code": response.get("status_code"),
                    **kwargs
                },
            )
        )
    return messages
