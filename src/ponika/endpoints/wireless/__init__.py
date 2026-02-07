from typing import TYPE_CHECKING
from ponika.endpoints.wireless.interfaces import InterfacesEndpoint
from ponika.endpoints.wireless.interfaces import WirelessInterfaceDefinition

if TYPE_CHECKING:
    from ponika import PonikaClient


class WirelessEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self._client: "PonikaClient" = client
        self.interfaces = InterfacesEndpoint(client)
