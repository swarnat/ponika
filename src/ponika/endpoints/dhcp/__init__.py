from typing import TYPE_CHECKING
from ponika.endpoints.dhcp.servers_ipv4 import IPv4ServerEndpoint
from ponika.endpoints.dhcp.servers_ipv6 import IPv6ServerEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class DHCPEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self._client: "PonikaClient" = client
        self.server_ipv4 = IPv4ServerEndpoint(client)
        self.server_ipv6 = IPv6ServerEndpoint(client)
