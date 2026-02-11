from typing import TYPE_CHECKING
from ponika.endpoints import Endpoint
from ponika.endpoints.firmware.device import FirmwareDeviceEndpoint
from ponika.endpoints.wireless.interfaces import InterfacesEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class FirmwareEndpoint(Endpoint):
    def __init__(self, client: "PonikaClient") -> None:
        super().__init__(client)
        
        self.device = FirmwareDeviceEndpoint(client)
