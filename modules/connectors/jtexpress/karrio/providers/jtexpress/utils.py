
import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors
import hashlib

class Settings(core.Settings):
    """J&T Express connection settings."""

    # Add carrier specific api connection properties here
    username: str
    api_key: str
    signature_key: str
    company_id: str

    @property
    def carrier_name(self):
        return "jtexpress"

    @property
    def server_url(self):
        return (
            "https://demoopenapi.jtjms-sa.com"
            if self.test_mode
            else "https://openapi.jtjms-sa.com"
        )

    # """uncomment the following code block to expose a carrier tracking url."""
    # @property
    # def tracking_url(self):
    #     return "https://www.carrier.com/tracking?tracking-id={}"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode()).decode("ascii")

    @property
    def generate_signature_key(self, data:dict):
        pair = "%s%s" % (lib.to_json(data), self.signature_key)
        md5_pair = hashlib.md5(pair.encode()).digest()
        return base64.b64encode(md5_pair).decode("ascii")

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

#     """uncomment the following code block to implement the oauth login."""
#     @property
#     def access_token(self):
#         """Retrieve the access_token using the client_id|client_secret pair
#         or collect it from the cache if an unexpired access_token exist.
#         """
#         cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"
#         now = datetime.datetime.now() + datetime.timedelta(minutes=30)

#         auth = self.connection_cache.get(cache_key) or {}
#         token = auth.get("access_token")
#         expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

#         if token is not None and expiry is not None and expiry > now:
#             return token

#         self.connection_cache.set(cache_key, lambda: login(self))
#         new_auth = self.connection_cache.get(cache_key)

#         return new_auth["access_token"]

# """uncomment the following code block to implement the oauth login."""
# def login(settings: Settings):
#     import karrio.providers.jtexpress.error as error

#     result = lib.request(
#         url=f"{settings.server_url}/oauth/token",
#         method="POST",
#         headers={"content-Type": "application/x-www-form-urlencoded"},
#         data=lib.to_query_string(
#             dict(
#                 grant_type="client_credentials",
#                 client_id=settings.client_id,
#                 client_secret=settings.client_secret,
#             )
#         ),
#     )

#     response = lib.to_dict(result)
#     messages = error.parse_error_response(response, settings)

#     if any(messages):
#         raise errors.ParsedMessagesError(messages)

#     expiry = datetime.datetime.now() + datetime.timedelta(
#         seconds=float(response.get("expires_in", 0))
#     )
#     return {**response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
