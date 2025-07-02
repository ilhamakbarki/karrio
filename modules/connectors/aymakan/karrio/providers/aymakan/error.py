"""Karrio Aymakan error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.aymakan.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    messages = []
    if response.get("error"):
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                message=response.get("message"),
                details={**kwargs},
            )
        )
    return messages
