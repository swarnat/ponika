from typing import TYPE_CHECKING

from ponika.endpoints.openvpn.config import ConfigEndpoint
from ponika.endpoints.openvpn.tls_clients import TlsClientsEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class OpenvpnEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client: 'PonikaClient' = client
        self.config = ConfigEndpoint(client)
        self.tls_clients = TlsClientsEndpoint(client)
