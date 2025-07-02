"""Karrio Aymakan client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.aymakan.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/service",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        track_ids = request.serialize()["track_ids"]
        response = lib.request(
            url=f"{self.settings.server_url}/shipping/track/{track_ids}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Authorization": self.settings.authorization,
                "Content-Type": "application/json",
                "user-agent": "app/1.0",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
