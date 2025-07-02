
import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """Logistic IO connection settings."""

    username: str
    password: str

    @property
    def carrier_name(self):
        return "logistic_io"

    @property
    def server_url(self):
        return (
            "https://sandbox.api.logistiq.io"
            if self.test_mode
            else "https://api.logistiq.io"
        )

    # """uncomment the following code block to expose a carrier tracking url."""
    # @property
    # def tracking_url(self):
    #     return "https://www.carrier.com/tracking?tracking-id={}"

    # """uncomment the following code block to implement the Basic auth."""
    # @property
    # def authorization(self):
    #     pair = "%s:%s" % (self.username, self.password)
    #     return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def access_token(self):
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.carrier_name}|{self.username}|{self.password}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=5)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token
        else:
            refreshToken = auth.get("refresh_token")
            if refreshToken is None:
                self.connection_cache.set(cache_key, lambda: login(self))
                new_auth = self.connection_cache.get(cache_key)
            else:
                self.connection_cache.set(cache_key, lambda: refresh_token(self, refreshToken))
                new_auth = self.connection_cache.get(cache_key)
            return new_auth["access_token"]

def login(settings: Settings):
    import karrio.providers.logistic_io.error as error

    result = lib.request(
        url=f"{settings.server_url}/auth/api/v1/accounts/login",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "user-agent": "app/1.0",
        },
        data=lib.to_json(
            dict(
                email=settings.username,
                password=settings.password,
            )
        ),
    )

    response = lib.to_dict(result)
    status = response.get("status")

    if status is not True:
        raise errors.ParsedMessagesError([
            response.get("detail") or response.get("error") or "Invalid username or password"
        ])

    expiry = datetime.datetime.now() + datetime.timedelta(minutes=60)
    return {
        "access_token": response.get("token"),
        "refresh_token": response.get("refreshToken"),
        "expiry": lib.fdatetime(expiry),
    }

def refresh_token(settings: Settings, refreshToken: str):
    import karrio.providers.logistic_io.error as error

    result = lib.request(
        url=f"{settings.server_url}/auth/api/v1/accounts/token",
        method="POST",
        headers={
            "Content-Type": "application/json",
            "user-agent": "app/1.0",
        },
        data=lib.to_json(
            dict(
                refresh_token=refreshToken,
            )
        ),
    )

    response = lib.to_dict(result)
    status = response.get("status")
    if status is not True:
        data = login(settings)
        if data.get("access_token") is None:
            raise errors.ParsedMessagesError([
                response.get("error_details") or "Invalid refresh token"
            ])
    else:
        data = response.get("data") or {}
    expiry = datetime.datetime.now() + datetime.timedelta(minutes=60)
    return {
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token"),
        "expiry": lib.fdatetime(expiry),
    }

class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
