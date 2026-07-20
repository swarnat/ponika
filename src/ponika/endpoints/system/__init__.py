from typing import TYPE_CHECKING

from ponika.endpoints.system.actions import ActionsEndpoint
from ponika.endpoints.system.banner import BannerEndpoint
from ponika.endpoints.system.buttons import ButtonsEndpoint
from ponika.endpoints.system.device import DeviceEndpoint
from ponika.endpoints.system.general import GeneralEndpoint
from ponika.endpoints.system.led import LedEndpoint

if TYPE_CHECKING:
    from ponika import PonikaClient


class SystemEndpoint:
    def __init__(self, client: 'PonikaClient') -> None:
        self._client = client
        self.actions = ActionsEndpoint(client)
        self.banner = BannerEndpoint(client)
        self.buttons = ButtonsEndpoint(client)
        self.general = GeneralEndpoint(client)
        self.device = DeviceEndpoint(client)
        self.led = LedEndpoint(client)
